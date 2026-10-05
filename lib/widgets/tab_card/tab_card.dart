import 'package:flutter/material.dart';
import '../../models/browser_tab.dart';
import '../../theme/app_theme.dart';
import '../../browser/browser_controller.dart';

class TabCard extends StatelessWidget {
  final BrowserTab tab;
  final bool isActive;
  final VoidCallback onTap;
  final VoidCallback onClose;

  const TabCard({
    super.key,
    required this.tab,
    required this.isActive,
    required this.onTap,
    required this.onClose,
  });

  @override
  Widget build(BuildContext context) {
    final displayDomain = BrowserController.formatDisplayUrl(tab.url);

    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(16),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        decoration: BoxDecoration(
          color: isActive ? AppTheme.surfaceLight : AppTheme.surface,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(
            color: isActive ? AppTheme.flameOrange : AppTheme.border,
            width: isActive ? 2.0 : 1.0,
          ),
          boxShadow: isActive
              ? [
                  BoxShadow(
                    color: AppTheme.flameOrange.withValues(alpha: 0.2),
                    blurRadius: 10,
                    offset: const Offset(0, 4),
                  )
                ]
              : [],
        ),
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header: Title & Close button
            Row(
              children: [
                Icon(
                  tab.url == 'firezip://home' ? Icons.local_fire_department_rounded : Icons.public_rounded,
                  size: 16,
                  color: isActive ? AppTheme.flameOrange : AppTheme.zipCyan,
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    tab.title.isEmpty ? 'New Tab' : tab.title,
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: TextStyle(
                      color: AppTheme.textPrimary,
                      fontWeight: isActive ? FontWeight.w700 : FontWeight.w500,
                      fontSize: 14,
                    ),
                  ),
                ),
                IconButton(
                  padding: EdgeInsets.zero,
                  constraints: const BoxConstraints(minWidth: 28, minHeight: 28),
                  icon: const Icon(Icons.close_rounded, size: 18, color: AppTheme.textSecondary),
                  onPressed: onClose,
                ),
              ],
            ),
            const SizedBox(height: 12),
            // Preview card area
            Expanded(
              child: Container(
                width: double.infinity,
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: AppTheme.background,
                  borderRadius: BorderRadius.circular(10),
                  border: Border.all(color: AppTheme.border.withValues(alpha: 0.5)),
                ),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(
                      Icons.shield_moon_outlined,
                      size: 28,
                      color: AppTheme.zipCyan.withValues(alpha: 0.8),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      displayDomain,
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                      style: const TextStyle(
                        color: AppTheme.textSecondary,
                        fontSize: 12,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                    const SizedBox(height: 4),
                    const Text(
                      'Temporary Session Active',
                      style: TextStyle(color: AppTheme.textMuted, fontSize: 10),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
