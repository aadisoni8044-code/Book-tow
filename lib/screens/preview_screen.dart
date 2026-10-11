import 'dart:io';
import 'package:flutter/material.dart';

import '../models/app_filter.dart';
import '../services/gallery_service.dart';
import '../services/share_service.dart';
import '../theme/app_colors.dart';

class PreviewScreen extends StatefulWidget {
  final String imagePath;
  final AppFilter appliedFilter;

  const PreviewScreen({
    super.key,
    required this.imagePath,
    required this.appliedFilter,
  });

  @override
  State<PreviewScreen> createState() => _PreviewScreenState();
}

class _PreviewScreenState extends State<PreviewScreen> {
  bool _isSaving = false;
  bool _isSaved = false;

  Future<void> _handleSave() async {
    if (_isSaving || _isSaved) return;

    setState(() => _isSaving = true);

    final success = await GalleryService.saveToGallery(widget.imagePath);

    if (mounted) {
      setState(() {
        _isSaving = false;
        _isSaved = success;
      });

      if (success) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            backgroundColor: AppColors.success,
            content: Row(
              children: const [
                Icon(Icons.check_circle_outline, color: Colors.white),
                SizedBox(width: 10),
                Text(
                  'Saved to Gallery in "Zipgram" album!',
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
              ],
            ),
            duration: const Duration(seconds: 3),
          ),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            backgroundColor: AppColors.error,
            content: Text('Failed to save photo to gallery'),
          ),
        );
      }
    }
  }

  Future<void> _handleShare() async {
    final success = await ShareService.sharePhoto(
      widget.imagePath,
      caption: 'Captured with Zipgram - ${widget.appliedFilter.name} Filter',
    );

    if (!success && mounted) {
      debugPrint('Share dismissed or failed');
    }
  }

  @override
  Widget build(BuildContext context) {
    final file = File(widget.imagePath);

    return Scaffold(
      backgroundColor: Colors.black,
      body: SafeArea(
        child: Column(
          children: [
            // Top Bar
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  IconButton(
                    onPressed: () => Navigator.of(context).pop(),
                    icon: const Icon(Icons.arrow_back, color: Colors.white),
                    tooltip: 'Retake',
                  ),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                    decoration: BoxDecoration(
                      color: AppColors.darkCard,
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Row(
                      children: [
                        Icon(
                          widget.appliedFilter.icon,
                          color: AppColors.primaryBlueLight,
                          size: 16,
                        ),
                        const SizedBox(width: 6),
                        Text(
                          widget.appliedFilter.name,
                          style: const TextStyle(
                            color: Colors.white,
                            fontSize: 13,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(width: 48), // Balance spacing
                ],
              ),
            ),

            // Main Photo Display Area
            Expanded(
              child: Container(
                margin: const EdgeInsets.symmetric(horizontal: 12),
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(20),
                  child: file.existsSync()
                      ? Image.file(
                          file,
                          fit: BoxFit.contain,
                          width: double.infinity,
                          height: double.infinity,
                        )
                      : const Center(
                          child: Text(
                            'Image not found',
                            style: TextStyle(color: Colors.white70),
                          ),
                        ),
                ),
              ),
            ),

            const SizedBox(height: 16),

            // Bottom Action Controls
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
              child: Column(
                children: [
                  // Prominent Share Button
                  SizedBox(
                    width: double.infinity,
                    height: 54,
                    child: ElevatedButton.icon(
                      onPressed: _handleShare,
                      icon: const Icon(Icons.share_outlined, size: 22),
                      label: const Text(
                        'Share Photo',
                        style: TextStyle(fontSize: 17, fontWeight: FontWeight.bold),
                      ),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.primaryBlue,
                        foregroundColor: Colors.white,
                        elevation: 4,
                      ),
                    ),
                  ),

                  const SizedBox(height: 12),

                  // Secondary Buttons Row (Retake & Save)
                  Row(
                    children: [
                      // Retake Button
                      Expanded(
                        child: SizedBox(
                          height: 48,
                          child: OutlinedButton.icon(
                            onPressed: () => Navigator.of(context).pop(),
                            icon: const Icon(Icons.refresh, size: 20),
                            label: const Text('Retake'),
                            style: OutlinedButton.styleFrom(
                              foregroundColor: Colors.white,
                              side: const BorderSide(color: AppColors.inactiveBorder),
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(width: 12),
                      // Save Button
                      Expanded(
                        child: SizedBox(
                          height: 48,
                          child: ElevatedButton.icon(
                            onPressed: _isSaving ? null : _handleSave,
                            icon: _isSaving
                                ? const SizedBox(
                                    width: 18,
                                    height: 18,
                                    child: CircularProgressIndicator(
                                      color: Colors.white,
                                      strokeWidth: 2,
                                    ),
                                  )
                                : Icon(
                                    _isSaved ? Icons.check : Icons.download_outlined,
                                    size: 20,
                                  ),
                            label: Text(_isSaved ? 'Saved' : 'Save Photo'),
                            style: ElevatedButton.styleFrom(
                              backgroundColor: _isSaved ? AppColors.success : AppColors.darkCard,
                              foregroundColor: Colors.white,
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
