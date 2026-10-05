import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:webview_flutter/webview_flutter.dart';
import '../models/browser_tab.dart';
import '../providers/browser_provider.dart';
import '../providers/settings_provider.dart';
import 'error_screen.dart';

class BrowserScreen extends StatefulWidget {
  final BrowserTab tab;
  final int tabIndex;

  const BrowserScreen({
    super.key,
    required this.tab,
    required this.tabIndex,
  });

  @override
  State<BrowserScreen> createState() => _BrowserScreenState();
}

class _BrowserScreenState extends State<BrowserScreen> {
  WebViewController? _controller;
  bool _isWebViewSupported = false;

  @override
  void initState() {
    super.initState();
    _isWebViewSupported = kIsWeb ||
        defaultTargetPlatform == TargetPlatform.android ||
        defaultTargetPlatform == TargetPlatform.iOS;

    if (_isWebViewSupported) {
      _initWebView();
    }
  }

  void _initWebView() {
    final settings = Provider.of<SettingsProvider>(context, listen: false);
    final browser = Provider.of<BrowserProvider>(context, listen: false);

    final controller = WebViewController()
      ..setJavaScriptMode(
        settings.javaScriptEnabled ? JavaScriptMode.unrestricted : JavaScriptMode.disabled,
      )
      ..setNavigationDelegate(
        NavigationDelegate(
          onPageStarted: (String url) {
            browser.updateTabLoading(widget.tabIndex, true, progress: 0.1);
            browser.updateTabUrl(widget.tabIndex, url);
          },
          onProgress: (int progress) {
            browser.updateTabLoading(widget.tabIndex, true, progress: progress / 100.0);
          },
          onPageFinished: (String url) async {
            browser.updateTabLoading(widget.tabIndex, false, progress: 1.0);
            browser.updateTabUrl(widget.tabIndex, url);

            final title = await _controller?.getTitle();
            if (title != null && title.isNotEmpty) {
              browser.updateTabTitle(widget.tabIndex, title);
            }

            final canBack = await _controller?.canGoBack() ?? false;
            final canForward = await _controller?.canGoForward() ?? false;
            browser.updateTabNavState(widget.tabIndex, canGoBack: canBack, canGoForward: canForward);
          },
          onWebResourceError: (WebResourceError error) {
            browser.setTabError(
              widget.tabIndex,
              'Error loading page (${error.errorCode}): ${error.description}',
            );
          },
        ),
      );

    if (widget.tab.url != 'about:blank') {
      controller.loadRequest(Uri.parse(widget.tab.url));
    }

    _controller = controller;
    browser.attachController(widget.tabIndex, controller);
  }

  @override
  void didUpdateWidget(BrowserScreen oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.tab.url != widget.tab.url &&
        _controller != null &&
        widget.tab.url != 'about:blank') {
      // Load request only if the URL change originated outside webview internal navigation
      _controller!.currentUrl().then((currentUrl) {
        if (currentUrl != widget.tab.url) {
          _controller!.loadRequest(Uri.parse(widget.tab.url));
        }
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (widget.tab.errorMessage != null) {
      return ErrorScreen(
        title: 'Connection Error',
        message: widget.tab.errorMessage!,
        onRetry: () {
          final browser = Provider.of<BrowserProvider>(context, listen: false);
          browser.updateTabUrl(widget.tabIndex, widget.tab.url);
          _controller?.reload();
        },
      );
    }

    if (!_isWebViewSupported) {
      return _buildDesktopFallbackView();
    }

    return Column(
      children: [
        if (widget.tab.isLoading)
          LinearProgressIndicator(
            value: widget.tab.progress,
            minHeight: 2,
            backgroundColor: Colors.transparent,
          ),
        Expanded(
          child: WebViewWidget(controller: _controller!),
        ),
      ],
    );
  }

  Widget _buildDesktopFallbackView() {
    return Center(
      child: Container(
        margin: const EdgeInsets.all(24),
        padding: const EdgeInsets.all(24),
        decoration: BoxDecoration(
          color: Theme.of(context).cardColor,
          borderRadius: BorderRadius.circular(16),
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.language, size: 64, color: Colors.blue),
            const SizedBox(height: 16),
            Text(
              'Browsing: ${widget.tab.title}',
              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            SelectableText(
              widget.tab.url,
              style: const TextStyle(color: Colors.blueAccent),
            ),
            const SizedBox(height: 16),
            const Text(
              'Mobile / Android / iOS native WebView active. Desktop preview simulation enabled.',
              textAlign: TextAlign.center,
              style: TextStyle(color: Colors.grey, fontSize: 12),
            ),
          ],
        ),
      ),
    );
  }
}
