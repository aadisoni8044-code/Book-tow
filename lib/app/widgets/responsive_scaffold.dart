import 'package:flutter/material.dart';

class ResponsiveScaffold extends StatelessWidget {
  final Widget body;
  final PreferredSizeWidget? appBar;
  final Widget? bottomNavigationBar;

  const ResponsiveScaffold({
    super.key,
    required this.body,
    this.appBar,
    this.bottomNavigationBar,
  });

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        final isDesktop = constraints.maxWidth >= 900;

        return Scaffold(
          appBar: appBar,
          body: Center(
            child: Container(
              constraints: BoxConstraints(
                maxWidth: isDesktop ? 1200 : double.infinity,
              ),
              child: body,
            ),
          ),
          bottomNavigationBar: bottomNavigationBar,
        );
      },
    );
  }
}
