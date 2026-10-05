import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/settings_provider.dart';
import '../widgets/firezip_logo.dart';
import '../widgets/private_badge.dart';
import '../theme/firezip_colors.dart';

class HomeScreen extends StatelessWidget {
  final Function(String) onSearch;
  final VoidCallback onOpenTabs;
  final VoidCallback onOpenDownloads;
  final VoidCallback onOpenSettings;

  const HomeScreen({
    super.key,
    required this.onSearch,
    required this.onOpenTabs,
    required this.onOpenDownloads,
    required this.onOpenSettings,
  });

  @override
  Widget build(BuildContext context) {
    final settings = Provider.of<SettingsProvider>(context);
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final controller = TextEditingController();

    return SingleChildScrollView(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 32),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          const SizedBox(height: 20),
          const FireZipLogo(size: 80, fontSize: 32),
          const SizedBox(height: 16),
          const PrivateBadge(),
          const SizedBox(height: 32),

          // Search input
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
            decoration: BoxDecoration(
              color: isDark ? FireZipColors.darkSurface : FireZipColors.lightSurface,
              borderRadius: BorderRadius.circular(30),
              border: Border.all(
                color: isDark ? FireZipColors.darkBorder : FireZipColors.lightBorder,
                width: 1.5,
              ),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withValues(alpha: 0.1),
                  blurRadius: 10,
                  offset: const Offset(0, 4),
                ),
              ],
            ),
            child: Row(
              children: [
                const Icon(Icons.search, color: FireZipColors.flameOrange),
                const SizedBox(width: 12),
                Expanded(
                  child: TextField(
                    controller: controller,
                    textInputAction: TextInputAction.search,
                    decoration: const InputDecoration(
                      hintText: 'Search or enter website address',
                      border: InputBorder.none,
                    ),
                    onSubmitted: (val) {
                      if (val.trim().isNotEmpty) {
                        onSearch(val.trim());
                      }
                    },
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.arrow_forward),
                  color: FireZipColors.zipYellow,
                  onPressed: () {
                    if (controller.text.trim().isNotEmpty) {
                      onSearch(controller.text.trim());
                    }
                  },
                ),
              ],
            ),
          ),

          const SizedBox(height: 40),

          // Search Engine Shortcuts
          Align(
            alignment: Alignment.centerLeft,
            child: Text(
              'Quick Search',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
                color: isDark ? FireZipColors.textSecondaryDark : FireZipColors.textSecondaryLight,
              ),
            ),
          ),
          const SizedBox(height: 16),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              _buildShortcutItem(
                context,
                icon: Icons.search,
                label: settings.selectedSearchEngine.name,
                color: FireZipColors.flameOrange,
                onTap: () => onSearch(settings.selectedSearchEngine.homeUrl),
              ),
              _buildShortcutItem(
                context,
                icon: Icons.tab,
                label: 'Tabs',
                color: Colors.blue,
                onTap: onOpenTabs,
              ),
              _buildShortcutItem(
                context,
                icon: Icons.download_rounded,
                label: 'Downloads',
                color: Colors.green,
                onTap: onOpenDownloads,
              ),
              _buildShortcutItem(
                context,
                icon: Icons.shield_outlined,
                label: 'Settings',
                color: FireZipColors.privatePurple,
                onTap: onOpenSettings,
              ),
            ],
          ),

          const SizedBox(height: 48),

          // Privacy Banner Info
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: isDark ? FireZipColors.darkCard : FireZipColors.lightCard,
              borderRadius: BorderRadius.circular(16),
            ),
            child: Column(
              children: [
                const Row(
                  children: [
                    Icon(Icons.security, color: FireZipColors.flameOrange),
                    SizedBox(width: 8),
                    Text(
                      'Automatic Session Cleanup',
                      style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                Text(
                  'FireZip automatically wipes temporary tab session data, cookies, and cache when you close tabs or exit the browser.',
                  style: TextStyle(
                    fontSize: 13,
                    color: isDark ? FireZipColors.textSecondaryDark : FireZipColors.textSecondaryLight,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildShortcutItem(
    BuildContext context, {
    required IconData icon,
    required String label,
    required Color color,
    required VoidCallback onTap,
  }) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return GestureDetector(
      onTap: onTap,
      child: Column(
        children: [
          Container(
            width: 56,
            height: 56,
            decoration: BoxDecoration(
              color: color.withValues(alpha: 0.15),
              shape: BoxShape.circle,
              border: Border.all(color: color.withValues(alpha: 0.3)),
            ),
            child: Icon(icon, color: color, size: 28),
          ),
          const SizedBox(height: 8),
          Text(
            label,
            style: TextStyle(
              fontSize: 12,
              fontWeight: FontWeight.w500,
              color: isDark ? FireZipColors.textPrimaryDark : FireZipColors.textPrimaryLight,
            ),
          ),
        ],
      ),
    );
  }
}
