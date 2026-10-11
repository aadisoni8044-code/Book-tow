import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:image/image.dart' as img;
import '../models/app_filter.dart';

class FilterParams {
  final String inputPath;
  final String outputPath;
  final AppFilterType filterType;
  final int quality;

  FilterParams({
    required this.inputPath,
    required this.outputPath,
    required this.filterType,
    this.quality = 90,
  });
}

class FilterService {
  /// Applies a filter to an image file at [inputPath] and saves to [outputPath].
  /// Executed in a background isolate to prevent UI stutters on large photos.
  static Future<File> applyFilterToFile({
    required String inputPath,
    required String outputPath,
    required AppFilterType filterType,
    int quality = 90,
  }) async {
    final params = FilterParams(
      inputPath: inputPath,
      outputPath: outputPath,
      filterType: filterType,
      quality: quality,
    );

    final String resultPath = await compute(_processImageIsolate, params);
    return File(resultPath);
  }

  /// Isolate top-level or static function for pixel manipulation
  static Future<String> _processImageIsolate(FilterParams params) async {
    final inputFile = File(params.inputPath);
    if (!inputFile.existsSync()) {
      throw Exception('Input file does not exist: ${params.inputPath}');
    }

    final bytes = await inputFile.readAsBytes();
    if (params.filterType == AppFilterType.original) {
      // Original filter preserves photo intact
      final outputFile = File(params.outputPath);
      await outputFile.writeAsBytes(bytes);
      return params.outputPath;
    }

    final img.Image? decodedImage = img.decodeImage(bytes);
    if (decodedImage == null) {
      throw Exception('Could not decode image at ${params.inputPath}');
    }

    // Retrieve matrix values for selected filter
    final filter = AppFilter.fromType(params.filterType);
    final m = filter.matrix;

    // Process pixels
    final int width = decodedImage.width;
    final int height = decodedImage.height;

    for (int y = 0; y < height; y++) {
      for (int x = 0; x < width; x++) {
        final pixel = decodedImage.getPixel(x, y);
        final num r = pixel.r;
        final num g = pixel.g;
        final num b = pixel.b;
        final num a = pixel.a;

        // Color matrix 4x5 transformation
        final int newR = (m[0] * r + m[1] * g + m[2] * b + m[4]).round().clamp(0, 255);
        final int newG = (m[5] * r + m[6] * g + m[7] * b + m[9]).round().clamp(0, 255);
        final int newB = (m[10] * r + m[11] * g + m[12] * b + m[14]).round().clamp(0, 255);

        decodedImage.setPixelRgba(x, y, newR, newG, newB, a.toInt());
      }
    }

    final encodedJpg = img.encodeJpg(decodedImage, quality: params.quality);
    final outputFile = File(params.outputPath);
    await outputFile.writeAsBytes(encodedJpg);

    return params.outputPath;
  }
}
