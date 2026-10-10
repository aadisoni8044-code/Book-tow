import 'package:flutter/material.dart';

enum FlashMode { off, auto, on, torch }
enum FilterQuality { normal, high, ultra }

class SettingsProvider with ChangeNotifier {
  FlashMode _flashMode = FlashMode.off;
  bool _gridEnabled = false;
  int _timerSeconds = 0; // 0, 3, 10
  FilterQuality _filterQuality = FilterQuality.high;
  bool _autoSaveToGallery = false;
  bool _soundEnabled = true;
  bool _isPremiumUser = false;

  // Getters
  FlashMode get flashMode => _flashMode;
  bool get gridEnabled => _gridEnabled;
  int get timerSeconds => _timerSeconds;
  FilterQuality get filterQuality => _filterQuality;
  bool get autoSaveToGallery => _autoSaveToGallery;
  bool get soundEnabled => _soundEnabled;
  bool get isPremiumUser => _isPremiumUser;

  // Setters
  void toggleFlashMode() {
    switch (_flashMode) {
      case FlashMode.off:
        _flashMode = FlashMode.auto;
        break;
      case FlashMode.auto:
        _flashMode = FlashMode.on;
        break;
      case FlashMode.on:
        _flashMode = FlashMode.off;
        break;
      case FlashMode.torch:
        _flashMode = FlashMode.off;
        break;
    }
    notifyListeners();
  }

  void setFlashMode(FlashMode mode) {
    _flashMode = mode;
    notifyListeners();
  }

  void toggleGrid() {
    _gridEnabled = !_gridEnabled;
    notifyListeners();
  }

  void cycleTimer() {
    if (_timerSeconds == 0) {
      _timerSeconds = 3;
    } else if (_timerSeconds == 3) {
      _timerSeconds = 10;
    } else {
      _timerSeconds = 0;
    }
    notifyListeners();
  }

  void setTimerSeconds(int seconds) {
    _timerSeconds = seconds;
    notifyListeners();
  }

  void setFilterQuality(FilterQuality quality) {
    _filterQuality = quality;
    notifyListeners();
  }

  void setAutoSave(bool value) {
    _autoSaveToGallery = value;
    notifyListeners();
  }

  void setSoundEnabled(bool value) {
    _soundEnabled = value;
    notifyListeners();
  }

  void setPremiumUser(bool value) {
    _isPremiumUser = value;
    notifyListeners();
  }
}
