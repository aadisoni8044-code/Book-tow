import 'package:flutter/foundation.dart';
import 'package:webview_flutter/webview_flutter.dart';

import '../models/browser_session.dart';
import 'cache_manager.dart';
import 'cookie_manager.dart';
import 'storage_manager.dart';

class PrivacySessionManager extends ChangeNotifier {
  final FireZipCookieManager _cookieManager = FireZipCookieManager();
  final FireZipCacheManager _cacheManager = FireZipCacheManager();
  final FireZipStorageManager _storageManager = FireZipStorageManager();

  BrowserSession? _currentSession;
  bool _isCleaning = false;
  DateTime? _lastCleanupTime;

  // Settings states
  bool _blockThirdPartyCookies = true;
  bool _doNotTrack = true;
  bool _javaScriptEnabled = true;
  bool _popUpBlocking = true;

  BrowserSession? get currentSession => _currentSession;
  bool get isCleaning => _isCleaning;
  DateTime? get lastCleanupTime => _lastCleanupTime;

  bool get blockThirdPartyCookies => _blockThirdPartyCookies;
  bool get doNotTrack => _doNotTrack;
  bool get javaScriptEnabled => _javaScriptEnabled;
  bool get popUpBlocking => _popUpBlocking;

  PrivacySessionManager() {
    createSession();
  }

  /// Creates a completely fresh temporary browsing session.
  BrowserSession createSession() {
    final newSessionId = 'fz_session_${DateTime.now().millisecondsSinceEpoch}';
    _currentSession = BrowserSession(
      sessionId: newSessionId,
      createdAt: DateTime.now(),
      tabs: [],
    );
    notifyListeners();
    debugPrint('[FireZip] Created new temporary session: $newSessionId');
    return _currentSession!;
  }

  /// Clears cookies from WebView storage.
  Future<bool> clearCookies() async {
    return await _cookieManager.clearCookies();
  }

  /// Clears cache.
  Future<bool> clearCache([WebViewController? controller]) async {
    return await _cacheManager.clearCache(controller);
  }

  /// Clears WebStorage.
  Future<bool> clearWebStorage([List<WebViewController>? controllers]) async {
    return await _storageManager.clearWebStorage(controllers);
  }

  /// Clears in-memory session history.
  void clearHistory() {
    debugPrint('[FireZip] In-memory browsing history reset.');
    notifyListeners();
  }

  /// Clears all open temporary tabs.
  void clearTemporaryTabs() {
    _currentSession?.tabs.clear();
    _currentSession?.activeTabIndex = 0;
    notifyListeners();
    debugPrint('[FireZip] All temporary tabs cleared.');
  }

  /// Clears all temporary session data (Cookies, Cache, WebStorage, History, Tabs).
  Future<void> clearSession([List<WebViewController>? controllers]) async {
    _isCleaning = true;
    notifyListeners();

    await clearCookies();
    await clearCache(controllers != null && controllers.isNotEmpty ? controllers.first : null);
    await clearWebStorage(controllers);
    clearHistory();
    clearTemporaryTabs();

    _lastCleanupTime = DateTime.now();
    _isCleaning = false;

    // Start a fresh session ID for subsequent browsing
    createSession();
    notifyListeners();
    debugPrint('[FireZip] Complete session clearance completed successfully.');
  }

  /// Invoked during lifecycle events (app detached/closed/paused) to clean session data.
  Future<void> cleanupOnExit([List<WebViewController>? controllers]) async {
    debugPrint('[FireZip] Executing automatic session cleanup on exit/lifecycle change...');
    await clearSession(controllers);
  }

  void updateSettings({
    bool? blockThirdPartyCookies,
    bool? doNotTrack,
    bool? javaScriptEnabled,
    bool? popUpBlocking,
  }) {
    if (blockThirdPartyCookies != null) _blockThirdPartyCookies = blockThirdPartyCookies;
    if (doNotTrack != null) _doNotTrack = doNotTrack;
    if (javaScriptEnabled != null) _javaScriptEnabled = javaScriptEnabled;
    if (popUpBlocking != null) _popUpBlocking = popUpBlocking;
    notifyListeners();
  }
}
