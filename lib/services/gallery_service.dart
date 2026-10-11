import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:gal/gal.dart';
import 'package:path_provider/path_provider.dart';

class GalleryService {
  static String? _latestPhotoPath;

  static String? get latestPhotoPath => _latestPhotoPath;

  /// Sets or updates the latest captured photo path
  static void setLatestPhotoPath(String path) {
    _latestPhotoPath = path;
  }

  /// Saves a photo to the device gallery in the Zipgram album (if supported).
  static Future<bool> saveToGallery(String filePath) async {
    try {
      final file = File(filePath);
      if (!file.existsSync()) {
        debugPrint('File does not exist: $filePath');
        return false;
      }

      // Check or request access permission using Gal
      final hasAccess = await Gal.hasAccess();
      if (!hasAccess) {
        final granted = await Gal.requestAccess();
        if (!granted) {
          debugPrint('Gallery access permission denied');
          return false;
        }
      }

      // Save image to gallery album "Zipgram"
      await Gal.putImage(filePath, album: 'Zipgram');
      _latestPhotoPath = filePath;
      return true;
    } catch (e) {
      debugPrint('Error saving image to gallery: $e');
      return false;
    }
  }

  /// Generates a temporary output path for captured/filtered images
  static Future<String> getTempImagePath({String prefix = 'zipgram_'}) async {
    final tempDir = await getTemporaryDirectory();
    final timestamp = DateTime.now().millisecondsSinceEpoch;
    return '${tempDir.path}/${prefix}_$timestamp.jpg';
  }
}
