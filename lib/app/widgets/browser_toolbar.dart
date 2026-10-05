import 'package:flutter/material.dart';
import '../theme/firezip_colors.dart';

class BrowserToolbar extends StatelessWidget {
  final bool canGoBack;
  final bool canGoForward;
  final int tabCount;
  final VoidCallback onBack;
  final VoidCallback onForward;
  final VoidCallback onReload;
  final VoidCallback onNewTab;
  final VoidCallback onOpenTabs;
  final VoidCallback onOpenMenu;

  const BrowserToolbar({
    super.key,
    required this.canGoBack,
    required this.canGoForward,
    required this.tabCount,
    required this.onBack,
    required this.onForward,
    required this.onReload,
    required this.onNewTab,
    required this.onOpenTabs,
    required this.onOpenMenu,
  });

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Container(
      height: 56,
      decoration: BoxDecoration(
        color: isDark ? FireZipColors.darkSurface : FireZipColors.lightSurface,
        border: Border(
          top: BorderSide(
            color: isDark ? FireZipColors.darkBorder : FireZipColors.lightBorder,
            width: 1,
          ),
        ),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          IconButton(
            icon: const Icon(Icons.arrow_back),
            onPressed: canGoBack ? onBack : null,
          ),
          IconButton(
            icon: const Icon(Icons.arrow_forward),
            onPressed: canGoForward ? onForward : null,
          ),
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: onReload,
          ),
          IconButton(
            icon: const Icon(Icons.add_box_outlined, color: FireZipColors.flameOrange),
            onPressed: onNewTab,
          ),
          Stack(
            alignment: Alignment.center,
            children: [
              IconButton(
                icon: const Icon(Icons.filter_none),
                onPressed: onOpenTabs,
              ),
              Positioned(
                child: IgnorePointer(
                  child: Text(
                    '$tabCount',
                    style: TextStyle(
                      fontSize: 11,
                      fontWeight: FontWeight.bold,
                      color: isDark ? Colors.white : Colors.black,
                    ),
                  ),
                ),
              ),
            ],
          ),
          IconButton(
            icon: const Icon(Icons.more_vert),
            onPressed: onOpenMenu,
          ),
        ],
      ),
    );
  }
}
