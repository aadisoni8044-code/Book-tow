import 'package:flutter/material.dart';
import '../screens/browser/browser_screen.dart';
import '../screens/downloads/downloads_screen.dart';
import '../screens/settings/settings_screen.dart';

class AppRoutes {
  static const String browser = '/';
  static const String settings = '/settings';
  static const String downloads = '/downloads';

  static Map<String, WidgetBuilder> get routes => {
        browser: (context) => const BrowserScreen(),
        settings: (context) => const SettingsScreen(),
        downloads: (context) => const DownloadsScreen(),
      };
}
