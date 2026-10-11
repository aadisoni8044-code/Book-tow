import 'package:flutter/foundation.dart';
import '../models/app_filter.dart';

class FilterProvider extends ChangeNotifier {
  AppFilter _selectedFilter = AppFilter.original;

  AppFilter get selectedFilter => _selectedFilter;
  AppFilterType get selectedType => _selectedFilter.type;
  List<double> get currentMatrix => _selectedFilter.matrix;

  void selectFilter(AppFilter filter) {
    if (_selectedFilter.type != filter.type) {
      _selectedFilter = filter;
      notifyListeners();
    }
  }

  void selectFilterByType(AppFilterType type) {
    final filter = AppFilter.fromType(type);
    selectFilter(filter);
  }

  void reset() {
    _selectedFilter = AppFilter.original;
    notifyListeners();
  }
}
