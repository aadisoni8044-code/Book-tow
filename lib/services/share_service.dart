import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:share_plus/share_plus.dart';

class ShareService {
  /// Shares a photo file via Android's native system share sheet.
  static Future<bool> sharePhoto(String filePath, {String? caption}) async {
    try {
      final file = File(filePath);
      if (!file.existsSync()) {
        debugPrint('Cannot share non-existent file: $filePath');
        return false;
      }

      final xFile = XFile(filePath, mimeType: 'image/jpeg');
      final result = await Share.shareXFiles(
        [xFile],
        text: caption ?? 'Captured with Zipgram Camera',
        subject: 'Zipgram Photo',
      );

      return result.status != ShareResultStatus.dismissed;
    } catch (e) {
      debugPrint('Error sharing photo: $e');
      return false;
    }
  }
}
