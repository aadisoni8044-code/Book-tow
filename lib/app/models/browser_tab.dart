/// Represents a browser tab instance in FireZip.
class BrowserTab {
  final String id;
  String url;
  String title;
  String? faviconUrl;
  bool isLoading;
  double progress;
  bool canGoBack;
  bool canGoForward;
  bool isSecure;
  final bool isPrivate;
  String? errorMessage;
  Object? webViewController;

  BrowserTab({
    required this.id,
    this.url = 'about:blank',
    this.title = 'New Tab',
    this.faviconUrl,
    this.isLoading = false,
    this.progress = 0.0,
    this.canGoBack = false,
    this.canGoForward = false,
    this.isSecure = true,
    this.isPrivate = true,
    this.errorMessage,
    this.webViewController,
  });

  BrowserTab copyWith({
    String? id,
    String? url,
    String? title,
    String? faviconUrl,
    bool? isLoading,
    double? progress,
    bool? canGoBack,
    bool? canGoForward,
    bool? isSecure,
    bool? isPrivate,
    String? errorMessage,
    Object? webViewController,
  }) {
    return BrowserTab(
      id: id ?? this.id,
      url: url ?? this.url,
      title: title ?? this.title,
      faviconUrl: faviconUrl ?? this.faviconUrl,
      isLoading: isLoading ?? this.isLoading,
      progress: progress ?? this.progress,
      canGoBack: canGoBack ?? this.canGoBack,
      canGoForward: canGoForward ?? this.canGoForward,
      isSecure: isSecure ?? this.isSecure,
      isPrivate: isPrivate ?? this.isPrivate,
      errorMessage: errorMessage ?? this.errorMessage,
      webViewController: webViewController ?? this.webViewController,
    );
  }
}
