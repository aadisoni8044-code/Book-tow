import 'package:flutter/material.dart';
import 'package:permission_handler/permission_handler.dart';

import '../theme/app_colors.dart';
import '../widgets/zipgram_logo.dart';
import 'camera_screen.dart';

class PermissionScreen extends StatefulWidget {
  const PermissionScreen({super.key});

  @override
  State<PermissionScreen> createState() => _PermissionScreenState();
}

class _PermissionScreenState extends State<PermissionScreen> {
  bool _isRequesting = false;

  Future<void> _requestPermissions() async {
    setState(() => _isRequesting = true);

    try {
      await [
        Permission.camera,
        Permission.photos,
        Permission.storage,
      ].request();
    } catch (e) {
      debugPrint('Permission request error: $e');
    } finally {
      if (mounted) {
        setState(() => _isRequesting = false);
        Navigator.of(context).pushReplacement(
          MaterialPageRoute(builder: (_) => const CameraScreen()),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.darkBackground,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 28, vertical: 20),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Spacer(),
              const ZipgramLogo(height: 52),
              const SizedBox(height: 32),
              Container(
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  color: AppColors.darkSurface,
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: AppColors.darkCard),
                ),
                child: Column(
                  children: const [
                    Icon(
                      Icons.camera_enhance_outlined,
                      size: 56,
                      color: AppColors.primaryBlue,
                    ),
                    SizedBox(height: 16),
                    Text(
                      'Camera & Gallery Access',
                      style: TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                    SizedBox(height: 12),
                    Text(
                      'Zipgram needs camera permission to capture live filtered photos and storage permission to save them to your device gallery.',
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        fontSize: 14,
                        color: AppColors.textSecondary,
                        height: 1.4,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),

              // Local-first Privacy Badge
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                decoration: BoxDecoration(
                  color: AppColors.primaryBlue.withValues(alpha: 0.1),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: AppColors.primaryBlue.withValues(alpha: 0.3)),
                ),
                child: Row(
                  children: const [
                    Icon(Icons.shield_outlined, color: AppColors.primaryBlue, size: 22),
                    SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        '100% Local Privacy: Your photos never leave your device. No cloud storage, no account registration required.',
                        style: TextStyle(
                          color: AppColors.primaryBlueLight,
                          fontSize: 12,
                          height: 1.3,
                        ),
                      ),
                    ),
                  ],
                ),
              ),

              const Spacer(),

              SizedBox(
                width: double.infinity,
                height: 54,
                child: ElevatedButton(
                  onPressed: _isRequesting ? null : _requestPermissions,
                  child: _isRequesting
                      ? const SizedBox(
                          width: 24,
                          height: 24,
                          child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2.5),
                        )
                      : const Text(
                          'Allow Camera & Start',
                          style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                        ),
                ),
              ),
              const SizedBox(height: 16),
            ],
          ),
        ),
      ),
    );
  }
}
