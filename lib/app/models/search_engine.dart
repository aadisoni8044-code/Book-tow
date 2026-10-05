class SearchEngine {
  final String id;
  final String name;
  final String searchUrl;
  final String homeUrl;
  final String iconPath;

  const SearchEngine({
    required this.id,
    required this.name,
    required this.searchUrl,
    required this.homeUrl,
    required this.iconPath,
  });

  static const List<SearchEngine> defaultEngines = [
    SearchEngine(
      id: 'duckduckgo',
      name: 'DuckDuckGo',
      searchUrl: 'https://duckduckgo.com/?q=',
      homeUrl: 'https://duckduckgo.com',
      iconPath: 'assets/icons/duckduckgo.png',
    ),
    SearchEngine(
      id: 'google',
      name: 'Google',
      searchUrl: 'https://www.google.com/search?q=',
      homeUrl: 'https://www.google.com',
      iconPath: 'assets/icons/google.png',
    ),
    SearchEngine(
      id: 'bing',
      name: 'Bing',
      searchUrl: 'https://www.bing.com/search?q=',
      homeUrl: 'https://www.bing.com',
      iconPath: 'assets/icons/bing.png',
    ),
    SearchEngine(
      id: 'brave',
      name: 'Brave Search',
      searchUrl: 'https://search.brave.com/search?q=',
      homeUrl: 'https://search.brave.com',
      iconPath: 'assets/icons/brave.png',
    ),
  ];
}
