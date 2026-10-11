import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:image/image.dart' as img;
import 'package:zipgram/models/app_filter.dart';
import 'package:zipgram/services/filter_service.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('AppFilter Tests', () {
    test('Verify all 10 required photo filters are defined', () {
      final filters = AppFilter.allFilters;
      expect(filters.length, equals(10));

      final filterTypes = filters.map((f) => f.type).toSet();
      expect(filterTypes.contains(AppFilterType.original), isTrue);
      expect(filterTypes.contains(AppFilterType.golden), isTrue);
      expect(filterTypes.contains(AppFilterType.arctic), isTrue);
      expect(filterTypes.contains(AppFilterType.mono), isTrue);
      expect(filterTypes.contains(AppFilterType.retro), isTrue);
      expect(filterTypes.contains(AppFilterType.cinema), isTrue);
      expect(filterTypes.contains(AppFilterType.vivid), isTrue);
      expect(filterTypes.contains(AppFilterType.dream), isTrue);
      expect(filterTypes.contains(AppFilterType.shadow), isTrue);
      expect(filterTypes.contains(AppFilterType.airy), isTrue);
    });

    test('Verify all filter matrices are valid 4x5 matrices (20 elements)', () {
      for (final filter in AppFilter.allFilters) {
        expect(filter.matrix.length, equals(20), reason: '${filter.name} matrix length invalid');
      }
    });

    test('FilterService applies Mono B&W filter transformation to image file', () async {
      // Create a temporary test image
      final tempDir = Directory.systemTemp.createTempSync('zipgram_test_');
      final inputPath = '${tempDir.path}/input.jpg';
      final outputPath = '${tempDir.path}/output.jpg';

      final testImage = img.Image(width: 50, height: 50);
      for (int y = 0; y < 50; y++) {
        for (int x = 0; x < 50; x++) {
          testImage.setPixelRgb(x, y, 200, 100, 50); // Orange color
        }
      }
      final inputBytes = img.encodeJpg(testImage);
      await File(inputPath).writeAsBytes(inputBytes);

      // Apply Mono filter
      final outputFile = await FilterService.applyFilterToFile(
        inputPath: inputPath,
        outputPath: outputPath,
        filterType: AppFilterType.mono,
        quality: 90,
      );

      expect(outputFile.existsSync(), isTrue);

      final resultBytes = await outputFile.readAsBytes();
      final resultImage = img.decodeImage(resultBytes);
      expect(resultImage, isNotNull);

      // In Mono grayscale, R, G, B values of processed pixels should be equal
      final pixel = resultImage!.getPixel(25, 25);
      expect((pixel.r - pixel.g).abs(), lessThanOrEqualTo(2));
      expect((pixel.g - pixel.b).abs(), lessThanOrEqualTo(2));

      tempDir.deleteSync(recursive: true);
    });
  });
}
