import 'browser_tab.dart';

class BrowserSession {
  final String sessionId;
  final DateTime createdAt;
  final List<BrowserTab> tabs;
  int activeTabIndex;

  BrowserSession({
    required this.sessionId,
    DateTime? createdAt,
    List<BrowserTab>? tabs,
    this.activeTabIndex = 0,
  })  : createdAt = createdAt ?? DateTime.now(),
        tabs = tabs ?? [];

  BrowserTab? get activeTab {
    if (tabs.isEmpty || activeTabIndex < 0 || activeTabIndex >= tabs.length) {
      return null;
    }
    return tabs[activeTabIndex];
  }
}
