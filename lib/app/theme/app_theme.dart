import 'package:flutter/material.dart';

class AppTheme {
  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      scaffoldBackgroundColor: const Color(0xFF0D111A),
      colorScheme: const ColorScheme.dark(
        primary: Color(0xFFFF5E1A),
        secondary: Color(0xFFFFB800),
        surface: Color(0xFF161C28),
        error: Color(0xFFE63946),
        onPrimary: Colors.white,
        onSurface: Color(0xFFF0F4FC),
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: Color(0xFF161C28),
        foregroundColor: Color(0xFFF0F4FC),
        elevation: 0,
        centerTitle: true,
      ),
      cardTheme: CardThemeData(
        color: const Color(0xFF1F2738),
        elevation: 2,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
        ),
      ),
      dialogTheme: DialogThemeData(
        backgroundColor: const Color(0xFF161C28),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20),
        ),
      ),
      fontFamily: 'Roboto',
    );
  }

  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      scaffoldBackgroundColor: const Color(0xFFF4F6FB),
      colorScheme: const ColorScheme.light(
        primary: Color(0xFFFF5E1A),
        secondary: Color(0xFFFFB800),
        surface: Color(0xFFFFFFFF),
        error: Color(0xFFE63946),
        onPrimary: Colors.white,
        onSurface: Color(0xFF0F172A),
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: Color(0xFFFFFFFF),
        foregroundColor: Color(0xFF0F172A),
        elevation: 0,
        centerTitle: true,
      ),
      cardTheme: CardThemeData(
        color: const Color(0xFFFFFFFF),
        elevation: 2,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
        ),
      ),
      dialogTheme: DialogThemeData(
        backgroundColor: const Color(0xFFFFFFFF),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20),
        ),
      ),
      fontFamily: 'Roboto',
    );
  }
}
