import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../providers/camera_provider.dart';
import '../providers/settings_provider.dart';
import '../theme/app_theme.dart';
import 'premium_screen.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.darkBackground,
      appBar: AppBar(
        title: const Text('Camera Settings'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => Navigator.of(context).pop(),
        ),
      ),
      body: Consumer2<SettingsProvider, CameraProvider>(
        builder: (context, settings, camera, child) {
          return ListView(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            children: [
              // Premium Banner Card
              GestureDetector(
                onTap: () {
                  Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (_) => const PremiumScreen(),
                    ),
                  );
                },
                child: Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    gradient: const LinearGradient(
                      colors: [Color(0xFF2D2500), Color(0xFF1A1700)],
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                    ),
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: AppTheme.primaryYellow.withOpacity(0.5)),
                  ),
                  child: Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.all(10),
                        decoration: const BoxDecoration(
                          color: AppTheme.primaryYellow,
                          shape: BoxShape.circle,
                        ),
                        child: const Icon(
                          Icons.workspace_premium,
                          color: Colors.black,
                          size: 24,
                        ),
                      ),
                      const SizedBox(width: 14),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              settings.isPremiumUser
                                  ? 'SnapCam Premium Active'
                                  : 'Unlock SnapCam Premium',
                              style: const TextStyle(
                                color: AppTheme.primaryYellow,
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            const SizedBox(height: 2),
                            Text(
                              settings.isPremiumUser
                                  ? 'Enjoy unlimited exclusive filters & Pro tools'
                                  : 'Access 20+ exclusive filters, 4K export & Pro controls',
                              style: const TextStyle(
                                color: AppTheme.textSecondary,
                                fontSize: 12,
                              ),
                            ),
                          ],
                        ),
                      ),
                      const Icon(
                        Icons.chevron_right,
                        color: AppTheme.primaryYellow,
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 24),

              // Section 1: Camera Controls
              const Padding(
                padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                child: Text(
                  'CAMERA CONTROLS',
                  style: TextStyle(
                    color: AppTheme.primaryYellow,
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 1.2,
                  ),
                ),
              ),
              Card(
                color: AppTheme.cardDark,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Column(
                  children: [
                    // Flash Mode Selector
                    ListTile(
                      leading: const Icon(Icons.flash_on, color: Colors.white),
                      title: const Text('Flash Mode'),
                      subtitle: Text(
                        settings.flashMode.name.toUpperCase(),
                        style: const TextStyle(color: AppTheme.textSecondary),
                      ),
                      trailing: DropdownButton<FlashMode>(
                        value: settings.flashMode,
                        dropdownColor: AppTheme.cardDark,
                        style: const TextStyle(color: AppTheme.primaryYellow, fontWeight: FontWeight.bold),
                        underline: const SizedBox(),
                        items: FlashMode.values.map((mode) {
                          return DropdownMenuItem(
                            value: mode,
                            child: Text(mode.name.toUpperCase()),
                          );
                        }).toList(),
                        onChanged: (mode) {
                          if (mode != null) {
                            settings.setFlashMode(mode);
                            camera.updateFlashMode(mode);
                          }
                        },
                      ),
                    ),
                    const Divider(height: 1, color: Colors.white10),

                    // Grid Overlay Switch
                    SwitchListTile(
                      activeColor: AppTheme.primaryYellow,
                      secondary: const Icon(Icons.grid_on, color: Colors.white),
                      title: const Text('Grid Overlay'),
                      subtitle: const TextStyle(color: AppTheme.textSecondary) != null
                          ? const Text('3x3 composition grid', style: TextStyle(color: AppTheme.textSecondary, fontSize: 12))
                          : null,
                      value: settings.gridEnabled,
                      onChanged: (val) => settings.toggleGrid(),
                    ),
                    const Divider(height: 1, color: Colors.white10),

                    // Timer Selector
                    ListTile(
                      leading: const Icon(Icons.timer, color: Colors.white),
                      title: const Text('Capture Timer'),
                      subtitle: Text(
                        settings.timerSeconds == 0
                            ? 'Off'
                            : '${settings.timerSeconds} Seconds',
                        style: const TextStyle(color: AppTheme.textSecondary),
                      ),
                      trailing: TextButton(
                        onPressed: () => settings.cycleTimer(),
                        child: Text(
                          settings.timerSeconds == 0
                              ? 'OFF'
                              : '${settings.timerSeconds}s',
                          style: const TextStyle(
                            color: AppTheme.primaryYellow,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ),
                    const Divider(height: 1, color: Colors.white10),

                    // Switch Camera Lens
                    ListTile(
                      leading: const Icon(Icons.flip_camera_ios, color: Colors.white),
                      title: const Text('Switch Camera Lens'),
                      subtitle: const Text('Toggle between front and rear cameras', style: TextStyle(color: AppTheme.textSecondary, fontSize: 12)),
                      trailing: const Icon(Icons.chevron_right, color: Colors.white54),
                      onTap: () {
                        camera.switchCamera();
                        Navigator.of(context).pop();
                      },
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 20),

              // Section 2: Photo & Quality Settings
              const Padding(
                padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                child: Text(
                  'PHOTO & SAVE OPTIONS',
                  style: TextStyle(
                    color: AppTheme.primaryYellow,
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 1.2,
                  ),
                ),
              ),
              Card(
                color: AppTheme.cardDark,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Column(
                  children: [
                    // Filter Output Quality
                    ListTile(
                      leading: const Icon(Icons.high_quality, color: Colors.white),
                      title: const Text('Filter Processing Quality'),
                      subtitle: Text(
                        settings.filterQuality.name.toUpperCase(),
                        style: const TextStyle(color: AppTheme.textSecondary),
                      ),
                      trailing: DropdownButton<FilterQuality>(
                        value: settings.filterQuality,
                        dropdownColor: AppTheme.cardDark,
                        style: const TextStyle(color: AppTheme.primaryYellow, fontWeight: FontWeight.bold),
                        underline: const SizedBox(),
                        items: FilterQuality.values.map((q) {
                          return DropdownMenuItem(
                            value: q,
                            child: Text(q.name.toUpperCase()),
                          );
                        }).toList(),
                        onChanged: (q) {
                          if (q != null) settings.setFilterQuality(q);
                        },
                      ),
                    ),
                    const Divider(height: 1, color: Colors.white10),

                    // Auto Save
                    SwitchListTile(
                      activeColor: AppTheme.primaryYellow,
                      secondary: const Icon(Icons.save_alt, color: Colors.white),
                      title: const Text('Auto-Save to Gallery'),
                      subtitle: const Text('Automatically save captured photo to device', style: TextStyle(color: AppTheme.textSecondary, fontSize: 12)),
                      value: settings.autoSaveToGallery,
                      onChanged: (val) => settings.setAutoSave(val),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 20),

              // Section 3: App Info & Credits
              Card(
                color: AppTheme.cardDark,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                ),
                child: const ListTile(
                  leading: Icon(Icons.info_outline, color: Colors.white),
                  title: Text('SnapCam Version'),
                  subtitle: Text('1.0.0 (Build 1)', style: TextStyle(color: AppTheme.textSecondary)),
                ),
              ),
            ],
          );
        },
      ),
    );
  }
}
