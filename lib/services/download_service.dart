import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:path_provider/path_provider.dart';
import 'package:http/http.dart' as http;

enum DownloadStatus { downloading, completed, failed }

class DownloadItem {
  final String id;
  final String filename;
  final String url;
  final String filePath;
  final int fileSize;
  final DateTime timestamp;
  DownloadStatus status;

  DownloadItem({
    required this.id,
    required this.filename,
    required this.url,
    required this.filePath,
    required this.fileSize,
    required this.timestamp,
    this.status = DownloadStatus.completed,
  });
}

class DownloadService extends ChangeNotifier {
  final List<DownloadItem> _downloads = [];

  List<DownloadItem> get downloads => List.unmodifiable(_downloads);

  /// Downloads a file from [url] and stores it in device temporary/downloads directory.
  Future<DownloadItem?> downloadFile(String url, {String? suggestedFilename}) async {
    try {
      final uri = Uri.parse(url);
      final filename = suggestedFilename ?? (uri.pathSegments.isNotEmpty ? uri.pathSegments.last : 'download_${DateTime.now().millisecondsSinceEpoch}');

      final dir = await getApplicationDocumentsDirectory();
      final filePath = '${dir.path}/$filename';

      final id = 'dl_${DateTime.now().millisecondsSinceEpoch}';
      final item = DownloadItem(
        id: id,
        filename: filename,
        url: url,
        filePath: filePath,
        fileSize: 0,
        timestamp: DateTime.now(),
        status: DownloadStatus.downloading,
      );

      _downloads.insert(0, item);
      notifyListeners();

      final response = await http.get(uri);
      if (response.statusCode == 200) {
        final file = File(filePath);
        await file.writeAsBytes(response.bodyBytes);
        item.status = DownloadStatus.completed;
        _downloads[_downloads.indexWhere((d) => d.id == id)] = DownloadItem(
          id: id,
          filename: filename,
          url: url,
          filePath: filePath,
          fileSize: response.bodyBytes.length,
          timestamp: item.timestamp,
          status: DownloadStatus.completed,
        );
        notifyListeners();
        debugPrint('[FireZip] Download complete: $filename at $filePath');
        return item;
      } else {
        item.status = DownloadStatus.failed;
        notifyListeners();
        return null;
      }
    } catch (e) {
      debugPrint('[FireZip] Download failed: $e');
      return null;
    }
  }

  /// Manually deletes a downloaded file from device disk.
  Future<bool> deleteFile(String id) async {
    final index = _downloads.indexWhere((d) => d.id == id);
    if (index == -1) return false;

    final item = _downloads[index];
    try {
      final file = File(item.filePath);
      if (await file.exists()) {
        await file.delete();
      }
      _downloads.removeAt(index);
      notifyListeners();
      debugPrint('[FireZip] Deleted download file: ${item.filePath}');
      return true;
    } catch (e) {
      debugPrint('[FireZip] Error deleting file: $e');
      return false;
    }
  }

  void clearDownloadHistory() {
    _downloads.clear();
    notifyListeners();
  }
}
