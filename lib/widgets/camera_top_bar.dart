import 'package:flutter/material.dart';
import '../providers/settings_provider.dart';
import '../theme/app_theme.dart';

class CameraTopBar extends StatelessWidget {
  final SettingsProvider settings;
  final VoidCallback onSwitchCamera;
  final VoidCallback onOpenSettings;
  final VoidCallback onOpenPremium;

  const CameraTopBar({
    super.key,
    required this.settings,
    required this.onSwitchCamera,
    required this.onOpenSettings,
    required this.onOpenPremium,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      color: Colors.transparent,
      child: SafeArea(
        bottom: false,
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            // Settings Button
            IconButton(
              icon: const Icon(Icons.settings, color: Colors.white),
              onPressed: onOpenSettings,
              tooltip: 'Settings',
            ),

            // Center Actions Group (Flash, Grid, Timer)
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
              decoration: BoxDecoration(
                color: Colors.black.withOpacity(0.4),
                borderRadius: BorderRadius.circular(24),
              ),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  // Flash Toggle
                  IconButton(
                    icon: Icon(
                      _getFlashIcon(settings.flashMode),
                      color: settings.flashMode != FlashMode.off
                          ? AppTheme.primaryYellow
                          : Colors.white,
                    ),
                    onPressed: () => settings.toggleFlashMode(),
                    tooltip: 'Flash',
                  ),

                  // Timer Cycle
                  IconButton(
                    icon: Stack(
                      alignment: Alignment.center,
                      children: [
                        Icon(
                          Icons.timer,
                          color: settings.timerSeconds > 0
                              ? AppTheme.primaryYellow
                              : Colors.white,
                        ),
                        if (settings.timerSeconds > 0)
                          Positioned(
                            right: 0,
                            bottom: 0,
                            child: Text(
                              '${settings.timerSeconds}',
                              style: const TextStyle(
                                fontSize: 10,
                                fontWeight: FontWeight.bold,
                                color: AppTheme.primaryYellow,
                              ),
                            ),
                          ),
                      ],
                    ),
                    onPressed: () => settings.cycleTimer(),
                    tooltip: 'Timer',
                  ),

                  // Grid Toggle
                  IconButton(
                    icon: Icon(
                      Icons.grid_on,
                      color: settings.gridEnabled
                          ? AppTheme.primaryYellow
                          : Colors.white.withOpacity(0.6),
                    ),
                    onPressed: () => settings.toggleGrid(),
                    tooltip: 'Grid',
                  ),
                ],
              ),
            ),

            // Right Group: Premium & Camera Switch
            Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                // Premium Upgrade Badge Button
                IconButton(
                  icon: Container(
                    padding: const EdgeInsets.all(4),
                    decoration: const BoxDecoration(
                      color: AppTheme.primaryYellow,
                      shape: BoxShape.circle,
                    ),
                    child: const Icon(
                      Icons.workspace_premium,
                      color: Colors.black,
                      size: 18,
                    ),
                  ),
                  onPressed: onOpenPremium,
                  tooltip: 'Premium',
                ),

                // Switch Camera
                IconButton(
                  icon: const Icon(Icons.flip_camera_ios, color: Colors.white),
                  onPressed: onSwitchCamera,
                  tooltip: 'Switch Camera',
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  IconData _getFlashIcon(FlashMode mode) {
    switch (mode) {
      case FlashMode.off:
        return Icons.flash_off;
      case FlashMode.auto:
        return Icons.flash_auto;
      case FlashMode.on:
        return Icons.flash_on;
      case FlashMode.torch:
        return Icons.highlight;
    }
  }
}
