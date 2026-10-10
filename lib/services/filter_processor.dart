import 'dart:io';
import 'dart:typed_data';
import 'package:image/image.dart' as img;
import '../models/app_filter.dart';

class FilterProcessor {
  /// Applies a given [AppFilter] to raw image bytes and returns encoded JPEG bytes.
  static Future<Uint8List> processImageBytes(
    Uint8List originalBytes,
    AppFilter filter, {
    int quality = 95,
  }) async {
    if (filter.type == FilterType.original) {
      return originalBytes;
    }

    final img.Image? decoded = img.decodeImage(originalBytes);
    if (decoded == null) {
      return originalBytes;
    }

    final List<double> m = filter.matrix;

    // Apply color matrix pixel by pixel
    for (int y = 0; y < decoded.height; y++) {
      for (int x = 0; x < decoded.width; x++) {
        final pixel = decoded.getPixel(x, y);
        final double r = pixel.r.toDouble();
        final double g = pixel.g.toDouble();
        final double b = pixel.b.toDouble();
        final double a = pixel.a.toDouble();

        final double newR = (m[0] * r + m[1] * g + m[2] * b + m[3] * a + m[4]).clamp(0.0, 255.0);
        final double newG = (m[5] * r + m[6] * g + m[7] * b + m[8] * a + m[9]).clamp(0.0, 255.0);
        final double newB = (m[10] * r + m[11] * g + m[12] * b + m[13] * a + m[14]).clamp(0.0, 255.0);
        final double newA = (m[15] * r + m[16] * g + m[17] * b + m[18] * a + m[19]).clamp(0.0, 255.0);

        decoded.setPixelRgb(x, y, newR.toInt(), newG.toInt(), newB.toInt());
      }
    }

    return Uint8List.fromList(img.encodeJpg(decoded, quality: quality));
  }

  /// Processes an image file on disk and writes the processed output to [outputPath].
  static Future<File> processImageFile(
    File inputFile,
    File outputFile,
    AppFilter filter, {
    int quality = 95,
  }) async {
    final Uint8List inputBytes = await inputFile.readAsBytes();
    final Uint8List outputBytes = await processImageBytes(
      inputBytes,
      filter,
      quality: quality,
    );
    await outputFile.writeAsBytes(outputBytes);
    return outputFile;
  }
}
