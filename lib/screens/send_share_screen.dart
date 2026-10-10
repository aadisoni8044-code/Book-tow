import 'dart:io';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:gal/gal.dart';
import 'package:path_provider/path_provider.dart';
import 'package:share_plus/share_plus.dart';

import '../models/app_filter.dart';
import '../services/filter_processor.dart';
import '../theme/app_theme.dart';

class SendShareScreen extends StatefulWidget {
  final File imageFile;
  final Uint8List? filteredBytes;
  final AppFilter selectedFilter;

  const SendShareScreen({
    super.key,
    required this.imageFile,
    this.filteredBytes,
    required this.selectedFilter,
  });

  @override
  State<SendShareScreen> createState() => _SendShareScreenState();
}

class _SendShareScreenState extends State<SendShareScreen> {
  bool _isSharing = false;
  bool _isSaving = false;
  bool _isSaved = false;

  Future<File> _getFinalFilteredFile() async {
    final tempDir = await getTemporaryDirectory();
    final String savePath =
        '${tempDir.path}/SnapCam_Share_${DateTime.now().millisecondsSinceEpoch}.jpg';
    final File targetFile = File(savePath);

    if (widget.filteredBytes != null) {
      await targetFile.writeAsBytes(widget.filteredBytes!);
    } else {
      await FilterProcessor.processImageFile(
        widget.imageFile,
        targetFile,
        widget.selectedFilter,
      );
    }
    return targetFile;
  }

  Future<void> _sharePhoto() async {
    if (_isSharing) return;

    setState(() {
      _isSharing = true;
    });

    try {
      final File finalFile = await _getFinalFilteredFile();
      final XFile xFile = XFile(finalFile.path, mimeType: 'image/jpeg');

      await Share.shareXFiles(
        [xFile],
        text: 'Captured with SnapCam!',
      );
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Failed to share image: $e'),
            backgroundColor: Colors.redAccent,
          ),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          _isSharing = false;
        });
      }
    }
  }

  Future<void> _saveOnly() async {
    if (_isSaving) return;

    setState(() {
      _isSaving = true;
    });

    try {
      final File finalFile = await _getFinalFilteredFile();
      await Gal.putImage(finalFile.path);

      if (mounted) {
        setState(() {
          _isSaved = true;
        });
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Saved to gallery successfully!'),
            backgroundColor: AppTheme.cardDark,
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Failed to save image: $e'),
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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.darkBackground,
      appBar: AppBar(
        title: const Text('Send / Share'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => Navigator.of(context).pop(),
        ),
      ),
      body: SafeArea(
        child: Column(
          children: [
            // Thumbnail Preview Card
            Expanded(
              child: Container(
                margin: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(20),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.5),
                      blurRadius: 15,
                      spreadRadius: 2,
                    ),
                  ],
                ),
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(20),
                  child: widget.filteredBytes != null
                      ? Image.memory(widget.filteredBytes!, fit: BoxFit.cover)
                      : Image.file(widget.imageFile, fit: BoxFit.cover),
                ),
              ),
            ),

            // Share Actions Panel
            Container(
              padding: const EdgeInsets.all(24),
              decoration: const BoxDecoration(
                color: AppTheme.cardDark,
                borderRadius: BorderRadius.vertical(top: Radius.circular(28)),
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.all(8),
                        decoration: BoxDecoration(
                          color: AppTheme.primaryYellow.withOpacity(0.2),
                          shape: BoxShape.circle,
                        ),
                        child: const Icon(
                          Icons.send_rounded,
                          color: AppTheme.primaryYellow,
                        ),
                      ),
                      const SizedBox(width: 12),
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            'Share Your Snap',
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          Text(
                            'Filter: ${widget.selectedFilter.name}',
                            style: const TextStyle(
                              color: AppTheme.textSecondary,
                              fontSize: 13,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                  const SizedBox(height: 24),

                  // Share to External Apps Button
                  ElevatedButton.icon(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppTheme.primaryYellow,
                      foregroundColor: Colors.black,
                      padding: const EdgeInsets.symmetric(vertical: 16),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(30),
                      ),
                    ),
                    onPressed: _isSharing ? null : _sharePhoto,
                    icon: _isSharing
                        ? const SizedBox(
                            width: 20,
                            height: 20,
                            child: CircularProgressIndicator(
                              strokeWidth: 2,
                              color: Colors.black,
                            ),
                          )
                        : const Icon(Icons.share_rounded, color: Colors.black),
                    label: const Text(
                      'Share to Other Apps',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  const SizedBox(height: 12),

                  // Save to Gallery without Sharing Button
                  OutlinedButton.icon(
                    style: OutlinedButton.styleFrom(
                      foregroundColor: Colors.white,
                      side: const BorderSide(color: Colors.white38),
                      padding: const EdgeInsets.symmetric(vertical: 16),
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(30),
                      ),
                    ),
                    onPressed: _isSaving ? null : _saveOnly,
                    icon: _isSaving
                        ? const SizedBox(
                            width: 20,
                            height: 20,
                            child: CircularProgressIndicator(
                              strokeWidth: 2,
                              color: AppTheme.primaryYellow,
                            ),
                          )
                        : Icon(
                            _isSaved ? Icons.check_circle : Icons.download_rounded,
                            color: _isSaved ? AppTheme.primaryYellow : Colors.white,
                          ),
                    label: Text(
                      _isSaved ? 'Saved to Gallery' : 'Save to Gallery Only',
                      style: TextStyle(
                        fontSize: 16,
                        color: _isSaved ? AppTheme.primaryYellow : Colors.white,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
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
