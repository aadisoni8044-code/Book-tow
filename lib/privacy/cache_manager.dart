import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:path_provider/path_provider.dart';
import 'package:webview_flutter/webview_flutter.dart';

class FireZipCacheManager {
  /// Clears cache for a given [WebViewController] and temporary cache directories.
  Future<bool> clearCache([WebViewController? controller]) async {
    bool success = true;
    try {
      if (controller != null) {
        await controller.clearCache();
      }

      // Also clean temporary directory cache files if possible
      final Directory tempDir = await getTemporaryDirectory();
      if (await tempDir.exists()) {
        final List<FileSystemEntity> entities = tempDir.listSync(recursive: false);
        for (final entity in entities) {
          try {
            if (entity is File) {
              await entity.delete();
            } else if (entity is Directory) {
              await entity.delete(recursive: true);
            }
          } catch (_) {
            // Ignore individual file locking errors during temp cleanup
          }
        }
      }
      debugPrint('[FireZip] Web cache and temporary cache directory cleared.');
    } catch (e) {
      debugPrint('[FireZip] Error clearing cache: $e');
      success = false;
    }
    return success;
  }
}
