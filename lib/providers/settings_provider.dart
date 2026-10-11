import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

class SettingsProvider extends ChangeNotifier {
  static const String _keyQuality = 'photo_quality';
  static const String _keyFlashMode = 'default_flash';
  static const String _keyPreferredCamera = 'preferred_camera';

  int _photoQuality = 90; // 70 = Medium, 90 = High, 100 = Max
  String _defaultFlash = 'off'; // off, always, auto
  String _preferredCamera = 'rear'; // rear, front

  int get photoQuality => _photoQuality;
  String get defaultFlash => _defaultFlash;
  String get preferredCamera => _preferredCamera;

  SettingsProvider() {
    _loadSettings();
  }

  Future<void> _loadSettings() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      _photoQuality = prefs.getInt(_keyQuality) ?? 90;
      _defaultFlash = prefs.getString(_keyFlashMode) ?? 'off';
      _preferredCamera = prefs.getString(_keyPreferredCamera) ?? 'rear';
      notifyListeners();
    } catch (e) {
      debugPrint('Error loading settings: $e');
    }
  }

  Future<void> setPhotoQuality(int quality) async {
    _photoQuality = quality;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt(_keyQuality, quality);
  }

  Future<void> setDefaultFlash(String flash) async {
    _defaultFlash = flash;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_keyFlashMode, flash);
  }

  Future<void> setPreferredCamera(String camera) async {
    _preferredCamera = camera;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_keyPreferredCamera, camera);
  }
}
