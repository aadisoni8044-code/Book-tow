import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'app/providers/browser_provider.dart';
import 'app/providers/download_provider.dart';
import 'app/providers/settings_provider.dart';
import 'app/screens/browser_screen.dart';
import 'app/screens/downloads_screen.dart';
import 'app/screens/home_screen.dart';
import 'app/screens/settings_screen.dart';
import 'app/screens/tabs_screen.dart';
import 'app/theme/app_theme.dart';
import 'app/widgets/address_bar.dart';
import 'app/widgets/browser_toolbar.dart';
import 'app/widgets/responsive_scaffold.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => SettingsProvider()),
        ChangeNotifierProvider(create: (_) => DownloadProvider()),
        ChangeNotifierProvider(create: (_) => BrowserProvider()),
      ],
      child: const FireZipApp(),
    ),
  );
}

class FireZipApp extends StatelessWidget {
  const FireZipApp({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<SettingsProvider>(
      builder: (context, settings, _) {
        return MaterialApp(
          title: 'FireZip',
          debugShowCheckedModeBanner: false,
          theme: AppTheme.lightTheme,
          darkTheme: AppTheme.darkTheme,
          themeMode: settings.isDarkMode ? ThemeMode.dark : ThemeMode.light,
          home: const MainScaffold(),
        );
      },
    );
  }
}

class MainScaffold extends StatefulWidget {
  const MainScaffold({super.key});

  @override
  State<MainScaffold> createState() => _MainScaffoldState();
}

class _MainScaffoldState extends State<MainScaffold> {
  @override
  Widget build(BuildContext context) {
    final browser = Provider.of<BrowserProvider>(context);
    final settings = Provider.of<SettingsProvider>(context, listen: false);
    final activeTab = browser.activeTab;

    final isHome = activeTab == null || activeTab.url == 'about:blank';

    return ResponsiveScaffold(
      body: SafeArea(
        child: Column(
          children: [
            AddressBar(
              currentUrl: activeTab?.url ?? 'about:blank',
              isLoading: activeTab?.isLoading ?? false,
              isSecure: activeTab?.isSecure ?? true,
              onSubmit: (input) {
                if (browser.activeTab == null) {
                  browser.newTab(initialUrl: input, searchEngine: settings.selectedSearchEngine);
                } else {
                  browser.updateTabUrl(
                    browser.activeTabIndex,
                    input,
                  );
                }
              },
              onReload: () => browser.reload(),
              onStop: () => browser.stopLoading(),
            ),
            Expanded(
              child: isHome
                  ? HomeScreen(
                      onSearch: (query) {
                        browser.updateTabUrl(
                          browser.activeTabIndex,
                          query,
                        );
                      },
                      onOpenTabs: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (_) => TabsScreen(onClose: () => Navigator.pop(context)),
                          ),
                        );
                      },
                      onOpenDownloads: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(builder: (_) => const DownloadsScreen()),
                        );
                      },
                      onOpenSettings: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (_) => SettingsScreen(
                              onOpenPrivacy: () {
                                Navigator.push(
                                  context,
                                  MaterialPageRoute(builder: (_) => const PrivacySettingsScreen()),
                                );
                              },
                              onOpenDownloads: () {
                                Navigator.push(
                                  context,
                                  MaterialPageRoute(builder: (_) => const DownloadsScreen()),
                                );
                              },
                            ),
                          ),
                        );
                      },
                    )
                  : BrowserScreen(
                      key: ValueKey(activeTab.id),
                      tab: activeTab,
                      tabIndex: browser.activeTabIndex,
                    ),
            ),
          ],
        ),
      ),
      bottomNavigationBar: BrowserToolbar(
        canGoBack: activeTab?.canGoBack ?? false,
        canGoForward: activeTab?.canGoForward ?? false,
        tabCount: browser.tabs.length,
        onBack: () => browser.goBack(),
        onForward: () => browser.goForward(),
        onReload: () => browser.reload(),
        onNewTab: () => browser.newTab(),
        onOpenTabs: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => TabsScreen(onClose: () => Navigator.pop(context)),
            ),
          );
        },
        onOpenMenu: () {
          showModalBottomSheet(
            context: context,
            builder: (ctx) => SafeArea(
              child: Wrap(
                children: [
                  ListTile(
                    leading: const Icon(Icons.shield_outlined),
                    title: const Text('Privacy & Security'),
                    onTap: () {
                      Navigator.pop(ctx);
                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (_) => const PrivacySettingsScreen()),
                      );
                    },
                  ),
                  ListTile(
                    leading: const Icon(Icons.download),
                    title: const Text('Downloads'),
                    onTap: () {
                      Navigator.pop(ctx);
                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (_) => const DownloadsScreen()),
                      );
                    },
                  ),
                  ListTile(
                    leading: const Icon(Icons.settings),
                    title: const Text('Settings'),
                    onTap: () {
                      Navigator.pop(ctx);
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) => SettingsScreen(
                            onOpenPrivacy: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(builder: (_) => const PrivacySettingsScreen()),
                              );
                            },
                            onOpenDownloads: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(builder: (_) => const DownloadsScreen()),
                              );
                            },
                          ),
                        ),
                      );
                    },
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
