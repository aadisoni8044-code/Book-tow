import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../theme/app_theme.dart';
import '../../browser/tab_manager.dart';
import '../../widgets/tab_card/tab_card.dart';

class TabsScreen extends StatelessWidget {
  final VoidCallback onCloseView;

  const TabsScreen({
    super.key,
    required this.onCloseView,
  });

  @override
  Widget build(BuildContext context) {
    final tabManager = Provider.of<TabManager>(context);
    final tabs = tabManager.tabs;
    final activeIndex = tabManager.activeTabIndex;

    return Scaffold(
      backgroundColor: AppTheme.background,
      appBar: AppBar(
        title: Text('Tabs (${tabs.length})'),
        actions: [
          TextButton.icon(
            icon: const Icon(Icons.delete_sweep_rounded, color: AppTheme.flameOrange, size: 20),
            label: const Text(
              'Close All Tabs',
              style: TextStyle(color: AppTheme.flameOrange, fontWeight: FontWeight.w700),
            ),
            onPressed: () async {
              final confirm = await showDialog<bool>(
                context: context,
                builder: (ctx) => AlertDialog(
                  backgroundColor: AppTheme.surface,
                  title: const Text('Close All Tabs?'),
                  content: const Text(
                    'This will close all open temporary tabs and clear all associated session data (cookies, cache, web storage).',
                    style: TextStyle(color: AppTheme.textSecondary),
                  ),
                  actions: [
                    TextButton(
                      child: const Text('Cancel'),
                      onPressed: () => Navigator.of(ctx).pop(false),
                    ),
                    ElevatedButton(
                      style: ElevatedButton.styleFrom(backgroundColor: AppTheme.flameOrange),
                      child: const Text('Close All & Clear Data'),
                      onPressed: () => Navigator.of(ctx).pop(true),
                    ),
                  ],
                ),
              );

              if (confirm == true) {
                await tabManager.closeAllTabs();
                onCloseView();
              }
            },
          ),
          const SizedBox(width: 8),
        ],
      ),
      body: tabs.isEmpty
          ? Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.tab_unselected_rounded, size: 64, color: AppTheme.textMuted),
                  const SizedBox(height: 16),
                  const Text('No Open Tabs', style: TextStyle(color: AppTheme.textSecondary, fontSize: 16)),
                  const SizedBox(height: 24),
                  ElevatedButton.icon(
                    icon: const Icon(Icons.add_rounded),
                    label: const Text('Open New Tab'),
                    onPressed: () {
                      tabManager.addTab();
                      onCloseView();
                    },
                  ),
                ],
              ),
            )
          : LayoutBuilder(
              builder: (context, constraints) {
                final crossAxisCount = constraints.maxWidth > 900 ? 4 : (constraints.maxWidth > 600 ? 3 : 2);
                return GridView.builder(
                  padding: const EdgeInsets.all(16),
                  gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: crossAxisCount,
                    childAspectRatio: 0.85,
                    crossAxisSpacing: 16,
                    mainAxisSpacing: 16,
                  ),
                  itemCount: tabs.length,
                  itemBuilder: (context, index) {
                    final tab = tabs[index];
                    return TabCard(
                      tab: tab,
                      isActive: index == activeIndex,
                      onTap: () {
                        tabManager.selectTabByIndex(index);
                        onCloseView();
                      },
                      onClose: () {
                        tabManager.closeTab(tab.id);
                      },
                    );
                  },
                );
              },
            ),
      floatingActionButton: FloatingActionButton.extended(
        backgroundColor: AppTheme.flameOrange,
        icon: const Icon(Icons.add_rounded, color: Colors.white),
        label: const Text('New Tab', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w700)),
        onPressed: () {
          tabManager.addTab();
          onCloseView();
        },
      ),
    );
  }
}
