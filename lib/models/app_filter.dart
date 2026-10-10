import 'package:flutter/material.dart';

enum FilterType {
  original,
  warm,
  cool,
  mono,
  retro,
  cinema,
  vivid,
  dream,
  shadow,
  airy,
}

class AppFilter {
  final FilterType type;
  final String name;
  final String description;
  final List<double> matrix;

  const AppFilter({
    required this.type,
    required this.name,
    required this.description,
    required this.matrix,
  });

  ColorFilter get colorFilter => ColorFilter.matrix(matrix);

  static const List<AppFilter> allFilters = [
    AppFilter(
      type: FilterType.original,
      name: 'Original',
      description: 'Natural look',
      matrix: [
        1, 0, 0, 0, 0,
        0, 1, 0, 0, 0,
        0, 0, 1, 0, 0,
        0, 0, 0, 1, 0,
      ],
    ),
    AppFilter(
      type: FilterType.warm,
      name: 'Warm',
      description: 'Golden hour feel',
      matrix: [
        1.2, 0.0, 0.0, 0.0, 15.0,
        0.0, 1.1, 0.0, 0.0, 8.0,
        0.0, 0.0, 0.8, 0.0, -12.0,
        0.0, 0.0, 0.0, 1.0, 0.0,
      ],
    ),
    AppFilter(
      type: FilterType.cool,
      name: 'Cool',
      description: 'Fresh blue tone',
      matrix: [
        0.8, 0.0, 0.0, 0.0, -8.0,
        0.0, 1.0, 0.0, 0.0, 5.0,
        0.0, 0.0, 1.25, 0.0, 18.0,
        0.0, 0.0, 0.0, 1.0, 0.0,
      ],
    ),
    AppFilter(
      type: FilterType.mono,
      name: 'Mono',
      description: 'Classic monochrome',
      matrix: [
        0.33, 0.59, 0.11, 0.0, 0.0,
        0.33, 0.59, 0.11, 0.0, 0.0,
        0.33, 0.59, 0.11, 0.0, 0.0,
        0.0,  0.0,  0.0,  1.0, 0.0,
      ],
    ),
    AppFilter(
      type: FilterType.retro,
      name: 'Retro',
      description: 'Vintage film',
      matrix: [
        0.393, 0.769, 0.189, 0.0, 15.0,
        0.349, 0.686, 0.168, 0.0, 5.0,
        0.272, 0.534, 0.131, 0.0, -10.0,
        0.0,   0.0,   0.0,   1.0, 0.0,
      ],
    ),
    AppFilter(
      type: FilterType.cinema,
      name: 'Cinema',
      description: 'Teal & Orange cinematic',
      matrix: [
        1.15, 0.0,  0.0,  0.0, 12.0,
        0.0,  0.95, 0.0,  0.0, 0.0,
        0.0,  0.0,  1.2,  0.0, 20.0,
        0.0,  0.0,  0.0,  1.0, 0.0,
      ],
    ),
    AppFilter(
      type: FilterType.vivid,
      name: 'Vivid',
      description: 'High pop & contrast',
      matrix: [
        1.3, 0.0, 0.0, 0.0, -15.0,
        0.0, 1.3, 0.0, 0.0, -15.0,
        0.0, 0.0, 1.3, 0.0, -15.0,
        0.0, 0.0, 0.0, 1.0, 0.0,
      ],
    ),
    AppFilter(
      type: FilterType.dream,
      name: 'Dream',
      description: 'Ethereal pastel glow',
      matrix: [
        1.1, 0.1, 0.0, 0.0, 20.0,
        0.0, 1.0, 0.1, 0.0, 15.0,
        0.1, 0.0, 1.2, 0.0, 25.0,
        0.0, 0.0, 0.0, 1.0, 0.0,
      ],
    ),
    AppFilter(
      type: FilterType.shadow,
      name: 'Shadow',
      description: 'Moody dark contrast',
      matrix: [
        0.8, 0.0, 0.0,  0.0, -25.0,
        0.0, 0.8, 0.0,  0.0, -25.0,
        0.0, 0.0, 0.85, 0.0, -20.0,
        0.0, 0.0, 0.0,  1.0, 0.0,
      ],
    ),
    AppFilter(
      type: FilterType.airy,
      name: 'Airy',
      description: 'Bright & soft background',
      matrix: [
        1.1, 0.0, 0.0,  0.0, 25.0,
        0.0, 1.1, 0.0,  0.0, 25.0,
        0.0, 0.0, 1.15, 0.0, 30.0,
        0.0, 0.0, 0.0,  1.0, 0.0,
      ],
    ),
  ];

  static AppFilter get defaultFilter => allFilters[0];

  static AppFilter getFilter(FilterType type) {
    return allFilters.firstWhere(
      (f) => f.type == type,
      orElse: () => defaultFilter,
    );
  }
}
