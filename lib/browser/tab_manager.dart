import 'package:flutter/foundation.dart';
import '../models/browser_tab.dart';
import '../privacy/privacy_session_manager.dart';

class TabManager extends ChangeNotifier {
  final PrivacySessionManager sessionManager;
  final List<BrowserTab> _tabs = [];
  int _activeTabIndex = 0;

  List<BrowserTab> get tabs => List.unmodifiable(_tabs);
  int get activeTabIndex => _activeTabIndex;

  BrowserTab? get activeTab {
    if (_tabs.isEmpty || _activeTabIndex < 0 || _activeTabIndex >= _tabs.length) {
      return null;
    }
    return _tabs[_activeTabIndex];
  }

  TabManager({required this.sessionManager}) {
    // Initialize with one default tab
    addTab(url: 'firezip://home', title: 'Home');
  }

  /// Adds a new tab to the current temporary session.
  BrowserTab addTab({String url = 'firezip://home', String title = 'New Tab'}) {
    final String newId = 'tab_${DateTime.now().microsecondsSinceEpoch}';
    final newTab = BrowserTab(
      id: newId,
      url: url,
      title: title,
      isLoading: false,
    );
    _tabs.add(newTab);
    _activeTabIndex = _tabs.length - 1;
    notifyListeners();
    return newTab;
  }

  /// Closes a tab by ID.
  void closeTab(String id) {
    final index = _tabs.indexWhere((t) => t.id == id);
    if (index == -1) return;

    _tabs.removeAt(index);
    if (_tabs.isEmpty) {
      // If all tabs closed, re-open a fresh home tab
      addTab(url: 'firezip://home', title: 'Home');
    } else {
      if (_activeTabIndex >= _tabs.length) {
        _activeTabIndex = _tabs.length - 1;
      }
      notifyListeners();
    }
  }

  /// Closes all tabs and triggers complete session cleanup.
  Future<void> closeAllTabs() async {
    final controllers = _tabs.map((t) => t.controller).whereType<dynamic>().toList();
    _tabs.clear();
    _activeTabIndex = 0;
    notifyListeners();

    // Trigger full session cleanup
    await sessionManager.clearSession();

    // Re-initialize with clean home tab
    addTab(url: 'firezip://home', title: 'Home');
  }

  /// Selects a tab by ID.
  void selectTab(String id) {
    final index = _tabs.indexWhere((t) => t.id == id);
    if (index != -1 && index != _activeTabIndex) {
      _activeTabIndex = index;
      notifyListeners();
    }
  }

  void selectTabByIndex(int index) {
    if (index >= 0 && index < _tabs.length) {
      _activeTabIndex = index;
      notifyListeners();
    }
  }
}
