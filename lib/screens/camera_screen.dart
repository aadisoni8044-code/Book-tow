import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../providers/camera_provider.dart';
import '../providers/filter_provider.dart';
import '../providers/settings_provider.dart';
import '../services/filter_service.dart';
import '../services/gallery_service.dart';
import '../theme/app_colors.dart';
import '../widgets/camera_controls.dart';
import '../widgets/filter_selector.dart';
import '../widgets/zipgram_logo.dart';
import 'preview_screen.dart';
import 'settings_screen.dart';

class CameraScreen extends StatefulWidget {
  const CameraScreen({super.key});

  @override
  State<CameraScreen> createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final settings = context.read<SettingsProvider>();
      context.read<CameraProvider>().initializeCamera(
            preferredCamera: settings.preferredCamera,
          );
    });
  }

  Future<void> _handleCapture() async {
    final cameraProvider = context.read<CameraProvider>();
    final filterProvider = context.read<FilterProvider>();
    final settingsProvider = context.read<SettingsProvider>();

    final rawPath = await cameraProvider.takePicture();
    if (rawPath == null || !mounted) return;

    // Show processing loading overlay
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (_) => const Center(
        child: CircularProgressIndicator(color: AppColors.primaryBlue),
      ),
    );

    try {
      final tempOutputPath = await GalleryService.getTempImagePath(prefix: 'zipgram_filtered');

      // Process filtered image
      final filteredFile = await FilterService.applyFilterToFile(
        inputPath: rawPath,
        outputPath: tempOutputPath,
        filterType: filterProvider.selectedType,
        quality: settingsProvider.photoQuality,
      );

      if (mounted) {
        Navigator.of(context).pop(); // Close loader

        // Open Preview Screen
        Navigator.of(context).push(
          MaterialPageRoute(
            builder: (_) => PreviewScreen(
              imagePath: filteredFile.path,
              appliedFilter: filterProvider.selectedFilter,
            ),
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        Navigator.of(context).pop();
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error processing photo: $e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Consumer2<CameraProvider, FilterProvider>(
        builder: (context, camera, filter, child) {
          return Stack(
            fit: StackFit.expand,
            children: [
              // 1. FULL SCREEN CAMERA PREVIEW WITH LIVE COLOR FILTER
              if (camera.isInitialized && camera.controller != null && camera.controller!.value.isInitialized)
                Positioned.fill(
                  child: ColorFiltered(
                    colorFilter: ColorFilter.matrix(filter.currentMatrix),
                    child: FittedBox(
                      fit: BoxFit.cover,
                      child: SizedBox(
                        width: camera.controller!.value.previewSize?.height ?? MediaQuery.of(context).size.width,
                        height: camera.controller!.value.previewSize?.width ?? MediaQuery.of(context).size.height,
                        child: CameraPreview(camera.controller!),
                      ),
                    ),
                  ),
                )
              else
                // Fallback Mock Camera Preview Screen
                Positioned.fill(
                  child: ColorFiltered(
                    colorFilter: ColorFilter.matrix(filter.currentMatrix),
                    child: Container(
                      decoration: const BoxDecoration(
                        gradient: LinearGradient(
                          colors: [
                            Color(0xFF0F172A),
                            Color(0xFF1E293B),
                            Color(0xFF0284C7),
                          ],
                          begin: Alignment.topLeft,
                          end: Alignment.bottomRight,
                        ),
                      ),
                      child: Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(
                              filter.selectedFilter.icon,
                              size: 72,
                              color: Colors.white70,
                            ),
                            const SizedBox(height: 12),
                            Text(
                              'Live Preview Mode: ${filter.selectedFilter.name}',
                              style: const TextStyle(
                                color: Colors.white,
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            const SizedBox(height: 6),
                            const Text(
                              'Simulated Camera active',
                              style: TextStyle(
                                color: AppColors.textSecondary,
                                fontSize: 13,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                ),

              // 2. TOP BRANDING BAR & CONTROLS
              SafeArea(
                child: Align(
                  alignment: Alignment.topCenter,
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const ZipgramLogo(height: 32),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                          decoration: BoxDecoration(
                            color: Colors.black45,
                            borderRadius: BorderRadius.circular(16),
                            border: Border.all(color: Colors.white24),
                          ),
                          child: Row(
                            children: [
                              Icon(
                                filter.selectedFilter.icon,
                                color: AppColors.primaryBlueLight,
                                size: 16,
                              ),
                              const SizedBox(width: 6),
                              Text(
                                filter.selectedFilter.name,
                                style: const TextStyle(
                                  color: Colors.white,
                                  fontSize: 12,
                                  fontWeight: FontWeight.w600,
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

              // 3. BOTTOM CONTROLS & FILTER SELECTOR
              SafeArea(
                child: Align(
                  alignment: Alignment.bottomCenter,
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      // Filter Selector
                      FilterSelector(
                        selectedFilter: filter.selectedFilter,
                        onFilterSelected: (newFilter) {
                          filter.selectFilter(newFilter);
                        },
                      ),
                      const SizedBox(height: 12),
                      // Camera Controls
                      CameraControls(
                        flashMode: camera.flashMode,
                        isCapturing: camera.isCapturing,
                        onToggleFlash: () => camera.toggleFlash(),
                        onSwitchCamera: () => camera.switchCamera(),
                        onTakePick: _handleCapture,
                        onOpenSettings: () {
                          Navigator.of(context).push(
                            MaterialPageRoute(
                              builder: (_) => const SettingsScreen(),
                            ),
                          );
                        },
                        onOpenGallery: () {
                          final path = GalleryService.latestPhotoPath;
                          if (path != null) {
                            Navigator.of(context).push(
                              MaterialPageRoute(
                                builder: (_) => PreviewScreen(
                                  imagePath: path,
                                  appliedFilter: filter.selectedFilter,
                                ),
                              ),
                            );
                          } else {
                            ScaffoldMessenger.of(context).showSnackBar(
                              const SnackBar(
                                content: Text('No photos captured yet'),
                                duration: Duration(seconds: 2),
                              ),
                            );
                          }
                        },
                      ),
                      const SizedBox(height: 8),
                    ],
                  ),
                ),
              ),
            ],
          );
        },
      ),
    );
  }
}
