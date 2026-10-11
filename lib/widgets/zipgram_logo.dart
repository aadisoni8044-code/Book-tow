import 'package:flutter/material.dart';

import '../theme/app_colors.dart';

class ZipgramLogo extends StatelessWidget {
  final double height;
  final bool showText;

  const ZipgramLogo({
    super.key,
    this.height = 36.0,
    this.showText = true,
  });

  @override
  Widget build(BuildContext context) {
    return Image.asset(
      'assets/images/logo.png',
      height: height,
      fit: BoxFit.contain,
      errorBuilder: (context, error, stackTrace) {
        // Fallback custom vector rendering if asset missing
        return Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
              decoration: BoxDecoration(
                color: AppColors.primaryBlue,
                borderRadius: BorderRadius.circular(8),
              ),
              child: const Text(
                'ZIP',
                style: TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                  fontSize: 16,
                  letterSpacing: 1.0,
                ),
              ),
            ),
            if (showText) ...[
              const SizedBox(width: 6),
              const Text(
                'gram',
                style: TextStyle(
                  color: AppColors.primaryBlue,
                  fontWeight: FontWeight.w400,
                  fontSize: 22,
                  letterSpacing: 0.5,
                ),
              ),
            ],
          ],
        );
      },
    );
  }
}
