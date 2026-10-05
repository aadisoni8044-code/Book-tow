import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:firezip/app/utils/url_helper.dart';
import 'package:firezip/app/models/search_engine.dart';
import 'package:firezip/app/providers/browser_provider.dart';
import 'package:firezip/app/providers/settings_provider.dart';
import 'package:firezip/app/providers/download_provider.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  setUp(() {
    SharedPreferences.setMockInitialValues({});
  });

  group('UrlHelper Tests', () {
    test('Formats valid https URL', () {
      final formatted = UrlHelper.formatUrl('https://flutter.dev');
      expect(formatted, equals('https://flutter.dev'));
    });

    test('Adds https schema to domain name', () {
      final formatted = UrlHelper.formatUrl('example.com');
      expect(formatted, equals('https://example.com'));
    });

    test('Converts search term to DuckDuckGo search URL', () {
      final formatted = UrlHelper.formatUrl('flutter browser app');
      expect(formatted, startsWith('https://duckduckgo.com/?q=flutter'));
    });

    test('Checks HTTPS security', () {
      expect(UrlHelper.isSecure('https://secure.site'), isTrue);
      expect(UrlHelper.isSecure('http://insecure.site'), isFalse);
    });

    test('Extracts display domain', () {
      expect(UrlHelper.getDisplayDomain('https://sub.domain.org/path?q=1'), equals('sub.domain.org'));
    });
  });

  group('SettingsProvider Tests', () {
    test('Default values are private and secure', () {
      final settings = SettingsProvider();
      expect(settings.privateMode, isTrue);
      expect(settings.doNotTrack, isTrue);
      expect(settings.blockThirdPartyCookies, isTrue);
    });

    test('Toggle preferences', () async {
      final settings = SettingsProvider();
      await settings.toggleDoNotTrack(false);
      expect(settings.doNotTrack, isFalse);

      await settings.setSearchEngine(SearchEngine.defaultEngines[1]); // Google
      expect(settings.selectedSearchEngine.id, equals('google'));
    });
  });

  group('BrowserProvider Tests', () {
    test('Initializes with 1 private tab', () {
      final browser = BrowserProvider();
      expect(browser.tabs.length, equals(1));
      expect(browser.activeTabIndex, equals(0));
      expect(browser.activeTab?.isPrivate, isTrue);
    });

    test('New tab creation and tab switching', () {
      final browser = BrowserProvider();
      browser.newTab(initialUrl: 'https://dart.dev');
      expect(browser.tabs.length, equals(2));
      expect(browser.activeTabIndex, equals(1));
      expect(browser.activeTab?.url, equals('https://dart.dev'));
    });

    test('Close tab', () {
      final browser = BrowserProvider();
      browser.newTab(initialUrl: 'https://flutter.dev');
      browser.closeTab(1);
      expect(browser.tabs.length, equals(1));
    });

    test('Close all tabs creates fresh new tab', () {
      final browser = BrowserProvider();
      browser.newTab(initialUrl: 'https://flutter.dev');
      browser.closeAllTabs();
      expect(browser.tabs.length, equals(1));
      expect(browser.activeTab?.url, equals('about:blank'));
    });
  });

  group('DownloadProvider Tests', () {
    test('Start download creates download item', () async {
      final downloadProvider = DownloadProvider();
      expect(downloadProvider.downloads.isEmpty, isTrue);

      await downloadProvider.startDownload('https://example.com/file.pdf');
      expect(downloadProvider.downloads.isNotEmpty, isTrue);
      expect(downloadProvider.downloads.first.filename, equals('file.pdf'));
    });
  });
}
