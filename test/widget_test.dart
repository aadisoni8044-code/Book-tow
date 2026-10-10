import 'package:flutter_test/flutter_test.dart';
import 'package:snap_cam/models/app_filter.dart';
import 'package:snap_cam/providers/settings_provider.dart';

void main() {
  group('AppFilter Tests', () {
    test('Should contain exactly 10 filters', () {
      expect(AppFilter.allFilters.length, 10);
    });

    test('Filter matrix should have 20 elements (5x4 color matrix)', () {
      for (final filter in AppFilter.allFilters) {
        expect(filter.matrix.length, 20);
      }
    });

    test('getFilter should return requested filter or default', () {
      final warm = AppFilter.getFilter(FilterType.warm);
      expect(warm.type, FilterType.warm);
      expect(warm.name, 'Warm');
    });
  });

  group('SettingsProvider Tests', () {
    test('Default settings values should be correct', () {
      final settings = SettingsProvider();
      expect(settings.flashMode, FlashMode.off);
      expect(settings.gridEnabled, false);
      expect(settings.timerSeconds, 0);
      expect(settings.filterQuality, FilterQuality.high);
      expect(settings.autoSaveToGallery, false);
      expect(settings.isPremiumUser, false);
    });

    test('Flash mode toggling sequence', () {
      final settings = SettingsProvider();
      settings.toggleFlashMode(); // off -> auto
      expect(settings.flashMode, FlashMode.auto);
      settings.toggleFlashMode(); // auto -> on
      expect(settings.flashMode, FlashMode.on);
      settings.toggleFlashMode(); // on -> off
      expect(settings.flashMode, FlashMode.off);
    });

    test('Timer cycling sequence', () {
      final settings = SettingsProvider();
      settings.cycleTimer(); // 0 -> 3
      expect(settings.timerSeconds, 3);
      settings.cycleTimer(); // 3 -> 10
      expect(settings.timerSeconds, 10);
      settings.cycleTimer(); // 10 -> 0
      expect(settings.timerSeconds, 0);
    });

    test('Premium upgrade toggle', () {
      final settings = SettingsProvider();
      settings.setPremiumUser(true);
      expect(settings.isPremiumUser, true);
    });
  });
}
