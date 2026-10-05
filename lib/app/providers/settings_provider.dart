import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/search_engine.dart';

class SettingsProvider with ChangeNotifier {
  bool _privateMode = true;
  bool _isDarkMode = true;
  bool _javaScriptEnabled = true;
  bool _doNotTrack = true;
  bool _blockThirdPartyCookies = true;
  bool _popUpBlocking = true;
  SearchEngine _selectedSearchEngine = SearchEngine.defaultEngines.first;

  bool get privateMode => _privateMode;
  bool get isDarkMode => _isDarkMode;
  bool get javaScriptEnabled => _javaScriptEnabled;
  bool get doNotTrack => _doNotTrack;
  bool get blockThirdPartyCookies => _blockThirdPartyCookies;
  bool get popUpBlocking => _popUpBlocking;
  SearchEngine get selectedSearchEngine => _selectedSearchEngine;

  SettingsProvider() {
    _loadSettings();
  }

  Future<void> _loadSettings() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      _isDarkMode = prefs.getBool('is_dark_mode') ?? true;
      _javaScriptEnabled = prefs.getBool('javascript_enabled') ?? true;
      _doNotTrack = prefs.getBool('do_not_track') ?? true;
      _blockThirdPartyCookies = prefs.getBool('block_3rd_party_cookies') ?? true;
      _popUpBlocking = prefs.getBool('pop_up_blocking') ?? true;

      final engineId = prefs.getString('search_engine_id') ?? 'duckduckgo';
      _selectedSearchEngine = SearchEngine.defaultEngines.firstWhere(
        (e) => e.id == engineId,
        orElse: () => SearchEngine.defaultEngines.first,
      );
      notifyListeners();
    } catch (_) {}
  }

  Future<void> togglePrivateMode(bool value) async {
    _privateMode = value;
    notifyListeners();
  }

  Future<void> toggleDarkMode(bool value) async {
    _isDarkMode = value;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('is_dark_mode', value);
  }

  Future<void> toggleJavaScript(bool value) async {
    _javaScriptEnabled = value;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('javascript_enabled', value);
  }

  Future<void> toggleDoNotTrack(bool value) async {
    _doNotTrack = value;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('do_not_track', value);
  }

  Future<void> toggleBlockThirdPartyCookies(bool value) async {
    _blockThirdPartyCookies = value;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('block_3rd_party_cookies', value);
  }

  Future<void> togglePopUpBlocking(bool value) async {
    _popUpBlocking = value;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('pop_up_blocking', value);
  }

  Future<void> setSearchEngine(SearchEngine engine) async {
    _selectedSearchEngine = engine;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('search_engine_id', engine.id);
  }
}
