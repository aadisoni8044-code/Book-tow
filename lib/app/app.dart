import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../browser/tab_manager.dart';
import '../privacy/privacy_session_manager.dart';
import '../services/download_service.dart';
import '../services/lifecycle_service.dart';
import '../theme/app_theme.dart';
import 'routes.dart';

class FireZipApp extends StatefulWidget {
  const FireZipApp({super.key});

  @override
  State<FireZipApp> createState() => _FireZipAppState();
}

class _FireZipAppState extends State<FireZipApp> {
  late PrivacySessionManager _privacySessionManager;
  late TabManager _tabManager;
  late DownloadService _downloadService;
  late LifecycleService _lifecycleService;

  @override
  void initState() {
    super.initState();
    _privacySessionManager = PrivacySessionManager();
    _tabManager = TabManager(sessionManager: _privacySessionManager);
    _downloadService = DownloadService();
    _lifecycleService = LifecycleService(sessionManager: _privacySessionManager);
    _lifecycleService.initialize();
  }

  @override
  void dispose() {
    _lifecycleService.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider<PrivacySessionManager>.value(value: _privacySessionManager),
        ChangeNotifierProvider<TabManager>.value(value: _tabManager),
        ChangeNotifierProvider<DownloadService>.value(value: _downloadService),
      ],
      child: MaterialApp(
        title: 'FireZip Browser',
        debugShowCheckedModeBanner: false,
        theme: AppTheme.darkTheme,
        routes: AppRoutes.routes,
        initialRoute: AppRoutes.browser,
      ),
    );
  }
}
