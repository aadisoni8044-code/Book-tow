import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';

import 'providers/camera_provider.dart';
import 'providers/filter_provider.dart';
import 'providers/settings_provider.dart';
import 'screens/permission_screen.dart';
import 'theme/app_theme.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Set dark status bar & navigation bar icons
  SystemChrome.setSystemUIOverlayStyle(
    const SystemUiOverlayStyle(
      statusBarColor: Colors.transparent,
      statusBarIconBrightness: Brightness.light,
      systemNavigationBarColor: Colors.black,
      systemNavigationBarIconBrightness: Brightness.light,
    ),
  );

  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => SettingsProvider()),
        ChangeNotifierProvider(create: (_) => FilterProvider()),
        ChangeNotifierProvider(create: (_) => CameraProvider()),
      ],
      child: const ZipgramApp(),
    ),
  );
}

class ZipgramApp extends StatelessWidget {
  const ZipgramApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Zipgram',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.darkTheme,
      home: const PermissionScreen(),
    );
  }
}
