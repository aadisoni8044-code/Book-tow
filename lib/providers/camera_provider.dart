import 'dart:async';
import 'dart:io';
import 'dart:typed_data';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:path_provider/path_provider.dart';
import 'package:permission_handler/permission_handler.dart';
import '../models/app_filter.dart';
import '../services/filter_processor.dart';

class CameraProvider with ChangeNotifier {
  CameraController? _controller;
  List<CameraDescription> _cameras = [];
  int _selectedCameraIndex = 0;

  bool _isInitializing = false;
  bool _isInitialized = false;
  bool _hasPermission = false;
  String? _errorMessage;

  AppFilter _selectedFilter = AppFilter.defaultFilter;
  bool _isCapturing = false;
  int _countdownSeconds = 0;

  File? _capturedImageFile;
  Uint8List? _capturedFilteredBytes;

  // Getters
  CameraController? get controller => _controller;
  List<CameraDescription> get cameras => _cameras;
  bool get isInitializing => _isInitializing;
  bool get isInitialized => _isInitialized;
  bool get hasPermission => _hasPermission;
  String? get errorMessage => _errorMessage;

  AppFilter get selectedFilter => _selectedFilter;
  bool get isCapturing => _isCapturing;
  int get countdownSeconds => _countdownSeconds;

  File? get capturedImageFile => _capturedImageFile;
  Uint8List? get capturedFilteredBytes => _capturedFilteredBytes;

  /// Request runtime camera permission and initialize camera hardware
  Future<void> requestPermissionsAndInit() async {
    _isInitializing = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final status = await Permission.camera.request();
      if (status.isGranted) {
        _hasPermission = true;
        await _initCamera();
      } else if (status.isPermanentlyDenied) {
        _hasPermission = false;
        _errorMessage = 'Camera permission permanently denied. Please enable it in Settings.';
      } else {
        _hasPermission = false;
        _errorMessage = 'Camera permission is required to use SnapCam.';
      }
    } catch (e) {
      _errorMessage = 'Error requesting camera permissions: $e';
    } finally {
      _isInitializing = false;
      notifyListeners();
    }
  }

  /// Initialize camera hardware controller
  Future<void> _initCamera() async {
    try {
      _cameras = await availableCameras();
      if (_cameras.isEmpty) {
        _isInitialized = false;
        _errorMessage = 'No camera hardware found on this device.';
        return;
      }

      final camera = _cameras[_selectedCameraIndex];
      _controller = CameraController(
        camera,
        ResolutionPreset.max,
        enableAudio: false,
        imageFormatGroup: ImageFormatGroup.jpeg,
      );

      await _controller!.initialize();
      _isInitialized = true;
      _errorMessage = null;
    } catch (e) {
      _isInitialized = false;
      _errorMessage = 'Failed to initialize camera: $e';
    }
  }

  /// Switch between Front and Rear camera lens
  Future<void> switchCamera() async {
    if (_cameras.length < 2) return;

    _selectedCameraIndex = (_selectedCameraIndex + 1) % _cameras.length;
    await _controller?.dispose();
    _controller = null;
    _isInitialized = false;
    notifyListeners();

    await _initCamera();
    notifyListeners();
  }

  /// Select active filter
  void setFilter(AppFilter filter) {
    _selectedFilter = filter;
    notifyListeners();

    // If a photo is already captured, update filtered bytes on the fly
    if (_capturedImageFile != null) {
      _applyFilterToCaptured(_selectedFilter);
    }
  }

  /// Apply selected filter to captured photo
  Future<void> _applyFilterToCaptured(AppFilter filter) async {
    if (_capturedImageFile == null) return;
    try {
      final Uint8List originalBytes = await _capturedImageFile!.readAsBytes();
      _capturedFilteredBytes = await FilterProcessor.processImageBytes(
        originalBytes,
        filter,
      );
      notifyListeners();
    } catch (e) {
      debugPrint('Error applying filter to captured photo: $e');
    }
  }

  /// Update Camera Flash Mode
  Future<void> updateFlashMode(FlashMode mode) async {
    if (_controller == null || !_controller!.value.isInitialized) return;
    try {
      await _controller!.setFlashMode(mode);
    } catch (e) {
      debugPrint('Failed to set flash mode: $e');
    }
  }

  /// Trigger Photo Capture with timer countdown
  Future<File?> takePicture({int timerSeconds = 0}) async {
    if (_isCapturing) return null;

    if (timerSeconds > 0) {
      _isCapturing = true;
      _countdownSeconds = timerSeconds;
      notifyListeners();

      while (_countdownSeconds > 0) {
        await Future.delayed(const Duration(seconds: 1));
        _countdownSeconds--;
        notifyListeners();
      }
    }

    _isCapturing = true;
    notifyListeners();

    try {
      XFile xFile;
      if (_controller != null && _controller!.value.isInitialized) {
        xFile = await _controller!.takePicture();
      } else {
        // Fallback or mock image generation if hardware camera preview is unavailable
        xFile = await _generateMockCapturedFile();
      }

      _capturedImageFile = File(xFile.path);
      final Uint8List originalBytes = await _capturedImageFile!.readAsBytes();

      _capturedFilteredBytes = await FilterProcessor.processImageBytes(
        originalBytes,
        _selectedFilter,
      );

      return _capturedImageFile;
    } catch (e) {
      _errorMessage = 'Failed to capture photo: $e';
      return null;
    } finally {
      _isCapturing = false;
      _countdownSeconds = 0;
      notifyListeners();
    }
  }

  /// Generates a placeholder image file when hardware camera is not available (e.g., emulator/desktop)
  Future<XFile> _generateMockCapturedFile() async {
    final tempDir = await getTemporaryDirectory();
    final file = File('${tempDir.path}/snap_cam_mock_${DateTime.now().millisecondsSinceEpoch}.jpg');

    // Create a simple colored solid image bytes
    final mockBytes = Uint8List.fromList(List.generate(200 * 200 * 3, (index) => (index * 7) % 256));
    await file.writeAsBytes(mockBytes);
    return XFile(file.path);
  }

  /// Reset captured image and return to camera view
  void clearCaptured() {
    _capturedImageFile = null;
    _capturedFilteredBytes = null;
    notifyListeners();
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }
}
