import 'dart:io';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';

import '../services/gallery_service.dart';
import '../theme/app_colors.dart';

class CameraControls extends StatelessWidget {
  final FlashMode flashMode;
  final bool isCapturing;
  final VoidCallback onToggleFlash;
  final VoidCallback onSwitchCamera;
  final VoidCallback onTakePick;
  final VoidCallback onOpenSettings;
  final VoidCallback onOpenGallery;

  const CameraControls({
    super.key,
    required this.flashMode,
    required this.isCapturing,
    required this.onToggleFlash,
    required this.onSwitchCamera,
    required this.onTakePick,
    required this.onOpenSettings,
    required this.onOpenGallery,
  });

  IconData _getFlashIcon() {
    switch (flashMode) {
      case FlashMode.always:
        return Icons.flash_on;
      case FlashMode.auto:
        return Icons.flash_auto;
      case FlashMode.torch:
        return Icons.highlight;
      case FlashMode.off:
        return Icons.flash_off;
    }
  }

  @override
  Widget build(BuildContext context) {
    final latestPath = GalleryService.latestPhotoPath;

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          // Gallery Shortcut Thumbnail
          GestureDetector(
            onTap: onOpenGallery,
            child: Container(
              width: 48,
              height: 48,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                border: Border.all(color: Colors.white30, width: 2),
                color: AppColors.darkCard,
              ),
              child: ClipOval(
                child: latestPath != null && File(latestPath).existsSync()
                    ? Image.file(
                        File(latestPath),
                        fit: BoxFit.cover,
                      )
                    : const Icon(
                        Icons.photo_library_outlined,
                        color: Colors.white,
                        size: 22,
                      ),
              ),
            ),
          ),

          // Flip Camera Button
          IconButton(
            onPressed: onSwitchCamera,
            icon: const Icon(
              Icons.flip_camera_ios_outlined,
              color: Colors.white,
              size: 28,
            ),
            style: IconButton.styleFrom(
              backgroundColor: Colors.black26,
              padding: const EdgeInsets.all(10),
            ),
          ),

          // Shutter Button
          GestureDetector(
            onTap: isCapturing ? null : onTakePick,
            child: AnimatedContainer(
              duration: const Duration(milliseconds: 150),
              width: 76,
              height: 76,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                border: Border.all(
                  color: AppColors.primaryBlue,
                  width: 4,
                ),
                color: Colors.transparent,
                boxShadow: [
                  BoxShadow(
                    color: AppColors.primaryBlue.withValues(alpha: 0.3),
                    blurRadius: 16,
                    spreadRadius: 2,
                  ),
                ],
              ),
              padding: const EdgeInsets.all(4),
              child: Container(
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: isCapturing ? AppColors.primaryBlueLight : Colors.white,
                ),
                child: isCapturing
                    ? const Center(
                        child: SizedBox(
                          width: 28,
                          height: 28,
                          child: CircularProgressIndicator(
                            color: AppColors.primaryBlue,
                            strokeWidth: 3,
                          ),
                        ),
                      )
                    : null,
              ),
            ),
          ),

          // Flash Toggle Button
          IconButton(
            onPressed: onToggleFlash,
            icon: Icon(
              _getFlashIcon(),
              color: flashMode == FlashMode.off ? Colors.white70 : AppColors.primaryBlueLight,
              size: 26,
            ),
            style: IconButton.styleFrom(
              backgroundColor: Colors.black26,
              padding: const EdgeInsets.all(10),
            ),
          ),

          // Settings Shortcut Button
          IconButton(
            onPressed: onOpenSettings,
            icon: const Icon(
              Icons.settings_outlined,
              color: Colors.white,
              size: 26,
            ),
            style: IconButton.styleFrom(
              backgroundColor: Colors.black26,
              padding: const EdgeInsets.all(10),
            ),
          ),
        ],
      ),
    );
  }
}
