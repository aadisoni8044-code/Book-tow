import 'package:flutter/material.dart';
import '../models/app_filter.dart';
import '../theme/app_theme.dart';

class FilterCarousel extends StatelessWidget {
  final AppFilter selectedFilter;
  final ValueChanged<AppFilter> onFilterSelected;

  const FilterCarousel({
    super.key,
    required this.selectedFilter,
    required this.onFilterSelected,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 100,
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        physics: const BouncingScrollPhysics(),
        padding: const EdgeInsets.symmetric(horizontal: 16),
        itemCount: AppFilter.allFilters.length,
        itemBuilder: (context, index) {
          final filter = AppFilter.allFilters[index];
          final isSelected = filter.type == selectedFilter.type;

          return GestureDetector(
            onTap: () => onFilterSelected(filter),
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 10),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Container(
                    width: 58,
                    height: 58,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      border: Border.all(
                        color: isSelected
                            ? AppTheme.primaryYellow
                            : Colors.white.withOpacity(0.5),
                        width: isSelected ? 3.0 : 1.5,
                      ),
                      boxShadow: isSelected
                          ? [
                              BoxShadow(
                                color: AppTheme.primaryYellow.withOpacity(0.5),
                                blurRadius: 10,
                                spreadRadius: 2,
                              )
                            ]
                          : [],
                    ),
                    child: ClipOval(
                      child: ColorFiltered(
                        colorFilter: filter.colorFilter,
                        child: Container(
                          decoration: BoxDecoration(
                            gradient: LinearGradient(
                              begin: Alignment.topLeft,
                              end: Alignment.bottomRight,
                              colors: [
                                Colors.purple.shade400,
                                Colors.amber.shade300,
                                Colors.teal.shade400,
                              ],
                            ),
                          ),
                          child: Icon(
                            _getFilterIcon(filter.type),
                            color: Colors.white.withOpacity(0.9),
                            size: 24,
                          ),
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(height: 6),
                  Text(
                    filter.name,
                    style: TextStyle(
                      fontSize: 12,
                      fontWeight:
                          isSelected ? FontWeight.bold : FontWeight.normal,
                      color: isSelected
                          ? AppTheme.primaryYellow
                          : Colors.white.withOpacity(0.8),
                    ),
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }

  IconData _getFilterIcon(FilterType type) {
    switch (type) {
      case FilterType.original:
        return Icons.wb_sunny_outlined;
      case FilterType.warm:
        return Icons.thermostat;
      case FilterType.cool:
        return Icons.ac_unit;
      case FilterType.mono:
        return Icons.filter_b_and_w;
      case FilterType.retro:
        return Icons.camera_roll_outlined;
      case FilterType.cinema:
        return Icons.movie_filter_outlined;
      case FilterType.vivid:
        return Icons.auto_awesome;
      case FilterType.dream:
        return Icons.cloud_outlined;
      case FilterType.shadow:
        return Icons.brightness_3_outlined;
      case FilterType.airy:
        return Icons.air;
    }
  }
}
