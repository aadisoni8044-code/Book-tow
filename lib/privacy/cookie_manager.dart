import 'package:flutter/foundation.dart';
import 'package:webview_flutter/webview_flutter.dart';

class FireZipCookieManager {
  WebViewCookieManager? _cookieManager;

  FireZipCookieManager() {
    try {
      _cookieManager = WebViewCookieManager();
    } catch (e) {
      debugPrint('[FireZip] WebViewCookieManager uninitialized in test or unsupported platform: $e');
    }
  }

  /// Clears all cookies stored in the WebView.
  Future<bool> clearCookies() async {
    if (_cookieManager == null) return false;
    try {
      final bool hadCookies = await _cookieManager!.clearCookies();
      debugPrint('[FireZip] WebView cookies cleared (hadCookies: $hadCookies)');
      return true;
    } catch (e) {
      debugPrint('[FireZip] Error clearing cookies: $e');
      return false;
    }
  }
}
