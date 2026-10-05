import 'package:flutter/foundation.dart';
import 'package:webview_flutter/webview_flutter.dart';
import '../models/browser_tab.dart';

class BrowserController {
  static const String defaultSearchEngineUrl = 'https://duckduckgo.com/?q=';

  /// Formats user input into a valid URL or a DuckDuckGo search query.
  static String parseInputUrl(String input) {
    final trimmed = input.trim();
    if (trimmed.isEmpty) return 'firezip://home';

    if (trimmed == 'firezip://home' || trimmed == 'about:blank') {
      return trimmed;
    }

    // Check if it's already an explicit scheme (http/https)
    if (trimmed.startsWith('http://') || trimmed.startsWith('https://')) {
      return trimmed;
    }

    // Check if it looks like a domain name (e.g., example.com, wikipedia.org, localhost)
    final domainRegex = RegExp(
      r'^(localhost|([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})(:[0-9]+)?(\/.*)?$',
      caseSensitive: false,
    );

    if (domainRegex.hasMatch(trimmed) && !trimmed.contains(' ')) {
      return 'https://$trimmed';
    }

    // Otherwise, treat as search query on DuckDuckGo
    return '$defaultSearchEngineUrl${Uri.encodeComponent(trimmed)}';
  }

  /// Checks if a URL is secure (HTTPS).
  static bool isSecureUrl(String url) {
    return url.startsWith('https://');
  }

  /// Extracts display domain or title from URL.
  static String formatDisplayUrl(String url) {
    if (url == 'firezip://home') return 'Home';
    try {
      final uri = Uri.parse(url);
      if (uri.host.isNotEmpty) return uri.host;
    } catch (_) {}
    return url;
  }

  /// Maps WebView error code/description to WebErrorType.
  static WebErrorType mapError(int errorCode, String description) {
    final lowerDesc = description.toLowerCase();
    if (errorCode == -2 || lowerDesc.contains('internet') || lowerDesc.contains('network') || lowerDesc.contains('namenotresolved')) {
      return WebErrorType.noInternet;
    }
    if (errorCode == -6 || lowerDesc.contains('connection_refused') || lowerDesc.contains('connect')) {
      return WebErrorType.connectionError;
    }
    if (lowerDesc.contains('ssl') || lowerDesc.contains('cert') || errorCode == -1200) {
      return WebErrorType.sslError;
    }
    if (errorCode == -10 || errorCode == 404 || lowerDesc.contains('not found')) {
      return WebErrorType.websiteUnavailable;
    }
    return WebErrorType.websiteUnavailable;
  }
}
