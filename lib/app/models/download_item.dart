enum DownloadStatus {
  pending,
  downloading,
  completed,
  failed,
  canceled,
}

class DownloadItem {
  final String id;
  final String filename;
  final String url;
  final String filePath;
  final int totalBytes;
  final int downloadedBytes;
  final DownloadStatus status;
  final DateTime timestamp;

  DownloadItem({
    required this.id,
    required this.filename,
    required this.url,
    required this.filePath,
    this.totalBytes = 0,
    this.downloadedBytes = 0,
    this.status = DownloadStatus.pending,
    DateTime? timestamp,
  }) : timestamp = timestamp ?? DateTime.now();

  double get progress => totalBytes > 0 ? (downloadedBytes / totalBytes) : 0.0;

  DownloadItem copyWith({
    String? id,
    String? filename,
    String? url,
    String? filePath,
    int? totalBytes,
    int? downloadedBytes,
    DownloadStatus? status,
    DateTime? timestamp,
  }) {
    return DownloadItem(
      id: id ?? this.id,
      filename: filename ?? this.filename,
      url: url ?? this.url,
      filePath: filePath ?? this.filePath,
      totalBytes: totalBytes ?? this.totalBytes,
      downloadedBytes: downloadedBytes ?? this.downloadedBytes,
      status: status ?? this.status,
      timestamp: timestamp ?? this.timestamp,
    );
  }
}
