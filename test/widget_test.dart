import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';
import 'package:zipgram/providers/camera_provider.dart';
import 'package:zipgram/providers/filter_provider.dart';
import 'package:zipgram/providers/settings_provider.dart';
import 'package:zipgram/screens/permission_screen.dart';
import 'package:zipgram/widgets/zipgram_logo.dart';

void main() {
  testWidgets('Renders Zipgram logo widget correctly', (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: Center(
            child: ZipgramLogo(),
          ),
        ),
      ),
    );

    expect(find.byType(ZipgramLogo), findsOneWidget);
  });

  testWidgets('Renders PermissionScreen with onboarding text and button', (WidgetTester tester) async {
    await tester.pumpWidget(
      MultiProvider(
        providers: [
          ChangeNotifierProvider(create: (_) => SettingsProvider()),
          ChangeNotifierProvider(create: (_) => FilterProvider()),
          ChangeNotifierProvider(create: (_) => CameraProvider()),
        ],
        child: const MaterialApp(
          home: PermissionScreen(),
        ),
      ),
    );

    expect(find.text('Camera & Gallery Access'), findsOneWidget);
    expect(find.text('Allow Camera & Start'), findsOneWidget);
  });
}
