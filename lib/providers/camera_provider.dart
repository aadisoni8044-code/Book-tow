import 'dart:io';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:image/image.dart' as img;
import '../services/gallery_service.dart';

class CameraProvider extends ChangeNotifier with WidgetsBindingObserver {
  CameraController? _controller;
  List<CameraDescription> _cameras = [];
  int _selectedCameraIndex = 0;
  FlashMode _flashMode = FlashMode.off;
  bool _isInitialized = false;
  bool _isInitializing = false;
  bool _isCapturing = false;
  bool _isMockMode = false;
  String? _errorMessage;

  CameraController? get controller => _controller;
  List<CameraDescription> get cameras => _cameras;
  FlashMode get flashMode => _flashMode;
  bool get isInitialized => _isInitialized;
  bool get isInitializing => _isInitializing;
  bool get isCapturing => _isCapturing;
  bool get isMockMode => _isMockMode;
  String? get errorMessage => _errorMessage;

  CameraLensDirection get currentLensDirection {
    if (_cameras.isNotEmpty && _selectedCameraIndex < _cameras.length) {
      return _cameras[_selectedCameraIndex].lensDirection;
    }
    return CameraLensDirection.back;
  }

  CameraProvider() {
    WidgetsBinding.instance.addObserver(this);
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    final CameraController? cameraController = _controller;
    if (cameraController == null || !cameraController.value.isInitialized) {
      return;
    }

    if (state == AppLifecycleState.inactive || state == AppLifecycleState.paused) {
      _controller?.dispose();
      _isInitialized = false;
      notifyListeners();
    } else if (state == AppLifecycleState.resumed) {
      initializeCamera();
    }
  }

  /// Initializes available cameras and activates controller
  Future<void> initializeCamera({String preferredCamera = 'rear'}) async {
    if (_isInitializing) return;
    _isInitializing = true;
    _errorMessage = null;
    notifyListeners();

    try {
      _cameras = await availableCameras();
      if (_cameras.isEmpty) {
        _isMockMode = true;
        _isInitialized = true;
        _isInitializing = false;
        notifyListeners();
        return;
      }

      _isMockMode = false;

      // Find camera index based on preference
      final targetDirection = preferredCamera == 'front'
          ? CameraLensDirection.front
          : CameraLensDirection.back;

      int targetIndex = _cameras.indexWhere((c) => c.lensDirection == targetDirection);
      if (targetIndex == -1) targetIndex = 0;
      _selectedCameraIndex = targetIndex;

      await _initController(_cameras[_selectedCameraIndex]);
    } catch (e) {
      debugPrint('Camera initialization error: $e');
      _errorMessage = 'Camera initialization failed. Mock camera activated.';
      _isMockMode = true;
      _isInitialized = true;
    } finally {
      _isInitializing = false;
      notifyListeners();
    }
  }

  Future<void> _initController(CameraDescription camera) async {
    if (_controller != null) {
      await _controller!.dispose();
    }

    _controller = CameraController(
      camera,
      ResolutionPreset.high,
      enableAudio: false,
      imageFormatGroup: ImageFormatGroup.jpeg,
    );

    try {
      await _controller!.initialize();
      await _controller!.setFlashMode(_flashMode);
      _isInitialized = true;
    } catch (e) {
      debugPrint('Controller initialize exception: $e');
      _errorMessage = 'Failed to open camera: $e';
      _isMockMode = true;
      _isInitialized = true;
    }
  }

  /// Toggles through flash modes: Off -> Auto -> Always -> Torch -> Off
  Future<void> toggleFlash() async {
    if (_isMockMode || _controller == null || !_controller!.value.isInitialized) {
      // Toggle local flash state for UI in mock mode
      if (_flashMode == FlashMode.off) {
        _flashMode = FlashMode.always;
      } else if (_flashMode == FlashMode.always) {
        _flashMode = FlashMode.auto;
      } else {
        _flashMode = FlashMode.off;
      }
      notifyListeners();
      return;
    }

    try {
      if (_flashMode == FlashMode.off) {
        _flashMode = FlashMode.always;
      } else if (_flashMode == FlashMode.always) {
        _flashMode = FlashMode.auto;
      } else if (_flashMode == FlashMode.auto) {
        _flashMode = FlashMode.torch;
      } else {
        _flashMode = FlashMode.off;
      }

      await _controller!.setFlashMode(_flashMode);
      notifyListeners();
    } catch (e) {
      debugPrint('Error setting flash mode: $e');
    }
  }

  /// Switches between front and rear cameras
  Future<void> switchCamera() async {
    if (_isMockMode || _cameras.length < 2) {
      // In mock mode or single camera, simulate camera flip state
      if (_selectedCameraIndex == 0) {
        _selectedCameraIndex = 1;
      } else {
        _selectedCameraIndex = 0;
      }
      notifyListeners();
      return;
    }

    _selectedCameraIndex = (_selectedCameraIndex + 1) % _cameras.length;
    _isInitialized = false;
    notifyListeners();

    await _initController(_cameras[_selectedCameraIndex]);
    notifyListeners();
  }

  /// Captures a photo from the camera or generates a mock photo in mock mode
  Future<String?> takePicture() async {
    if (_isCapturing) return null;
    _isCapturing = true;
    notifyListeners();

    try {
      if (_isMockMode || _controller == null || !_controller!.value.isInitialized) {
        // Generate mock test photo
        final tempPath = await GalleryService.getTempImagePath(prefix: 'zipgram_mock');
        final mockImage = img.Image(width: 1080, height: 1440);
        // Paint gradient pattern for realistic camera frame
        for (int y = 0; y < mockImage.height; y++) {
          for (int x = 0; x < mockImage.width; x++) {
            final int r = (x * 255 ~/ mockImage.width);
            final int g = (y * 255 ~/ mockImage.height);
            final int b = ((x + y) * 255 ~/ (mockImage.width + mockImage.height));
            mockImage.setPixelRgb(x, y, r, g, b);
          }
        }
        final bytes = img.encodeJpg(mockImage, quality: 90);
        final file = File(tempPath);
        await file.writeAsBytes(bytes);
        return tempPath;
      }

      final XFile xFile = await _controller!.takePicture();
      return xFile.path;
    } catch (e) {
      debugPrint('Error capturing photo: $e');
      return null;
    } finally {
      _isCapturing = false;
      notifyListeners();
    }
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    _controller?.dispose();
    super.dispose();
  }
}
