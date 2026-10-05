import 'package:flutter/material.dart';
import '../theme/firezip_colors.dart';

class FireZipLogo extends StatelessWidget {
  final double size;
  final bool showText;
  final double fontSize;

  const FireZipLogo({
    super.key,
    this.size = 64,
    this.showText = true,
    this.fontSize = 28,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        SizedBox(
          width: size,
          height: size,
          child: CustomPaint(
            painter: _FireZipLogoPainter(),
          ),
        ),
        if (showText) ...[
          const SizedBox(height: 12),
          RichText(
            text: TextSpan(
              style: TextStyle(
                fontSize: fontSize,
                fontWeight: FontWeight.bold,
                letterSpacing: 1.2,
              ),
              children: const [
                TextSpan(
                  text: 'Fire',
                  style: TextStyle(color: FireZipColors.flameOrange),
                ),
                TextSpan(
                  text: 'Zip',
                  style: TextStyle(color: FireZipColors.zipYellow),
                ),
              ],
            ),
          ),
        ],
      ],
    );
  }
}

class _FireZipLogoPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final width = size.width;
    final height = size.height;

    // Outer flame gradient
    final flameGradient = SweepGradient(
      center: Alignment.center,
      colors: const [
        FireZipColors.flameOrange,
        FireZipColors.zipYellow,
        FireZipColors.flameRed,
        FireZipColors.flameOrange,
      ],
    );

    final flamePaint = Paint()
      ..shader = flameGradient.createShader(Rect.fromLTWH(0, 0, width, height))
      ..style = PaintingStyle.fill;

    // Flame Path
    final flamePath = Path();
    flamePath.moveTo(width * 0.5, height * 0.05);
    flamePath.cubicTo(
      width * 0.75, height * 0.25,
      width * 0.95, height * 0.45,
      width * 0.90, height * 0.70,
    );
    flamePath.cubicTo(
      width * 0.85, height * 0.95,
      width * 0.15, height * 0.95,
      width * 0.10, height * 0.70,
    );
    flamePath.cubicTo(
      width * 0.05, height * 0.45,
      width * 0.25, height * 0.25,
      width * 0.50, height * 0.05,
    );
    flamePath.close();

    canvas.drawPath(flamePath, flamePaint);

    // Inner Zip/Lightning Arrow Symbol (cutout contrast)
    final zipPaint = Paint()
      ..color = Colors.white
      ..style = PaintingStyle.fill;

    final zipPath = Path();
    zipPath.moveTo(width * 0.58, height * 0.20);
    zipPath.lineTo(width * 0.32, height * 0.52);
    zipPath.lineTo(width * 0.52, height * 0.52);
    zipPath.lineTo(width * 0.42, height * 0.80);
    zipPath.lineTo(width * 0.68, height * 0.48);
    zipPath.lineTo(width * 0.48, height * 0.48);
    zipPath.close();

    canvas.drawPath(zipPath, zipPaint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
