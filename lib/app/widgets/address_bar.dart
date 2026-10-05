import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../theme/firezip_colors.dart';
import 'private_badge.dart';

class AddressBar extends StatefulWidget {
  final String currentUrl;
  final bool isLoading;
  final bool isSecure;
  final Function(String) onSubmit;
  final VoidCallback? onReload;
  final VoidCallback? onStop;

  const AddressBar({
    super.key,
    required this.currentUrl,
    required this.isLoading,
    required this.isSecure,
    required this.onSubmit,
    this.onReload,
    this.onStop,
  });

  @override
  State<AddressBar> createState() => _AddressBarState();
}

class _AddressBarState extends State<AddressBar> {
  late TextEditingController _textController;
  late FocusNode _focusNode;
  bool _isEditing = false;

  @override
  void initState() {
    super.initState();
    _textController = TextEditingController(text: widget.currentUrl);
    _focusNode = FocusNode();
    _focusNode.addListener(() {
      setState(() {
        _isEditing = _focusNode.hasFocus;
        if (_focusNode.hasFocus) {
          _textController.selection = TextSelection(
            baseOffset: 0,
            extentOffset: _textController.text.length,
          );
        }
      });
    });
  }

  @override
  void didUpdateWidget(AddressBar oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.currentUrl != widget.currentUrl && !_focusNode.hasFocus) {
      _textController.text = widget.currentUrl;
    }
  }

  @override
  void dispose() {
    _textController.dispose();
    _focusNode.dispose();
    super.dispose();
  }

  void _handleSubmitted(String val) {
    _focusNode.unfocus();
    widget.onSubmit(val);
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Container(
      height: 48,
      margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: isDark ? FireZipColors.darkSurface : FireZipColors.lightSurface,
        borderRadius: BorderRadius.circular(24),
        border: Border.all(
          color: _isEditing
              ? FireZipColors.flameOrange
              : (isDark ? FireZipColors.darkBorder : FireZipColors.lightBorder),
          width: 1.5,
        ),
      ),
      child: Row(
        children: [
          const SizedBox(width: 12),
          Icon(
            widget.isSecure ? Icons.lock_outline : Icons.lock_open_outlined,
            size: 18,
            color: widget.isSecure ? Colors.green : Colors.orange,
          ),
          const SizedBox(width: 8),
          const PrivateBadge(compact: true),
          const SizedBox(width: 8),
          Expanded(
            child: TextField(
              controller: _textController,
              focusNode: _focusNode,
              textInputAction: TextInputAction.go,
              keyboardType: TextInputType.url,
              style: TextStyle(
                fontSize: 14,
                color: isDark ? FireZipColors.textPrimaryDark : FireZipColors.textPrimaryLight,
              ),
              decoration: const InputDecoration(
                hintText: 'Search or enter website',
                hintStyle: TextStyle(fontSize: 14, color: Colors.grey),
                border: InputBorder.none,
                isDense: true,
                contentPadding: EdgeInsets.symmetric(vertical: 12),
              ),
              onSubmitted: _handleSubmitted,
            ),
          ),
          if (_textController.text.isNotEmpty)
            IconButton(
              icon: const Icon(Icons.close, size: 18),
              onPressed: () {
                _textController.clear();
              },
            ),
          IconButton(
            icon: const Icon(Icons.content_paste, size: 18),
            onPressed: () async {
              final data = await Clipboard.getData(Clipboard.kTextPlain);
              if (data?.text != null) {
                _textController.text = data!.text!;
                _handleSubmitted(data.text!);
              }
            },
          ),
          if (widget.isLoading)
            IconButton(
              icon: const Icon(Icons.stop_outlined, size: 20, color: Colors.red),
              onPressed: widget.onStop,
            )
          else
            IconButton(
              icon: const Icon(Icons.refresh, size: 20),
              onPressed: widget.onReload,
            ),
          const SizedBox(width: 4),
        ],
      ),
    );
  }
}
