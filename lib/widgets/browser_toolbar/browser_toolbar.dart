import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';
import '../../models/browser_tab.dart';

class MobileBottomToolbar extends StatelessWidget {
  final bool canGoBack;
  final bool canGoForward;
  final int tabCount;
  final VoidCallback onGoBack;
  final VoidCallback onGoForward;
  final VoidCallback onReload;
  final VoidCallback onNewTab;
  final VoidCallback onOpenTabs;
  final VoidCallback onOpenMenu;

  const MobileBottomToolbar({
    super.key,
    required this.canGoBack,
    required this.canGoForward,
    required this.tabCount,
    required this.onGoBack,
    required this.onGoForward,
    required this.onReload,
    required this.onNewTab,
    required this.onOpenTabs,
    required this.onOpenMenu,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 56,
      decoration: const BoxDecoration(
        color: AppTheme.surface,
        border: Border(top: BorderSide(color: AppTheme.border, width: 1)),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          IconButton(
            icon: const Icon(Icons.arrow_back_ios_new_rounded, size: 20),
            color: canGoBack ? AppTheme.textPrimary : AppTheme.textMuted,
            onPressed: canGoBack ? onGoBack : null,
            tooltip: 'Back',
          ),
          IconButton(
            icon: const Icon(Icons.arrow_forward_ios_rounded, size: 20),
            color: canGoForward ? AppTheme.textPrimary : AppTheme.textMuted,
            onPressed: canGoForward ? onGoForward : null,
            tooltip: 'Forward',
          ),
          IconButton(
            icon: const Icon(Icons.refresh_rounded, size: 22),
            color: AppTheme.textPrimary,
            onPressed: onReload,
            tooltip: 'Reload',
          ),
          IconButton(
            icon: const Icon(Icons.add_circle_outline_rounded, size: 24),
            color: AppTheme.flameOrange,
            onPressed: onNewTab,
            tooltip: 'New Tab',
          ),
          InkWell(
            onTap: onOpenTabs,
            borderRadius: BorderRadius.circular(8),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
              decoration: BoxDecoration(
                border: Border.all(color: AppTheme.zipCyan, width: 1.5),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Text(
                '$tabCount',
                style: const TextStyle(
                  color: AppTheme.zipCyan,
                  fontWeight: FontWeight.w800,
                  fontSize: 13,
                ),
              ),
            ),
          ),
          IconButton(
            icon: const Icon(Icons.menu_rounded, size: 24),
            color: AppTheme.textPrimary,
            onPressed: onOpenMenu,
            tooltip: 'Menu',
          ),
        ],
      ),
    );
  }
}

class DesktopHeaderTabBar extends StatelessWidget {
  final List<BrowserTab> tabs;
  final int activeIndex;
  final ValueChanged<int> onSelectTab;
  final ValueChanged<String> onCloseTab;
  final VoidCallback onNewTab;

  const DesktopHeaderTabBar({
    super.key,
    required this.tabs,
    required this.activeIndex,
    required this.onSelectTab,
    required this.onCloseTab,
    required this.onNewTab,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 40,
      color: AppTheme.background,
      child: Row(
        children: [
          Expanded(
            child: ListView.builder(
              scrollDirection: Axis.horizontal,
              itemCount: tabs.length,
              itemBuilder: (context, index) {
                final tab = tabs[index];
                final isActive = index == activeIndex;
                return Container(
                  width: 180,
                  margin: const EdgeInsets.only(right: 2, top: 4),
                  decoration: BoxDecoration(
                    color: isActive ? AppTheme.surface : AppTheme.surfaceLight.withValues(alpha: 0.5),
                    borderRadius: const BorderRadius.vertical(top: Radius.circular(8)),
                    border: Border(
                      top: BorderSide(
                        color: isActive ? AppTheme.flameOrange : Colors.transparent,
                        width: 2,
                      ),
                    ),
                  ),
                  child: InkWell(
                    onTap: () => onSelectTab(index),
                    child: Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 10),
                      child: Row(
                        children: [
                          Icon(
                            tab.url == 'firezip://home' ? Icons.local_fire_department_rounded : Icons.public_rounded,
                            size: 14,
                            color: isActive ? AppTheme.flameOrange : AppTheme.textSecondary,
                          ),
                          const SizedBox(width: 8),
                          Expanded(
                            child: Text(
                              tab.title.isEmpty ? 'New Tab' : tab.title,
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                              style: TextStyle(
                                color: isActive ? AppTheme.textPrimary : AppTheme.textSecondary,
                                fontSize: 13,
                                fontWeight: isActive ? FontWeight.w600 : FontWeight.w400,
                              ),
                            ),
                          ),
                          InkWell(
                            onTap: () => onCloseTab(tab.id),
                            borderRadius: BorderRadius.circular(10),
                            child: const Padding(
                              padding: EdgeInsets.all(2.0),
                              child: Icon(Icons.close_rounded, size: 14, color: AppTheme.textMuted),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
          IconButton(
            icon: const Icon(Icons.add_rounded, size: 20, color: AppTheme.flameOrange),
            onPressed: onNewTab,
            tooltip: 'New Tab',
          ),
        ],
      ),
    );
  }
}
