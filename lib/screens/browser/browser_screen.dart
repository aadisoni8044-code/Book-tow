import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:webview_flutter/webview_flutter.dart';

import '../../browser/browser_controller.dart';
import '../../browser/tab_manager.dart';
import '../../models/browser_tab.dart';
import '../../privacy/privacy_session_manager.dart';
import '../../theme/app_theme.dart';
import '../../widgets/address_bar/address_bar.dart';
import '../../widgets/browser_toolbar/browser_toolbar.dart';
import '../downloads/downloads_screen.dart';
import '../error/error_screen.dart';
import '../home/home_screen.dart';
import '../settings/settings_screen.dart';
import '../tabs/tabs_screen.dart';

class BrowserScreen extends StatefulWidget {
  const BrowserScreen({super.key});

  @override
  State<BrowserScreen> createState() => _BrowserScreenState();
}

class _BrowserScreenState extends State<BrowserScreen> {
  final Map<String, WebViewController> _controllers = {};

  WebViewController _getOrCreateController(BrowserTab tab) {
    if (_controllers.containsKey(tab.id)) {
      return _controllers[tab.id]!;
    }

    final controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setNavigationDelegate(
        NavigationDelegate(
          onPageStarted: (String url) {
            tab.update(isLoading: true, url: url, errorType: WebErrorType.none);
          },
          onPageFinished: (String url) async {
            final title = await _controllers[tab.id]?.getTitle();
            final canGoBack = await _controllers[tab.id]?.canGoBack() ?? false;
            final canGoForward = await _controllers[tab.id]?.canGoForward() ?? false;
            tab.update(
              isLoading: false,
              url: url,
              title: title ?? BrowserController.formatDisplayUrl(url),
              canGoBack: canGoBack,
              canGoForward: canGoForward,
            );
          },
          onWebResourceError: (WebResourceError error) {
            final errorType = BrowserController.mapError(error.errorCode, error.description);
            tab.update(
              isLoading: false,
              errorType: errorType,
              errorMessage: error.description,
            );
          },
        ),
      );

    if (tab.url != 'firezip://home' && tab.url.isNotEmpty) {
      final parsed = BrowserController.parseInputUrl(tab.url);
      controller.loadRequest(Uri.parse(parsed));
    }

    _controllers[tab.id] = controller;
    tab.controller = controller;
    return controller;
  }

  void _navigateToUrl(BrowserTab tab, String rawInput) {
    tab.clearError();
    final parsed = BrowserController.parseInputUrl(rawInput);
    tab.update(url: parsed, title: BrowserController.formatDisplayUrl(parsed));

    if (parsed == 'firezip://home') {
      return;
    }

    final controller = _getOrCreateController(tab);
    controller.loadRequest(Uri.parse(parsed));
  }

  void _openMenuModal(BuildContext context) {
    final tabManager = Provider.of<TabManager>(context, listen: false);
    final privacyManager = Provider.of<PrivacySessionManager>(context, listen: false);

    showModalBottomSheet(
      context: context,
      backgroundColor: AppTheme.surface,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (ctx) => SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const SizedBox(height: 8),
            Container(
              width: 36,
              height: 4,
              decoration: BoxDecoration(
                color: AppTheme.border,
                borderRadius: BorderRadius.circular(2),
              ),
            ),
            const SizedBox(height: 16),
            ListTile(
              leading: const Icon(Icons.add_rounded, color: AppTheme.flameOrange),
              title: const Text('New Tab', style: TextStyle(color: AppTheme.textPrimary)),
              onTap: () {
                Navigator.pop(ctx);
                tabManager.addTab();
              },
            ),
            ListTile(
              leading: const Icon(Icons.tab_rounded, color: AppTheme.zipCyan),
              title: Text('Tabs (${tabManager.tabs.length})', style: const TextStyle(color: AppTheme.textPrimary)),
              onTap: () {
                Navigator.pop(ctx);
                _openTabsScreen(context);
              },
            ),
            ListTile(
              leading: const Icon(Icons.download_rounded, color: AppTheme.textPrimary),
              title: const Text('Downloads', style: TextStyle(color: AppTheme.textPrimary)),
              onTap: () {
                Navigator.pop(ctx);
                _openDownloadsScreen(context);
              },
            ),
            ListTile(
              leading: const Icon(Icons.security_rounded, color: AppTheme.privacyGreen),
              title: const Text('Privacy & Security Settings', style: TextStyle(color: AppTheme.textPrimary)),
              onTap: () {
                Navigator.pop(ctx);
                _openSettingsScreen(context);
              },
            ),
            const Divider(color: AppTheme.border),
            ListTile(
              leading: const Icon(Icons.cleaning_services_rounded, color: AppTheme.flameOrange),
              title: const Text('Clear Current Session Data', style: TextStyle(color: AppTheme.flameOrange, fontWeight: FontWeight.w700)),
              onTap: () async {
                Navigator.pop(ctx);
                final controllersList = _controllers.values.toList();
                await privacyManager.clearSession(controllersList);
                _controllers.clear();
                tabManager.closeAllTabs();
                if (context.mounted) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Session data cleared.')),
                  );
                }
              },
            ),
            const SizedBox(height: 12),
          ],
        ),
      ),
    );
  }

  void _openTabsScreen(BuildContext context) {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => TabsScreen(onCloseView: () => Navigator.of(context).pop()),
      ),
    );
  }

  void _openSettingsScreen(BuildContext context) {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => const SettingsScreen(),
      ),
    );
  }

  void _openDownloadsScreen(BuildContext context) {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => const DownloadsScreen(),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final tabManager = Provider.of<TabManager>(context);
    final activeTab = tabManager.activeTab;
    final size = MediaQuery.of(context).size;
    final isDesktop = size.width > 700;

    if (activeTab == null) {
      return const Scaffold(
        backgroundColor: AppTheme.background,
        body: Center(child: CircularProgressIndicator()),
      );
    }

    final isHomeTab = activeTab.url == 'firezip://home' || activeTab.url == 'about:blank';

    return Scaffold(
      backgroundColor: AppTheme.background,
      body: SafeArea(
        child: Column(
          children: [
            // Desktop Top Header TabBar
            if (isDesktop)
              DesktopHeaderTabBar(
                tabs: tabManager.tabs,
                activeIndex: tabManager.activeTabIndex,
                onSelectTab: (idx) => tabManager.selectTabByIndex(idx),
                onCloseTab: (id) => tabManager.closeTab(id),
                onNewTab: () => tabManager.addTab(),
              ),

            // Top Address Bar
            AddressBar(
              currentUrl: activeTab.url,
              isLoading: activeTab.isLoading,
              onSubmit: (input) => _navigateToUrl(activeTab, input),
              onReload: () {
                activeTab.clearError();
                if (_controllers.containsKey(activeTab.id)) {
                  _controllers[activeTab.id]?.reload();
                } else {
                  _navigateToUrl(activeTab, activeTab.url);
                }
              },
              onOpenMenu: () => _openMenuModal(context),
            ),

            // Main Web View / Home View / Error View Body
            Expanded(
              child: AnimatedSwitcher(
                duration: const Duration(milliseconds: 250),
                child: activeTab.errorType != WebErrorType.none
                    ? FireZipErrorScreen(
                        errorType: activeTab.errorType,
                        customMessage: activeTab.errorMessage,
                        onTryAgain: () {
                          activeTab.clearError();
                          _navigateToUrl(activeTab, activeTab.url);
                        },
                        onGoHome: () {
                          activeTab.clearError();
                          _navigateToUrl(activeTab, 'firezip://home');
                        },
                      )
                    : isHomeTab
                        ? HomeScreen(
                            onNavigate: (input) => _navigateToUrl(activeTab, input),
                            onOpenSettings: () => _openSettingsScreen(context),
                            onOpenDownloads: () => _openDownloadsScreen(context),
                            onOpenTabs: () => _openTabsScreen(context),
                          )
                        : _buildWebViewContainer(activeTab),
              ),
            ),

            // Mobile Bottom Navigation Toolbar
            if (!isDesktop)
              MobileBottomToolbar(
                canGoBack: activeTab.canGoBack,
                canGoForward: activeTab.canGoForward,
                tabCount: tabManager.tabs.length,
                onGoBack: () async {
                  if (_controllers.containsKey(activeTab.id)) {
                    await _controllers[activeTab.id]?.goBack();
                  }
                },
                onGoForward: () async {
                  if (_controllers.containsKey(activeTab.id)) {
                    await _controllers[activeTab.id]?.goForward();
                  }
                },
                onReload: () {
                  activeTab.clearError();
                  _controllers[activeTab.id]?.reload();
                },
                onNewTab: () => tabManager.addTab(),
                onOpenTabs: () => _openTabsScreen(context),
                onOpenMenu: () => _openMenuModal(context),
              ),
          ],
        ),
      ),
    );
  }

  Widget _buildWebViewContainer(BrowserTab tab) {
    // If WebViewController exists and is supported
    try {
      final controller = _getOrCreateController(tab);
      return WebViewWidget(controller: controller);
    } catch (_) {
      // Fallback frame renderer for environments without native webview platform implementations
      return Container(
        color: AppTheme.surface,
        alignment: Alignment.center,
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.web_rounded, size: 64, color: AppTheme.zipCyan),
            const SizedBox(height: 16),
            Text(
              'Rendering ${tab.url}',
              style: const TextStyle(color: AppTheme.textPrimary, fontSize: 18, fontWeight: FontWeight.bold),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 12),
            const Text(
              'Temporary Private Session Active',
              style: TextStyle(color: AppTheme.privacyGreen, fontWeight: FontWeight.w600),
            ),
            const SizedBox(height: 24),
            ElevatedButton.icon(
              icon: const Icon(Icons.home_rounded),
              label: const Text('Return Home'),
              onPressed: () => _navigateToUrl(tab, 'firezip://home'),
            ),
          ],
        ),
      );
    }
  }
}
