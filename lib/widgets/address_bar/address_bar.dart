import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';
import '../../browser/browser_controller.dart';

class AddressBar extends StatefulWidget {
  final String currentUrl;
  final bool isLoading;
  final ValueChanged<String> onSubmit;
  final VoidCallback onReload;
  final VoidCallback onOpenMenu;

  const AddressBar({
    super.key,
    required this.currentUrl,
    required this.isLoading,
    required this.onSubmit,
    required this.onReload,
    required this.onOpenMenu,
  });

  @override
  State<AddressBar> createState() => _AddressBarState();
}

class _AddressBarState extends State<AddressBar> {
  late TextEditingController _textController;
  final FocusNode _focusNode = FocusNode();
  bool _isEditing = false;

  @override
  void initState() {
    super.initState();
    _textController = TextEditingController(text: _getDisplayText(widget.currentUrl));
    _focusNode.addListener(() {
      setState(() {
        _isEditing = _focusNode.hasFocus;
        if (!_focusNode.hasFocus) {
          _textController.text = _getDisplayText(widget.currentUrl);
        }
      });
    });
  }

  @override
  void didUpdateWidget(AddressBar oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.currentUrl != widget.currentUrl && !_focusNode.hasFocus) {
      _textController.text = _getDisplayText(widget.currentUrl);
    }
  }

  @override
  void dispose() {
    _textController.dispose();
    _focusNode.dispose();
    super.dispose();
  }

  String _getDisplayText(String url) {
    if (url == 'firezip://home' || url == 'about:blank') {
      return '';
    }
    return url;
  }

  void _handleSubmit() {
    final text = _textController.text.trim();
    _focusNode.unfocus();
    if (text.isNotEmpty) {
      widget.onSubmit(text);
    }
  }

  @override
  Widget build(BuildContext context) {
    final isSecure = BrowserController.isSecureUrl(widget.currentUrl);
    final isHome = widget.currentUrl == 'firezip://home' || widget.currentUrl == 'about:blank';

    return Container(
      height: 48,
      margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: AppTheme.surfaceLight,
        borderRadius: BorderRadius.circular(24),
        border: Border.all(
          color: _isEditing ? AppTheme.flameOrange : AppTheme.border,
          width: _isEditing ? 1.5 : 1.0,
        ),
      ),
      child: Row(
        children: [
          const SizedBox(width: 12),
          // Security / Privacy Icon
          Tooltip(
            message: isHome
                ? 'Private Home Session'
                : (isSecure ? 'Secure Connection (HTTPS)' : 'Standard Connection'),
            child: Icon(
              isHome
                  ? Icons.shield_outlined
                  : (isSecure ? Icons.lock_rounded : Icons.info_outline_rounded),
              size: 18,
              color: isHome
                  ? AppTheme.zipCyan
                  : (isSecure ? AppTheme.privacyGreen : AppTheme.textSecondary),
            ),
          ),
          const SizedBox(width: 8),
          // URL / Search TextField
          Expanded(
            child: TextField(
              controller: _textController,
              focusNode: _focusNode,
              textInputAction: TextInputAction.go,
              style: const TextStyle(
                color: AppTheme.textPrimary,
                fontSize: 14,
                fontWeight: FontWeight.w500,
              ),
              decoration: const InputDecoration(
                hintText: 'Search or enter website',
                hintStyle: TextStyle(color: AppTheme.textMuted, fontSize: 14),
                border: InputBorder.none,
                enabledBorder: InputBorder.none,
                focusedBorder: InputBorder.none,
                contentPadding: EdgeInsets.zero,
                isDense: true,
              ),
              onSubmitted: (_) => _handleSubmit(),
            ),
          ),
          // Reload / Stop Button
          if (widget.isLoading)
            SizedBox(
              width: 32,
              height: 32,
              child: IconButton(
                padding: EdgeInsets.zero,
                icon: const SizedBox(
                  width: 14,
                  height: 14,
                  child: CircularProgressIndicator(
                    strokeWidth: 2,
                    valueColor: AlwaysStoppedAnimation<Color>(AppTheme.flameOrange),
                  ),
                ),
                onPressed: () {},
              ),
            )
          else if (!isHome)
            IconButton(
              padding: EdgeInsets.zero,
              constraints: const BoxConstraints(minWidth: 32, minHeight: 32),
              icon: const Icon(Icons.refresh_rounded, size: 20, color: AppTheme.textSecondary),
              onPressed: widget.onReload,
            ),
          // Menu button
          IconButton(
            padding: EdgeInsets.zero,
            constraints: const BoxConstraints(minWidth: 36, minHeight: 36),
            icon: const Icon(Icons.more_vert_rounded, size: 20, color: AppTheme.textSecondary),
            onPressed: widget.onOpenMenu,
          ),
          const SizedBox(width: 4),
        ],
      ),
    );
  }
}
