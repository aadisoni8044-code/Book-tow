import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/download_item.dart';
import '../providers/download_provider.dart';
import '../theme/firezip_colors.dart';

class DownloadsScreen extends StatelessWidget {
  const DownloadsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final downloadProvider = Provider.of<DownloadProvider>(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Download Manager'),
        actions: [
          if (downloadProvider.downloads.isNotEmpty)
            IconButton(
              icon: const Icon(Icons.delete_outline),
              tooltip: 'Clear List',
              onPressed: () => downloadProvider.clearDownloadList(),
            ),
        ],
      ),
      body: Column(
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            color: FireZipColors.flameOrange.withValues(alpha: 0.1),
            child: const Row(
              children: [
                Icon(Icons.info_outline, size: 18, color: FireZipColors.flameOrange),
                SizedBox(width: 8),
                Expanded(
                  child: Text(
                    'Downloaded files remain stored on device disk and are managed by your device OS.',
                    style: TextStyle(fontSize: 12),
                  ),
                ),
              ],
            ),
          ),
          Expanded(
            child: downloadProvider.downloads.isEmpty
                ? const Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.download_done_rounded, size: 64, color: Colors.grey),
                        SizedBox(height: 12),
                        Text('No active or recent downloads', style: TextStyle(color: Colors.grey)),
                      ],
                    ),
                  )
                : ListView.separated(
                    padding: const EdgeInsets.all(16),
                    itemCount: downloadProvider.downloads.length,
                    separatorBuilder: (_, __) => const SizedBox(height: 12),
                    itemBuilder: (context, index) {
                      final item = downloadProvider.downloads[index];
                      return Card(
                        child: ListTile(
                          leading: Icon(
                            item.status == DownloadStatus.completed
                                ? Icons.insert_drive_file
                                : Icons.downloading,
                            color: FireZipColors.flameOrange,
                          ),
                          title: Text(item.filename, style: const TextStyle(fontWeight: FontWeight.bold)),
                          subtitle: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(item.url, maxLines: 1, overflow: TextOverflow.ellipsis),
                              if (item.status == DownloadStatus.downloading) ...[
                                const SizedBox(height: 4),
                                LinearProgressIndicator(value: item.progress),
                              ],
                            ],
                          ),
                          trailing: Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              if (item.status == DownloadStatus.completed)
                                IconButton(
                                  icon: const Icon(Icons.open_in_new, size: 20),
                                  onPressed: () => downloadProvider.openFile(item),
                                ),
                              IconButton(
                                icon: const Icon(Icons.delete_forever, size: 20, color: Colors.redAccent),
                                onPressed: () => downloadProvider.deleteFile(item),
                              ),
                            ],
                          ),
                        ),
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }
}
