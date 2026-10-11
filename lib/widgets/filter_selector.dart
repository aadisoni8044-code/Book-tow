import 'package:flutter/material.dart';

import '../models/app_filter.dart';
import '../theme/app_colors.dart';

class FilterSelector extends StatelessWidget {
  final AppFilter selectedFilter;
  final ValueChanged<AppFilter> onFilterSelected;

  const FilterSelector({
    super.key,
    required this.selectedFilter,
    required this.onFilterSelected,
  });

  @override
  Widget build(BuildContext context) {
    final filters = AppFilter.allFilters;

    return SizedBox(
      height: 90,
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        padding: const EdgeInsets.symmetric(horizontal: 16),
        itemCount: filters.length,
        itemBuilder: (context, index) {
          final filter = filters[index];
          final isSelected = filter.type == selectedFilter.type;

          return Padding(
            padding: const EdgeInsets.only(right: 12),
            child: GestureDetector(
              onTap: () => onFilterSelected(filter),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  AnimatedContainer(
                    duration: const Duration(milliseconds: 200),
                    width: 58,
                    height: 58,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      border: Border.all(
                        color: isSelected
                            ? AppColors.primaryBlue
                            : AppColors.inactiveBorder,
                        width: isSelected ? 3.0 : 1.5,
                      ),
                      boxShadow: isSelected
                          ? [
                              BoxShadow(
                                color: AppColors.primaryBlue.withValues(alpha: 0.5),
                                blurRadius: 10,
                                spreadRadius: 1,
                              )
                            ]
                          : [],
                    ),
                    child: ColorFiltered(
                      colorFilter: ColorFilter.matrix(filter.matrix),
                      child: ClipOval(
                        child: Container(
                          color: AppColors.darkCard,
                          child: Icon(
                            filter.icon,
                            color: isSelected ? Colors.white : AppColors.textSecondary,
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
                      color: isSelected ? AppColors.primaryBlue : AppColors.textSecondary,
                      fontSize: 12,
                      fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
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
}
