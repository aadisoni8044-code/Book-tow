import 'package:flutter/material.dart';

enum AppFilterType {
  original,
  golden,
  arctic,
  mono,
  retro,
  cinema,
  vivid,
  dream,
  shadow,
  airy,
}

class AppFilter {
  final AppFilterType type;
  final String name;
  final String description;
  final IconData icon;
  final List<double> matrix;

  const AppFilter({
    required this.type,
    required this.name,
    required this.description,
    required this.icon,
    required this.matrix,
  });

  static const AppFilter original = AppFilter(
    type: AppFilterType.original,
    name: 'Original',
    description: 'Clean, unaltered original photo',
    icon: Icons.camera_alt_outlined,
    matrix: [
      1, 0, 0, 0, 0,
      0, 1, 0, 0, 0,
      0, 0, 1, 0, 0,
      0, 0, 0, 1, 0,
    ],
  );

  static const AppFilter golden = AppFilter(
    type: AppFilterType.golden,
    name: 'Golden',
    description: 'Warm, sun-kissed golden tones',
    icon: Icons.wb_sunny_outlined,
    matrix: [
      1.2, 0.1, 0.0, 0, 20,
      0.1, 1.1, 0.0, 0, 15,
      0.0, 0.0, 0.8, 0, -10,
      0.0, 0.0, 0.0, 1, 0,
    ],
  );

  static const AppFilter arctic = AppFilter(
    type: AppFilterType.arctic,
    name: 'Arctic',
    description: 'Crisp, cool blue hues',
    icon: Icons.ac_unit,
    matrix: [
      0.8, 0.1, 0.1, 0, -10,
      0.1, 1.0, 0.2, 0, 5,
      0.1, 0.2, 1.3, 0, 25,
      0.0, 0.0, 0.0, 1, 0,
    ],
  );

  static const AppFilter mono = AppFilter(
    type: AppFilterType.mono,
    name: 'Mono',
    description: 'Timeless black & white monochrome',
    icon: Icons.filter_b_and_w,
    matrix: [
      0.2126, 0.7152, 0.0722, 0, 0,
      0.2126, 0.7152, 0.0722, 0, 0,
      0.2126, 0.7152, 0.0722, 0, 0,
      0.0,    0.0,    0.0,    1, 0,
    ],
  );

  static const AppFilter retro = AppFilter(
    type: AppFilterType.retro,
    name: 'Retro',
    description: 'Classic vintage sepia aesthetic',
    icon: Icons.style,
    matrix: [
      0.393, 0.769, 0.189, 0, 10,
      0.349, 0.686, 0.168, 0, 5,
      0.272, 0.534, 0.131, 0, 0,
      0.000, 0.000, 0.000, 1, 0,
    ],
  );

  static const AppFilter cinema = AppFilter(
    type: AppFilterType.cinema,
    name: 'Cinema',
    description: 'Rich cinematic teal & orange contrast',
    icon: Icons.movie_filter,
    matrix: [
      1.3, -0.1, -0.1, 0, 0,
      -0.1, 1.1,  0.1, 0, -5,
      -0.1, 0.2,  1.4, 0, 10,
      0.0,  0.0,  0.0, 1, 0,
    ],
  );

  static const AppFilter vivid = AppFilter(
    type: AppFilterType.vivid,
    name: 'Vivid',
    description: 'Enhanced color vibrancy & depth',
    icon: Icons.auto_awesome,
    matrix: [
      1.4, -0.2, -0.2, 0, 0,
      -0.2, 1.4, -0.2, 0, 0,
      -0.2, -0.2, 1.4, 0, 0,
      0.0,  0.0,  0.0, 1, 0,
    ],
  );

  static const AppFilter dream = AppFilter(
    type: AppFilterType.dream,
    name: 'Dream',
    description: 'Soft, dreamy pastel glow',
    icon: Icons.cloud_outlined,
    matrix: [
      1.0, 0.1, 0.1, 0, 25,
      0.1, 1.0, 0.1, 0, 25,
      0.1, 0.1, 1.1, 0, 30,
      0.0, 0.0, 0.0, 1, 0,
    ],
  );

  static const AppFilter shadow = AppFilter(
    type: AppFilterType.shadow,
    name: 'Shadow',
    description: 'Moody, dramatic dark shadows',
    icon: Icons.brightness_3_outlined,
    matrix: [
      0.8, 0.0, 0.0, 0, -25,
      0.0, 0.8, 0.0, 0, -25,
      0.0, 0.0, 0.9, 0, -20,
      0.0, 0.0, 0.0, 1, 0,
    ],
  );

  static const AppFilter airy = AppFilter(
    type: AppFilterType.airy,
    name: 'Airy',
    description: 'Bright, soft high-key exposure',
    icon: Icons.wb_cloudy_outlined,
    matrix: [
      1.1, 0.05, 0.05, 0, 35,
      0.05, 1.1, 0.05, 0, 35,
      0.05, 0.05, 1.1, 0, 40,
      0.0,  0.0,  0.0, 1, 0,
    ],
  );

  static List<AppFilter> get allFilters => [
        original,
        golden,
        arctic,
        mono,
        retro,
        cinema,
        vivid,
        dream,
        shadow,
        airy,
      ];

  static AppFilter fromType(AppFilterType type) {
    return allFilters.firstWhere(
      (f) => f.type == type,
      orElse: () => original,
    );
  }
}
