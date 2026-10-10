import 'dart:io';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:gal/gal.dart';
import 'package:path_provider/path_provider.dart';
import 'package:provider/provider.dart';

import '../providers/camera_provider.dart';
import '../providers/settings_provider.dart';
import '../services/filter_processor.dart';
import '../theme/app_theme.dart';
import '../widgets/filter_carousel.dart';
import 'send_share_screen.dart';

class CapturedPhotoScreen extends StatefulWidget {
  const CapturedPhotoScreen({super.key});

  @override
  State<CapturedPhotoScreen> createState() => _CapturedPhotoScreenState();
}

class _CapturedPhotoScreenState extends State<CapturedPhotoScreen> {
  bool _isSaving = false;
  bool _isSaved = false;

  Future<void> _saveToGallery(CameraProvider camera) async {
    if (_isSaving || camera.capturedImageFile == null) return;

    setState(() {
      _isSaving = true;
    });

    try {
      final tempDir = await getTemporaryDirectory();
      final String savePath =
          '${tempDir.path}/SnapCam_${DateTime.now().millisecondsSinceEpoch}.jpg';
      final File saveFile = File(savePath);

      if (camera.capturedFilteredBytes != null) {
        await saveFile.writeAsBytes(camera.capturedFilteredBytes!);
      } else {
        await FilterProcessor.processImageFile(
          camera.capturedImageFile!,
          saveFile,
          camera.selectedFilter,
        );
      }

      // Save using Gal
      await Gal.putImage(saveFile.path);

      if (mounted) {
        setState(() {
          _isSaved = true;
        });
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Row(
              children: [
                Icon(Icons.check_circle, color: AppTheme.primaryYellow),
                SizedBox(width: 8),
                Text('Photo saved to Gallery!'),
              ],
            ),
            backgroundColor: AppTheme.cardDark,
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Failed to save photo: $e'),
            backgroundColor: Colors.redAccent,
          ),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          _isSaving = false;
        });
      }
    }
  }

  void _onRetake(CameraProvider camera) {
    camera.clearCaptured();
    Navigator.of(context).pop();
  }

  void _onSend(CameraProvider camera) {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => SendShareScreen(
          imageFile: camera.capturedImageFile!,
          filteredBytes: camera.capturedFilteredBytes,
          selectedFilter: camera.selectedFilter,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Consumer2<CameraProvider, SettingsProvider>(
      builder: (context, camera, settings, child) {
        final File? imageFile = camera.capturedImageFile;
        final Uint8List? filteredBytes = camera.capturedFilteredBytes;

        if (imageFile == null) {
          return Scaffold(
            backgroundColor: AppTheme.darkBackground,
            appBar: AppBar(),
            body: const Center(
              child: Text('No photo captured', style: TextStyle(color: Colors.white)),
            ),
          );
        }

        return Scaffold(
          backgroundColor: AppTheme.darkBackground,
          body: Stack(
            fit: StackTrace.expand,
            children: [
              // 1. Full-screen Photo Preview
              filteredBytes != null
                  ? Image.memory(
                      filteredBytes,
                      fit: BoxFit.cover,
                      width: double.infinity,
                      height: double.infinity,
                    )
                  : Image.file(
                      imageFile,
                      fit: BoxFit.cover,
                      width: double.infinity,
                      height: double.infinity,
                    ),

              // 2. Top Action Bar (Retake / Close)
              Positioned(
                top: 0,
                left: 0,
                right: 0,
                child: SafeArea(
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        // Retake / Back button
                        IconButton(
                          icon: Container(
                            padding: const EdgeInsets.all(8),
                            decoration: BoxDecoration(
                              color: Colors.black.withOpacity(0.5),
                              shape: BoxShape.circle,
                            ),
                            child: const Icon(Icons.close, color: Colors.white, size: 24),
                          ),
                          onPressed: () => _onRetake(camera),
                          tooltip: 'Retake',
                        ),

                        // Active Filter Name Chip
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
                          decoration: BoxDecoration(
                            color: Colors.black.withOpacity(0.6),
                            borderRadius: BorderRadius.circular(20),
                            border: Border.all(color: AppTheme.primaryYellow.withOpacity(0.6)),
                          ),
                          child: Text(
                            camera.selectedFilter.name.toUpperCase(),
                            style: const TextStyle(
                              color: AppTheme.primaryYellow,
                              fontSize: 12,
                              fontWeight: FontWeight.bold,
                              letterSpacing: 1.2,
                            ),
                          ),
                        ),

                        // Quick Retake Text Button
                        TextButton(
                          onPressed: () => _onRetake(camera),
                          child: const Text('Retake', style: TextStyle(color: Colors.white, fontSize: 16)),
                        ),
                      ],
                    ),
                  ),
                ),
              ),

              // 3. Bottom Controls Area (Filter Selector + Save & Send Buttons)
              Positioned(
                bottom: 0,
                left: 0,
                right: 0,
                child: Container(
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      begin: Alignment.bottomCenter,
                      end: Alignment.topCenter,
                      colors: [
                        Colors.black.withOpacity(0.85),
                        Colors.transparent,
                      ],
                    ),
                  ),
                  child: SafeArea(
                    top: false,
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        // Filter Selection Carousel (Post-capture filter change)
                        FilterCarousel(
                          selectedFilter: camera.selectedFilter,
                          onFilterSelected: (filter) {
                            camera.setFilter(filter);
                          },
                        ),
                        const SizedBox(height: 16),

                        // Actions Row: Download/Save and Send/Share Button
                        Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                          child: Row(
                            children: [
                              // Save to Gallery Button
                              Expanded(
                                child: OutlinedButton.icon(
                                  style: OutlinedButton.styleFrom(
                                    foregroundColor: Colors.white,
                                    side: BorderSide(
                                      color: _isSaved ? AppTheme.primaryYellow : Colors.white38,
                                      width: 1.5,
                                    ),
                                    padding: const EdgeInsets.symmetric(vertical: 14),
                                    shape: RoundedRectangleBorder(
                                      borderRadius: BorderRadius.circular(30),
                                    ),
                                  ),
                                  onPressed: _isSaving ? null : () => _saveToGallery(camera),
                                  icon: _isSaving
                                      ? const SizedBox(
                                          width: 18,
                                          height: 18,
                                          child: CircularProgressIndicator(
                                            strokeWidth: 2,
                                            color: AppTheme.primaryYellow,
                                          ),
                                        )
                                      : Icon(
                                          _isSaved ? Icons.check : Icons.download,
                                          color: _isSaved ? AppTheme.primaryYellow : Colors.white,
                                        ),
                                  label: Text(
                                    _isSaved ? 'Saved' : 'Save',
                                    style: TextStyle(
                                      color: _isSaved ? AppTheme.primaryYellow : Colors.white,
                                      fontWeight: FontWeight.bold,
                                      fontSize: 16,
                                    ),
                                  ),
                                ),
                              ),
                              const SizedBox(width: 16),

                              // Send / Share Button
                              Expanded(
                                child: ElevatedButton.icon(
                                  style: ElevatedButton.styleFrom(
                                    backgroundColor: AppTheme.primaryYellow,
                                    foregroundColor: Colors.black,
                                    padding: const EdgeInsets.symmetric(vertical: 14),
                                    shape: RoundedRectangleBorder(
                                      borderRadius: BorderRadius.circular(30),
                                    ),
                                  ),
                                  onPressed: () => _onSend(camera),
                                  icon: const Icon(Icons.send_rounded, color: Colors.black),
                                  label: const Text(
                                    'Send To',
                                    style: TextStyle(
                                      color: Colors.black,
                                      fontWeight: FontWeight.bold,
                                      fontSize: 16,
                                    ),
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}
