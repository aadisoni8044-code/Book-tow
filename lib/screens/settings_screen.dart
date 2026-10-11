import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../providers/settings_provider.dart';
import '../theme/app_colors.dart';
import '../widgets/zipgram_logo.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final settings = context.watch<SettingsProvider>();

    return Scaffold(
      backgroundColor: AppColors.darkBackground,
      appBar: AppBar(
        title: const Text('Zipgram Settings'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => Navigator.of(context).pop(),
        ),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Center(
                child: Padding(
                  padding: EdgeInsets.symmetric(vertical: 16),
                  child: ZipgramLogo(height: 40),
                ),
              ),

              const SizedBox(height: 16),

              // Image Quality Settings
              const Text(
                'CAMERA & CAPTURE',
                style: TextStyle(
                  color: AppColors.primaryBlueLight,
                  fontSize: 12,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 1.2,
                ),
              ),
              const SizedBox(height: 10),

              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    children: [
                      // Photo Quality
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: const [
                              Text(
                                'Photo Export Quality',
                                style: TextStyle(
                                  fontSize: 16,
                                  fontWeight: FontWeight.w600,
                                  color: Colors.white,
                                ),
                              ),
                              SizedBox(height: 4),
                              Text(
                                'Higher quality results in larger file size',
                                style: TextStyle(
                                  fontSize: 12,
                                  color: AppColors.textSecondary,
                                ),
                              ),
                            ],
                          ),
                          DropdownButton<int>(
                            value: settings.photoQuality,
                            dropdownColor: AppColors.darkSurface,
                            underline: const SizedBox(),
                            style: const TextStyle(
                              color: AppColors.primaryBlueLight,
                              fontWeight: FontWeight.bold,
                            ),
                            items: const [
                              DropdownMenuItem(value: 70, child: Text('70% (Medium)')),
                              DropdownMenuItem(value: 90, child: Text('90% (High)')),
                              DropdownMenuItem(value: 100, child: Text('100% (Max)')),
                            ],
                            onChanged: (val) {
                              if (val != null) settings.setPhotoQuality(val);
                            },
                          ),
                        ],
                      ),
                      const Divider(color: AppColors.inactiveBorder, height: 24),

                      // Default Flash Mode
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text(
                            'Default Flash Mode',
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.w600,
                              color: Colors.white,
                            ),
                          ),
                          DropdownButton<String>(
                            value: settings.defaultFlash,
                            dropdownColor: AppColors.darkSurface,
                            underline: const SizedBox(),
                            style: const TextStyle(
                              color: AppColors.primaryBlueLight,
                              fontWeight: FontWeight.bold,
                            ),
                            items: const [
                              DropdownMenuItem(value: 'off', child: Text('Off')),
                              DropdownMenuItem(value: 'always', child: Text('Always On')),
                              DropdownMenuItem(value: 'auto', child: Text('Auto')),
                            ],
                            onChanged: (val) {
                              if (val != null) settings.setDefaultFlash(val);
                            },
                          ),
                        ],
                      ),
                      const Divider(color: AppColors.inactiveBorder, height: 24),

                      // Preferred Camera
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text(
                            'Preferred Camera',
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.w600,
                              color: Colors.white,
                            ),
                          ),
                          DropdownButton<String>(
                            value: settings.preferredCamera,
                            dropdownColor: AppColors.darkSurface,
                            underline: const SizedBox(),
                            style: const TextStyle(
                              color: AppColors.primaryBlueLight,
                              fontWeight: FontWeight.bold,
                            ),
                            items: const [
                              DropdownMenuItem(value: 'rear', child: Text('Rear Camera')),
                              DropdownMenuItem(value: 'front', child: Text('Front Camera')),
                            ],
                            onChanged: (val) {
                              if (val != null) settings.setPreferredCamera(val);
                            },
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),

              const SizedBox(height: 24),

              // Privacy Section
              const Text(
                'PRIVACY & LOCAL FIRST',
                style: TextStyle(
                  color: AppColors.primaryBlueLight,
                  fontSize: 12,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 1.2,
                ),
              ),
              const SizedBox(height: 10),

              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: const [
                      Row(
                        children: [
                          Icon(Icons.shield, color: AppColors.primaryBlue),
                          SizedBox(width: 10),
                          Text(
                            'Local-First Camera Application',
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                              color: Colors.white,
                            ),
                          ),
                        ],
                      ),
                      SizedBox(height: 12),
                      Text(
                        '• No Account Required: Zipgram requires zero registration or personal details.\n'
                        '• Local Storage: Photos are saved directly on your phone.\n'
                        '• Zero Data Collection: Zipgram does not upload, track, or collect your photos.\n'
                        '• Native Sharing: Photos are shared strictly through your phone\'s native Android share sheet.',
                        style: TextStyle(
                          fontSize: 13,
                          color: AppColors.textSecondary,
                          height: 1.5,
                        ),
                      ),
                    ],
                  ),
                ),
              ),

              const SizedBox(height: 24),

              // App Version Information
              Card(
                child: ListTile(
                  title: const Text(
                    'App Version',
                    style: TextStyle(color: Colors.white, fontWeight: FontWeight.w600),
                  ),
                  trailing: const Text(
                    '1.0.0 (Build 1)',
                    style: TextStyle(color: AppColors.textSecondary),
                  ),
                  leading: const Icon(Icons.info_outline, color: AppColors.primaryBlue),
                ),
              ),

              const SizedBox(height: 32),

              // Return to Camera Button
              SizedBox(
                width: double.infinity,
                height: 52,
                child: ElevatedButton.icon(
                  onPressed: () => Navigator.of(context).pop(),
                  icon: const Icon(Icons.camera_alt),
                  label: const Text('Return to Camera'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
