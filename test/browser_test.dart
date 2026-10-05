import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

import 'package:firezip/app/app.dart';
import 'package:firezip/browser/browser_controller.dart';
import 'package:firezip/browser/tab_manager.dart';
import 'package:firezip/models/browser_tab.dart';
import 'package:firezip/privacy/privacy_session_manager.dart';
import 'package:firezip/screens/error/error_screen.dart';
import 'package:firezip/screens/home/home_screen.dart';
import 'package:firezip/screens/settings/settings_screen.dart';
import 'package:firezip/services/download_service.dart';
import 'package:firezip/widgets/logo/firezip_logo.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('BrowserController Unit Tests', () {
    test('parseInputUrl correctly handles empty and home scheme', () {
      expect(BrowserController.parseInputUrl(''), 'firezip://home');
      expect(BrowserController.parseInputUrl('   '), 'firezip://home');
      expect(BrowserController.parseInputUrl('firezip://home'), 'firezip://home');
      expect(BrowserController.parseInputUrl('about:blank'), 'about:blank');
    });

    test('parseInputUrl formats valid web domains into HTTPS URLs', () {
      expect(BrowserController.parseInputUrl('example.com'), 'https://example.com');
      expect(BrowserController.parseInputUrl('https://flutter.dev'), 'https://flutter.dev');
      expect(BrowserController.parseInputUrl('http://localhost:8080'), 'http://localhost:8080');
      expect(BrowserController.parseInputUrl('wikipedia.org/wiki/Privacy'), 'https://wikipedia.org/wiki/Privacy');
    });

    test('parseInputUrl routes search terms to DuckDuckGo', () {
      expect(
        BrowserController.parseInputUrl('privacy web browser'),
        'https://duckduckgo.com/?q=privacy%20web%20browser',
      );
      expect(
        BrowserController.parseInputUrl('what is firezip'),
        'https://duckduckgo.com/?q=what%20is%20firezip',
      );
    });

    test('isSecureUrl detects HTTPS correctly', () {
      expect(BrowserController.isSecureUrl('https://secure.org'), true);
      expect(BrowserController.isSecureUrl('http://insecure.org'), false);
      expect(BrowserController.isSecureUrl('firezip://home'), false);
    });

    test('mapError correctly classifies network & web errors', () {
      expect(BrowserController.mapError(-2, 'net::ERR_NAME_NOT_RESOLVED'), WebErrorType.noInternet);
      expect(BrowserController.mapError(-6, 'net::ERR_CONNECTION_REFUSED'), WebErrorType.connectionError);
      expect(BrowserController.mapError(-1200, 'SSL Certificate Error'), WebErrorType.sslError);
      expect(BrowserController.mapError(404, 'Not Found'), WebErrorType.websiteUnavailable);
    });
  });

  group('PrivacySessionManager Unit Tests', () {
    test('createSession initializes a fresh temporary session', () {
      final psm = PrivacySessionManager();
      final session = psm.currentSession;
      expect(session, isNotNull);
      expect(session!.sessionId.startsWith('fz_session_'), true);
    });

    test('clearSession resets session state and creates a new session ID', () async {
      final psm = PrivacySessionManager();
      final oldId = psm.currentSession?.sessionId;

      await psm.clearSession();

      final newId = psm.currentSession?.sessionId;
      expect(newId, isNotNull);
      expect(newId, isNot(equals(oldId)));
      expect(psm.lastCleanupTime, isNotNull);
    });

    test('updateSettings updates privacy controls', () {
      final psm = PrivacySessionManager();
      psm.updateSettings(
        blockThirdPartyCookies: false,
        doNotTrack: false,
        javaScriptEnabled: false,
        popUpBlocking: false,
      );

      expect(psm.blockThirdPartyCookies, false);
      expect(psm.doNotTrack, false);
      expect(psm.javaScriptEnabled, false);
      expect(psm.popUpBlocking, false);
    });
  });

  group('TabManager Unit Tests', () {
    test('initializes with a default home tab', () {
      final psm = PrivacySessionManager();
      final tm = TabManager(sessionManager: psm);

      expect(tm.tabs.length, 1);
      expect(tm.activeTab?.url, 'firezip://home');
    });

    test('addTab creates and selects new tab', () {
      final psm = PrivacySessionManager();
      final tm = TabManager(sessionManager: psm);

      tm.addTab(url: 'https://example.com', title: 'Example');
      expect(tm.tabs.length, 2);
      expect(tm.activeTabIndex, 1);
      expect(tm.activeTab?.url, 'https://example.com');
    });

    test('closeTab closes tab and handles active index', () {
      final psm = PrivacySessionManager();
      final tm = TabManager(sessionManager: psm);

      final tab2 = tm.addTab(url: 'https://example.com', title: 'Example');
      expect(tm.tabs.length, 2);

      tm.closeTab(tab2.id);
      expect(tm.tabs.length, 1);
      expect(tm.activeTabIndex, 0);
    });

    test('closeAllTabs clears tabs, triggers session cleanup, and restores home tab', () async {
      final psm = PrivacySessionManager();
      final tm = TabManager(sessionManager: psm);

      tm.addTab(url: 'https://example.com', title: 'Example');
      tm.addTab(url: 'https://flutter.dev', title: 'Flutter');
      expect(tm.tabs.length, 3);

      await tm.closeAllTabs();

      expect(tm.tabs.length, 1);
      expect(tm.activeTab?.url, 'firezip://home');
    });
  });

  group('DownloadService Unit Tests', () {
    test('initializes with empty downloads and allows manual clear', () {
      final ds = DownloadService();
      expect(ds.downloads, isEmpty);

      ds.clearDownloadHistory();
      expect(ds.downloads, isEmpty);
    });
  });

  group('UI & Widget Tests', () {
    testWidgets('FireZipLogo renders logo and brand text', (WidgetTester tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: FireZipLogo(size: 100, showText: true),
          ),
        ),
      );

      expect(find.text('FireZip'), findsOneWidget);
      expect(find.text('FAST • TEMPORARY • PRIVATE'), findsOneWidget);
    });

    testWidgets('HomeScreen displays search bar and private session indicator', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: HomeScreen(
              onNavigate: (_) {},
              onOpenSettings: () {},
              onOpenDownloads: () {},
              onOpenTabs: () {},
            ),
          ),
        ),
      );

      expect(find.text('FireZip'), findsOneWidget);
      expect(find.text('Search or enter website'), findsOneWidget);
      expect(find.textContaining('Private Session Active'), findsOneWidget);
    });

    testWidgets('SettingsScreen displays Privacy & Security controls and honest disclaimer', (WidgetTester tester) async {
      final psm = PrivacySessionManager();

      await tester.pumpWidget(
        ChangeNotifierProvider<PrivacySessionManager>.value(
          value: psm,
          child: const MaterialApp(
            home: SettingsScreen(),
          ),
        ),
      );

      expect(find.text('Privacy & Security'), findsOneWidget);
      expect(find.text('Private Session: ON'), findsOneWidget);
      expect(find.text('Clear Current Session'), findsOneWidget);
      expect(find.text('Clear Cookies'), findsOneWidget);
      expect(find.text('Block Third-Party Cookies'), findsOneWidget);
      expect(find.textContaining('FireZip does not retain your browsing history'), findsOneWidget);
    });

    testWidgets('FireZipErrorScreen renders error title and retry buttons', (WidgetTester tester) async {
      bool tryAgainPressed = false;
      bool goHomePressed = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: FireZipErrorScreen(
              errorType: WebErrorType.noInternet,
              onTryAgain: () => tryAgainPressed = true,
              onGoHome: () => goHomePressed = true,
            ),
          ),
        ),
      );

      expect(find.text('No Internet Connection'), findsOneWidget);
      expect(find.text('Try Again'), findsOneWidget);
      expect(find.text('Go Home'), findsOneWidget);

      await tester.tap(find.text('Try Again'));
      expect(tryAgainPressed, true);

      await tester.tap(find.text('Go Home'));
      expect(goHomePressed, true);
    });

    testWidgets('FireZipApp boots successfully and displays home view', (WidgetTester tester) async {
      await tester.pumpWidget(const FireZipApp());
      await tester.pump();
      await tester.pump(const Duration(milliseconds: 500));

      expect(find.text('FireZip'), findsAtLeast(1));
      expect(find.text('Search or enter website'), findsAtLeast(1));
    });
  });
}
