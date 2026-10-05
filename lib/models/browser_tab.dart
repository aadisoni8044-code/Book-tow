import 'package:flutter/foundation.dart';
import 'package:webview_flutter/webview_flutter.dart';

enum WebErrorType {
  none,
  noInternet,
  websiteUnavailable,
  invalidUrl,
  connectionError,
  sslError,
}

class BrowserTab extends ChangeNotifier {
  final String id;
  String url;
  String title;
  String? faviconUrl;
  bool isLoading;
  bool canGoBack;
  bool canGoForward;
  WebErrorType errorType;
  String? errorMessage;
  WebViewController? controller;

  BrowserTab({
    required this.id,
    this.url = 'about:blank',
    this.title = 'New Tab',
    this.faviconUrl,
    this.isLoading = false,
    this.canGoBack = false,
    this.canGoForward = false,
    this.errorType = WebErrorType.none,
    this.errorMessage,
    this.controller,
  });

  void update({
    String? url,
    String? title,
    String? faviconUrl,
    bool? isLoading,
    bool? canGoBack,
    bool? canGoForward,
    WebErrorType? errorType,
    String? errorMessage,
  }) {
    if (url != null) this.url = url;
    if (title != null) this.title = title;
    if (faviconUrl != null) this.faviconUrl = faviconUrl;
    if (isLoading != null) this.isLoading = isLoading;
    if (canGoBack != null) this.canGoBack = canGoBack;
    if (canGoForward != null) this.canGoForward = canGoForward;
    if (errorType != null) this.errorType = errorType;
    if (errorMessage != null) this.errorMessage = errorMessage;
    notifyListeners();
  }

  void clearError() {
    errorType = WebErrorType.none;
    errorMessage = null;
    notifyListeners();
  }
}
