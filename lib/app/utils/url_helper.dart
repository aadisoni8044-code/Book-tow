import '../models/search_engine.dart';

class UrlHelper {
  /// Checks if the input string is a valid URL or search term.
  /// If input is a raw search string, converts it to a search engine URL.
  static String formatUrl(String input, {SearchEngine? searchEngine}) {
    final trimmed = input.trim();
    if (trimmed.isEmpty) return 'about:blank';

    final engine = searchEngine ?? SearchEngine.defaultEngines.first;

    // Direct special schemas
    if (trimmed.startsWith('about:') ||
        trimmed.startsWith('file:') ||
        trimmed.startsWith('data:')) {
      return trimmed;
    }

    // Check if input starts with http:// or https://
    if (trimmed.startsWith('http://') || trimmed.startsWith('https://')) {
      return trimmed;
    }

    // Check for IP address or domain format (e.g., example.com, 192.168.1.1, localhost)
    final domainRegex = RegExp(
      r'^(localhost|(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}|(?:\d{1,3}\.){3}\d{1,3})(?::\d+)?(?:/.*)?$',
      caseSensitive: false,
    );

    if (domainRegex.hasMatch(trimmed) && !trimmed.contains(' ')) {
      return 'https://$trimmed';
    }

    // Treat as search query
    final encoded = Uri.encodeComponent(trimmed);
    return '${engine.searchUrl}$encoded';
  }

  /// Determines if a given URL uses HTTPS protocol.
  static bool isSecure(String url) {
    return url.toLowerCase().startsWith('https://');
  }

  /// Extracts display domain name from full URL.
  static String getDisplayDomain(String url) {
    if (url.startsWith('about:') || url.isEmpty) return url;
    try {
      final uri = Uri.parse(url);
      return uri.host.isNotEmpty ? uri.host : url;
    } catch (_) {
      return url;
    }
  }
}
