import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';
import '../models/browser_tab.dart';
import '../models/search_engine.dart';
import '../utils/url_helper.dart';

class BrowserProvider with ChangeNotifier, WidgetsBindingObserver {
  final List<BrowserTab> _tabs = [];
  int _activeTabIndex = 0;

  List<BrowserTab> get tabs => List.unmodifiable(_tabs);
  int get activeTabIndex => _activeTabIndex;

  BrowserTab? get activeTab =>
      _tabs.isNotEmpty && _activeTabIndex >= 0 && _activeTabIndex < _tabs.length
          ? _tabs[_activeTabIndex]
          : null;

  BrowserProvider() {
    WidgetsBinding.instance.addObserver(this);
    // Initialize with 1 default home tab
    newTab();
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    clearAllTemporarySessionData();
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.paused || state == AppLifecycleState.detached) {
      // Clean temporary private session state on backgrounding/termination
      clearWebViewSessionData();
    }
  }

  void newTab({String initialUrl = 'about:blank', SearchEngine? searchEngine}) {
    final formattedUrl = UrlHelper.formatUrl(initialUrl, searchEngine: searchEngine);
    final id = DateTime.now().microsecondsSinceEpoch.toString();

    final tab = BrowserTab(
      id: id,
      url: formattedUrl,
      title: formattedUrl == 'about:blank' ? 'New Tab' : UrlHelper.getDisplayDomain(formattedUrl),
      isPrivate: true,
      isSecure: UrlHelper.isSecure(formattedUrl),
    );

    _tabs.add(tab);
    _activeTabIndex = _tabs.length - 1;
    notifyListeners();
  }

  void selectTab(int index) {
    if (index >= 0 && index < _tabs.length) {
      _activeTabIndex = index;
      notifyListeners();
    }
  }

  void closeTab(int index) {
    if (index < 0 || index >= _tabs.length) return;

    final closedTab = _tabs[index];
    _tabs.removeAt(index);

    // Clean up closed tab's controller reference if present
    closedTab.webViewController = null;

    if (_tabs.isEmpty) {
      // If all tabs closed, create a fresh new home tab
      newTab();
    } else {
      if (_activeTabIndex >= _tabs.length) {
        _activeTabIndex = _tabs.length - 1;
      }
      notifyListeners();
    }
  }

  void closeAllTabs() {
    _tabs.clear();
    clearWebViewSessionData();
    newTab();
  }

  void updateTabUrl(int index, String newUrl) {
    if (index >= 0 && index < _tabs.length) {
      final tab = _tabs[index];
      tab.url = newUrl;
      tab.isSecure = UrlHelper.isSecure(newUrl);
      if (newUrl == 'about:blank') {
        tab.title = 'New Tab';
      } else {
        tab.title = UrlHelper.getDisplayDomain(newUrl);
      }
      tab.errorMessage = null;
      notifyListeners();
    }
  }

  void updateTabTitle(int index, String title) {
    if (index >= 0 && index < _tabs.length && title.isNotEmpty) {
      _tabs[index].title = title;
      notifyListeners();
    }
  }

  void updateTabLoading(int index, bool isLoading, {double progress = 0.0}) {
    if (index >= 0 && index < _tabs.length) {
      _tabs[index].isLoading = isLoading;
      _tabs[index].progress = progress;
      notifyListeners();
    }
  }

  void updateTabNavState(int index, {required bool canGoBack, required bool canGoForward}) {
    if (index >= 0 && index < _tabs.length) {
      _tabs[index].canGoBack = canGoBack;
      _tabs[index].canGoForward = canGoForward;
      notifyListeners();
    }
  }

  void setTabError(int index, String error) {
    if (index >= 0 && index < _tabs.length) {
      _tabs[index].errorMessage = error;
      _tabs[index].isLoading = false;
      notifyListeners();
    }
  }

  void attachController(int index, WebViewController controller) {
    if (index >= 0 && index < _tabs.length) {
      _tabs[index].webViewController = controller;
    }
  }

  Future<void> goBack() async {
    final controller = activeTab?.webViewController as WebViewController?;
    if (controller != null && await controller.canGoBack()) {
      await controller.goBack();
    }
  }

  Future<void> goForward() async {
    final controller = activeTab?.webViewController as WebViewController?;
    if (controller != null && await controller.canGoForward()) {
      await controller.goForward();
    }
  }

  Future<void> reload() async {
    final controller = activeTab?.webViewController as WebViewController?;
    if (controller != null) {
      await controller.reload();
    } else if (activeTab != null) {
      updateTabUrl(_activeTabIndex, activeTab!.url);
    }
  }

  Future<void> stopLoading() async {
    final controller = activeTab?.webViewController as WebViewController?;
    if (controller != null) {
      await controller.runJavaScript('window.stop();');
    }
    if (activeTab != null) {
      updateTabLoading(_activeTabIndex, false);
    }
  }

  /// Clears native WebView cookies, local cache, and temporary browsing data
  Future<void> clearWebViewSessionData() async {
    try {
      final cookieManager = WebViewCookieManager();
      await cookieManager.clearCookies();
    } catch (_) {}
  }

  /// Wipes all in-memory temporary session data
  void clearAllTemporarySessionData() {
    clearWebViewSessionData();
    for (final tab in _tabs) {
      tab.webViewController = null;
    }
    _tabs.clear();
  }
}
