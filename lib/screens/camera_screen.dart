import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../providers/camera_provider.dart';
import '../providers/settings_provider.dart';
import '../theme/app_theme.dart';
import '../widgets/camera_top_bar.dart';
import '../widgets/filter_carousel.dart';
import 'captured_photo_screen.dart';
import 'premium_screen.dart';
import 'settings_screen.dart';

class CameraScreen extends StatefulWidget {
  const CameraScreen({super.key});

  @override
  State<CameraScreen> createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> with WidgetsBindingObserver {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final cameraProvider = Provider.of<CameraProvider>(context, listen: false);
      if (!cameraProvider.isInitialized && !cameraProvider.isInitializing) {
        cameraProvider.requestPermissionsAndInit();
      }
    });
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    final cameraProvider = Provider.of<CameraProvider>(context, listen: false);
    if (cameraProvider.controller == null || !cameraProvider.controller!.value.isInitialized) {
      return;
    }

    if (state == AppLifecycleState.inactive || state == AppLifecycleState.paused) {
      // Free camera resource when app goes background
      cameraProvider.controller?.dispose();
    } else if (state == AppLifecycleState.resumed) {
      // Re-init when app comes back to foreground
      cameraProvider.requestPermissionsAndInit();
    }
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    super.dispose();
  }

  void _onShutterTap(CameraProvider cameraProvider, SettingsProvider settings) async {
    final file = await cameraProvider.takePicture(
      timerSeconds: settings.timerSeconds,
    );

    if (file != null && mounted) {
      Navigator.of(context).push(
        MaterialPageRoute(
          builder: (_) => const CapturedPhotoScreen(),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Consumer2<CameraProvider, SettingsProvider>(
      builder: (context, camera, settings, child) {
        return Scaffold(
          backgroundColor: AppTheme.darkBackground,
          body: Stack(
            fit: StackTrace.expand,
            children: [
              // 1. Full-screen Camera Preview with Filter
              _buildCameraPreview(camera),

              // 2. Camera Grid Overlay (if enabled)
              if (settings.gridEnabled) _buildGridOverlay(),

              // 3. Countdown Overlay (if timer active)
              if (camera.isCapturing && camera.countdownSeconds > 0)
                _buildCountdownOverlay(camera.countdownSeconds),

              // 4. Top Action Bar
              Positioned(
                top: 0,
                left: 0,
                right: 0,
                child: CameraTopBar(
                  settings: settings,
                  onSwitchCamera: () => camera.switchCamera(),
                  onOpenSettings: () {
                    Navigator.of(context).push(
                      MaterialPageRoute(
                        builder: (_) => const SettingsScreen(),
                      ),
                    );
                  },
                  onOpenPremium: () {
                    Navigator.of(context).push(
                      MaterialPageRoute(
                        builder: (_) => const PremiumScreen(),
                      ),
                    );
                  },
                ),
              ),

              // 5. Bottom Controls (Filter Carousel + Shutter & Gallery)
              Positioned(
                bottom: 0,
                left: 0,
                right: 0,
                child: SafeArea(
                  top: false,
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      // Filter Carousel
                      FilterCarousel(
                        selectedFilter: camera.selectedFilter,
                        onFilterSelected: (filter) {
                          camera.setFilter(filter);
                        },
                      ),
                      const SizedBox(height: 16),

                      // Shutter and Side Action Buttons Row
                      Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 8),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                          children: [
                            // Left Gallery Quick Launch / Memory Button
                            IconButton(
                              icon: Container(
                                padding: const EdgeInsets.all(10),
                                decoration: BoxDecoration(
                                  color: Colors.black.withOpacity(0.5),
                                  shape: BoxShape.circle,
                                  border: Border.all(
                                    color: Colors.white.withOpacity(0.3),
                                  ),
                                ),
                                child: const Icon(
                                  Icons.photo_library_outlined,
                                  color: Colors.white,
                                  size: 24,
                                ),
                              ),
                              onPressed: () {
                                ScaffoldMessenger.of(context).showSnackBar(
                                  const SnackBar(
                                    content: Text('Gallery quick launch opened'),
                                    duration: Duration(seconds: 1),
                                  ),
                                );
                              },
                              tooltip: 'Gallery',
                            ),

                            // Center Large Circular Shutter Button
                            GestureDetector(
                              onTap: () => _onShutterTap(camera, settings),
                              child: Container(
                                width: 84,
                                height: 84,
                                decoration: BoxDecoration(
                                  shape: BoxShape.circle,
                                  border: Border.all(
                                    color: AppTheme.primaryYellow,
                                    width: 4,
                                  ),
                                  boxShadow: [
                                    BoxShadow(
                                      color: AppTheme.primaryYellow.withOpacity(0.3),
                                      blurRadius: 16,
                                      spreadRadius: 2,
                                    ),
                                  ],
                                ),
                                padding: const EdgeInsets.all(4),
                                child: Container(
                                  decoration: const BoxDecoration(
                                    color: AppTheme.primaryYellow,
                                    shape: BoxShape.circle,
                                  ),
                                  child: camera.isCapturing
                                      ? const Center(
                                          child: SizedBox(
                                            width: 28,
                                            height: 28,
                                            child: CircularProgressIndicator(
                                              color: Colors.black,
                                              strokeWidth: 3,
                                            ),
                                          ),
                                        )
                                      : null,
                                ),
                              ),
                            ),

                            // Right Secondary Action / Premium Effect Button
                            IconButton(
                              icon: Container(
                                padding: const EdgeInsets.all(10),
                                decoration: BoxDecoration(
                                  color: Colors.black.withOpacity(0.5),
                                  shape: BoxShape.circle,
                                  border: Border.all(
                                    color: Colors.white.withOpacity(0.3),
                                  ),
                                ),
                                child: const Icon(
                                  Icons.auto_awesome,
                                  color: AppTheme.primaryYellow,
                                  size: 24,
                                ),
                              ),
                              onPressed: () {
                                Navigator.of(context).push(
                                  MaterialPageRoute(
                                    builder: (_) => const PremiumScreen(),
                                  ),
                                );
                              },
                              tooltip: 'Special Effects',
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(height: 12),
                    ],
                  ),
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  Widget _buildCameraPreview(CameraProvider camera) {
    if (camera.isInitializing) {
      return const Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            CircularProgressIndicator(color: AppTheme.primaryYellow),
            SizedBox(height: 16),
            Text(
              'Initializing Camera...',
              style: TextStyle(color: Colors.white70),
            ),
          ],
        ),
      );
    }

    if (camera.errorMessage != null) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(32),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.camera_alt_outlined, color: Colors.white54, size: 64),
              const SizedBox(height: 16),
              Text(
                camera.errorMessage!,
                textAlign: TextAlign.center,
                style: const TextStyle(color: Colors.white, fontSize: 16),
              ),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: () => camera.requestPermissionsAndInit(),
                child: const Text('Grant Camera Access'),
              ),
            ],
          ),
        ),
      );
    }

    Widget rawPreview;
    if (camera.isInitialized && camera.controller != null) {
      final controller = camera.controller!;
      final previewSize = controller.value.previewSize;

      if (previewSize != null) {
        // Crop/Fit camera preview to full available screen without distortion
        rawPreview = LayoutBuilder(
          builder: (context, constraints) {
            var scale = constraints.maxHeight / (constraints.maxWidth * controller.value.aspectRatio);
            if (scale < 1) scale = 1 / scale;

            return Transform.scale(
              scale: scale,
              child: Center(
                child: CameraPreview(controller),
              ),
            );
          },
        );
      } else {
        rawPreview = CameraPreview(controller);
      }
    } else {
      // Mock full-screen live feed fallback for non-supported hardware environment
      rawPreview = Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [
              Colors.grey.shade900,
              Colors.blueGrey.shade900,
            ],
          ),
        ),
        child: const Center(
          child: Icon(Icons.camera_front, size: 100, color: Colors.white24),
        ),
      );
    }

    // Apply live filter to camera stream
    return ColorFiltered(
      colorFilter: camera.selectedFilter.colorFilter,
      child: rawPreview,
    );
  }

  Widget _buildGridOverlay() {
    return IgnorePointer(
      child: Column(
        children: [
          Expanded(
            child: Row(
              children: [
                Expanded(child: Container(decoration: BoxDecoration(border: Border.all(color: Colors.white24, width: 0.5)))),
                Expanded(child: Container(decoration: BoxDecoration(border: Border.all(color: Colors.white24, width: 0.5)))),
                Expanded(child: Container(decoration: BoxDecoration(border: Border.all(color: Colors.white24, width: 0.5)))),
              ],
            ),
          ),
          Expanded(
            child: Row(
              children: [
                Expanded(child: Container(decoration: BoxDecoration(border: Border.all(color: Colors.white24, width: 0.5)))),
                Expanded(child: Container(decoration: BoxDecoration(border: Border.all(color: Colors.white24, width: 0.5)))),
                Expanded(child: Container(decoration: BoxDecoration(border: Border.all(color: Colors.white24, width: 0.5)))),
              ],
            ),
          ),
          Expanded(
            child: Row(
              children: [
                Expanded(child: Container(decoration: BoxDecoration(border: Border.all(color: Colors.white24, width: 0.5)))),
                Expanded(child: Container(decoration: BoxDecoration(border: Border.all(color: Colors.white24, width: 0.5)))),
                Expanded(child: Container(decoration: BoxDecoration(border: Border.all(color: Colors.white24, width: 0.5)))),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildCountdownOverlay(int seconds) {
    return Container(
      color: Colors.black.withOpacity(0.5),
      child: Center(
        child: AnimatedSwitcher(
          duration: const Duration(milliseconds: 300),
          child: Text(
            '$seconds',
            key: ValueKey(seconds),
            style: const TextStyle(
              fontSize: 120,
              fontWeight: FontWeight.bold,
              color: AppTheme.primaryYellow,
            ),
          ),
        ),
      ),
    );
  }
}
