import 'dart:io';
import 'package:flutter/material.dart';
import 'package:path_provider/path_provider.dart';
import 'package:url_launcher/url_launcher.dart';
import '../models/download_item.dart';

class DownloadProvider with ChangeNotifier {
  final List<DownloadItem> _downloads = [];

  List<DownloadItem> get downloads => List.unmodifiable(_downloads);

  /// Simulated/real download trigger
  Future<void> startDownload(String url, {String? filename}) async {
    final name = filename ?? url.split('/').last.split('?').first;
    final safeName = name.isEmpty ? 'download_${DateTime.now().millisecondsSinceEpoch}.bin' : name;

    Directory dir;
    try {
      dir = await getApplicationDocumentsDirectory();
    } catch (_) {
      dir = Directory.systemTemp;
    }

    final filePath = '${dir.path}/$safeName';
    final id = DateTime.now().millisecondsSinceEpoch.toString();

    final item = DownloadItem(
      id: id,
      filename: safeName,
      url: url,
      filePath: filePath,
      totalBytes: 1024 * 500, // sample size
      downloadedBytes: 0,
      status: DownloadStatus.downloading,
    );

    _downloads.insert(0, item);
    notifyListeners();

    // Simulate progressive download
    for (int i = 1; i <= 5; i++) {
      await Future.delayed(const Duration(milliseconds: 200));
      final idx = _downloads.indexWhere((d) => d.id == id);
      if (idx != -1) {
        final progressBytes = (item.totalBytes * (i / 5)).round();
        final isDone = i == 5;

        // Create dummy file for local open demonstration
        if (isDone) {
          try {
            final file = File(filePath);
            await file.writeAsString('Downloaded private file content from FireZip');
          } catch (_) {}
        }

        _downloads[idx] = _downloads[idx].copyWith(
          downloadedBytes: progressBytes,
          status: isDone ? DownloadStatus.completed : DownloadStatus.downloading,
        );
        notifyListeners();
      }
    }
  }

  Future<void> openFile(DownloadItem item) async {
    final uri = Uri.file(item.filePath);
    if (await canLaunchUrl(uri)) {
      await launchUrl(uri);
    }
  }

  Future<void> deleteFile(DownloadItem item) async {
    try {
      final file = File(item.filePath);
      if (await file.exists()) {
        await file.delete();
      }
    } catch (_) {}
    _downloads.removeWhere((d) => d.id == item.id);
    notifyListeners();
  }

  void clearDownloadList() {
    _downloads.clear();
    notifyListeners();
  }
}
