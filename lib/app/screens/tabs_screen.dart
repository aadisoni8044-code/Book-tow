import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/browser_provider.dart';
import '../theme/firezip_colors.dart';
import '../widgets/private_badge.dart';

class TabsScreen extends StatelessWidget {
  final VoidCallback onClose;

  const TabsScreen({super.key, required this.onClose});

  @override
  Widget build(BuildContext context) {
    final browser = Provider.of<BrowserProvider>(context);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Tabs Manager'),
        actions: [
          TextButton.icon(
            onPressed: () {
              browser.closeAllTabs();
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Closed all tabs and wiped temporary session data.')),
              );
            },
            icon: const Icon(Icons.delete_sweep, color: FireZipColors.flameOrange),
            label: const Text(
              'Close All',
              style: TextStyle(color: FireZipColors.flameOrange),
            ),
          ),
        ],
      ),
      body: Column(
        children: [
          const Padding(
            padding: EdgeInsets.symmetric(vertical: 8.0),
            child: PrivateBadge(),
          ),
          Expanded(
            child: GridView.builder(
              padding: const EdgeInsets.all(16),
              gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
                maxCrossAxisExtent: 220,
                childAspectRatio: 0.85,
                crossAxisSpacing: 16,
                mainAxisSpacing: 16,
              ),
              itemCount: browser.tabs.length,
              itemBuilder: (context, index) {
                final tab = browser.tabs[index];
                final isSelected = index == browser.activeTabIndex;

                return GestureDetector(
                  onTap: () {
                    browser.selectTab(index);
                    onClose();
                  },
                  child: Container(
                    decoration: BoxDecoration(
                      color: isDark ? FireZipColors.darkCard : FireZipColors.lightCard,
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(
                        color: isSelected
                            ? FireZipColors.flameOrange
                            : (isDark ? FireZipColors.darkBorder : FireZipColors.lightBorder),
                        width: isSelected ? 2 : 1,
                      ),
                      boxShadow: isSelected
                          ? [
                              BoxShadow(
                                color: FireZipColors.flameOrange.withValues(alpha: 0.3),
                                blurRadius: 8,
                              )
                            ]
                          : null,
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        // Card Header
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                          decoration: BoxDecoration(
                            color: isDark ? FireZipColors.darkSurface : FireZipColors.lightSurface,
                            borderRadius: const BorderRadius.vertical(top: Radius.circular(15)),
                          ),
                          child: Row(
                            children: [
                              Icon(
                                tab.isSecure ? Icons.lock : Icons.lock_open,
                                size: 14,
                                color: tab.isSecure ? Colors.green : Colors.orange,
                              ),
                              const SizedBox(width: 6),
                              Expanded(
                                child: Text(
                                  tab.title,
                                  maxLines: 1,
                                  overflow: TextOverflow.ellipsis,
                                  style: const TextStyle(
                                    fontSize: 12,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ),
                              GestureDetector(
                                onTap: () => browser.closeTab(index),
                                child: const Icon(Icons.close, size: 18),
                              ),
                            ],
                          ),
                        ),
                        // Preview Body
                        Expanded(
                          child: Container(
                            padding: const EdgeInsets.all(12),
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Icon(
                                  Icons.web,
                                  size: 40,
                                  color: isSelected ? FireZipColors.flameOrange : Colors.grey,
                                ),
                                const SizedBox(height: 8),
                                Text(
                                  tab.url,
                                  maxLines: 2,
                                  overflow: TextOverflow.ellipsis,
                                  textAlign: TextAlign.center,
                                  style: const TextStyle(fontSize: 11, color: Colors.grey),
                                ),
                              ],
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {
          browser.newTab();
          onClose();
        },
        backgroundColor: FireZipColors.flameOrange,
        icon: const Icon(Icons.add, color: Colors.white),
        label: const Text('New Tab', style: TextStyle(color: Colors.white)),
      ),
    );
  }
}
