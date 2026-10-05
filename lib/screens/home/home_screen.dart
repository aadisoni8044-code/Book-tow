import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';
import '../../widgets/logo/firezip_logo.dart';

class HomeScreen extends StatefulWidget {
  final ValueChanged<String> onNavigate;
  final VoidCallback onOpenSettings;
  final VoidCallback onOpenDownloads;
  final VoidCallback onOpenTabs;

  const HomeScreen({
    super.key,
    required this.onNavigate,
    required this.onOpenSettings,
    required this.onOpenDownloads,
    required this.onOpenTabs,
  });

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final TextEditingController _searchController = TextEditingController();

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  void _handleSearch() {
    final query = _searchController.text.trim();
    if (query.isNotEmpty) {
      widget.onNavigate(query);
    }
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    final isDesktop = size.width > 700;

    return SingleChildScrollView(
      padding: EdgeInsets.symmetric(
        horizontal: isDesktop ? size.width * 0.2 : 24,
        vertical: 40,
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          const SizedBox(height: 20),
          // Logo
          const FireZipLogo(size: 90, showText: true, animate: true),
          const SizedBox(height: 32),

          // Private Session Indicator Badge
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            decoration: BoxDecoration(
              color: AppTheme.surfaceLight,
              borderRadius: BorderRadius.circular(20),
              border: Border.all(color: AppTheme.privacyGreen.withValues(alpha: 0.5)),
            ),
            child: const Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(Icons.shield_rounded, size: 16, color: AppTheme.privacyGreen),
                SizedBox(width: 8),
                Flexible(
                  child: Text(
                    'Private Session Active • Data cleared on exit',
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: TextStyle(
                      color: AppTheme.privacyGreen,
                      fontWeight: FontWeight.w600,
                      fontSize: 12,
                    ),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 32),

          // Search / Address Bar Input
          Container(
            decoration: BoxDecoration(
              color: AppTheme.surface,
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: AppTheme.border, width: 1.5),
              boxShadow: [
                BoxShadow(
                  color: AppTheme.flameOrange.withValues(alpha: 0.1),
                  blurRadius: 20,
                  offset: const Offset(0, 8),
                )
              ],
            ),
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
            child: Row(
              children: [
                const Icon(Icons.search_rounded, color: AppTheme.flameOrange, size: 24),
                const SizedBox(width: 12),
                Expanded(
                  child: TextField(
                    controller: _searchController,
                    textInputAction: TextInputAction.search,
                    style: const TextStyle(color: AppTheme.textPrimary, fontSize: 16),
                    decoration: const InputDecoration(
                      hintText: 'Search or enter website',
                      hintStyle: TextStyle(color: AppTheme.textMuted, fontSize: 16),
                      border: InputBorder.none,
                      enabledBorder: InputBorder.none,
                      focusedBorder: InputBorder.none,
                      contentPadding: EdgeInsets.symmetric(vertical: 14),
                    ),
                    onSubmitted: (_) => _handleSearch(),
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.arrow_forward_rounded, color: AppTheme.zipCyan),
                  onPressed: _handleSearch,
                  tooltip: 'Go',
                ),
              ],
            ),
          ),
          const SizedBox(height: 40),

          // Quick Action Cards
          Wrap(
            spacing: 16,
            runSpacing: 16,
            alignment: WrapAlignment.center,
            children: [
              _QuickActionButton(
                icon: Icons.add_rounded,
                label: 'New Tab',
                accentColor: AppTheme.flameOrange,
                onTap: () => widget.onNavigate('firezip://home'),
              ),
              _QuickActionButton(
                icon: Icons.tab_rounded,
                label: 'Tabs',
                accentColor: AppTheme.zipCyan,
                onTap: widget.onOpenTabs,
              ),
              _QuickActionButton(
                icon: Icons.download_rounded,
                label: 'Downloads',
                accentColor: AppTheme.textPrimary,
                onTap: widget.onOpenDownloads,
              ),
              _QuickActionButton(
                icon: Icons.security_rounded,
                label: 'Settings',
                accentColor: AppTheme.privacyGreen,
                onTap: widget.onOpenSettings,
              ),
            ],
          ),
          const SizedBox(height: 48),

          // Fast Search Suggestions
          const Text(
            'PRIVACY QUICK SEARCH',
            style: TextStyle(
              color: AppTheme.textMuted,
              fontSize: 11,
              fontWeight: FontWeight.w700,
              letterSpacing: 1.5,
            ),
          ),
          const SizedBox(height: 16),
          Wrap(
            spacing: 10,
            runSpacing: 10,
            alignment: WrapAlignment.center,
            children: [
              _SearchChip(label: 'Wikipedia', query: 'https://wikipedia.org', onTap: widget.onNavigate),
              _SearchChip(label: 'DuckDuckGo', query: 'https://duckduckgo.com', onTap: widget.onNavigate),
              _SearchChip(label: 'GitHub', query: 'https://github.com', onTap: widget.onNavigate),
              _SearchChip(label: 'Archive.org', query: 'https://archive.org', onTap: widget.onNavigate),
            ],
          ),
        ],
      ),
    );
  }
}

class _QuickActionButton extends StatelessWidget {
  final IconData icon;
  final String label;
  final Color accentColor;
  final VoidCallback onTap;

  const _QuickActionButton({
    required this.icon,
    required this.label,
    required this.accentColor,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(16),
      child: Container(
        width: 100,
        padding: const EdgeInsets.symmetric(vertical: 16),
        decoration: BoxDecoration(
          color: AppTheme.surface,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: AppTheme.border),
        ),
        child: Column(
          children: [
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: accentColor.withValues(alpha: 0.15),
                shape: BoxShape.circle,
              ),
              child: Icon(icon, color: accentColor, size: 22),
            ),
            const SizedBox(height: 10),
            Text(
              label,
              style: const TextStyle(
                color: AppTheme.textPrimary,
                fontSize: 13,
                fontWeight: FontWeight.w600,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _SearchChip extends StatelessWidget {
  final String label;
  final String query;
  final ValueChanged<String> onTap;

  const _SearchChip({
    required this.label,
    required this.query,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return ActionChip(
      backgroundColor: AppTheme.surfaceLight,
      side: const BorderSide(color: AppTheme.border),
      label: Text(label, style: const TextStyle(color: AppTheme.textSecondary, fontSize: 13)),
      onPressed: () => onTap(query),
    );
  }
}
