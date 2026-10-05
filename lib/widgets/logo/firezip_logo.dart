import 'dart:math' as math;
import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';

class FireZipLogo extends StatefulWidget {
  final double size;
  final bool showText;
  final bool animate;

  const FireZipLogo({
    super.key,
    this.size = 80,
    this.showText = true,
    this.animate = false,
  });

  @override
  State<FireZipLogo> createState() => _FireZipLogoState();
}

class _FireZipLogoState extends State<FireZipLogo>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 4),
    );
    if (widget.animate) {
      _controller.repeat(reverse: true);
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        AnimatedBuilder(
          animation: _controller,
          builder: (context, child) {
            return CustomPaint(
              size: Size(widget.size, widget.size),
              painter: _FireZipPainter(
                progress: _controller.value,
              ),
            );
          },
        ),
        if (widget.showText) ...[
          SizedBox(height: widget.size * 0.15),
          ShaderMask(
            shaderCallback: (bounds) => const LinearGradient(
              colors: [AppTheme.flameOrange, AppTheme.zipCyan],
              begin: Alignment.centerLeft,
              end: Alignment.centerRight,
            ).createShader(bounds),
            child: Text(
              'FireZip',
              style: TextStyle(
                fontSize: widget.size * 0.38,
                fontWeight: FontWeight.w900,
                letterSpacing: 1.2,
                color: Colors.white,
              ),
            ),
          ),
          SizedBox(height: widget.size * 0.05),
          Text(
            'FAST • TEMPORARY • PRIVATE',
            style: TextStyle(
              fontSize: math.max(10, widget.size * 0.12),
              fontWeight: FontWeight.w700,
              letterSpacing: 2.0,
              color: AppTheme.textSecondary,
            ),
          ),
        ],
      ],
    );
  }
}

class _FireZipPainter extends CustomPainter {
  final double progress;

  _FireZipPainter({this.progress = 0});

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final w = size.width;
    final h = size.height;

    // Background glow
    final glowPaint = Paint()
      ..shader = RadialGradient(
        colors: [
          AppTheme.flameOrange.withValues(alpha: 0.35 + 0.1 * math.sin(progress * math.pi)),
          AppTheme.zipCyan.withValues(alpha: 0.15),
          Colors.transparent,
        ],
        stops: const [0.0, 0.5, 1.0],
      ).createShader(Rect.fromCircle(center: center, radius: w * 0.65));

    canvas.drawCircle(center, w * 0.65, glowPaint);

    // Outer Shield / Flame teardrop geometry
    final flamePath = Path();
    flamePath.moveTo(w * 0.5, h * 0.05); // Top tip
    // Right curve down
    flamePath.cubicTo(
      w * 0.82, h * 0.25,
      w * 0.95, h * 0.55,
      w * 0.80, h * 0.82,
    );
    // Bottom curve
    flamePath.cubicTo(
      w * 0.68, h * 0.98,
      w * 0.32, h * 0.98,
      w * 0.20, h * 0.82,
    );
    // Left curve up
    flamePath.cubicTo(
      w * 0.05, h * 0.55,
      w * 0.18, h * 0.25,
      w * 0.5, h * 0.05,
    );
    flamePath.close();

    final flamePaint = Paint()
      ..shader = const LinearGradient(
        begin: Alignment.topCenter,
        end: Alignment.bottomRight,
        colors: [
          AppTheme.flameOrange,
          AppTheme.flameOrangeLight,
          AppTheme.zipCyan,
        ],
        stops: [0.0, 0.55, 1.0],
      ).createShader(Rect.fromLTWH(0, 0, w, h))
      ..style = PaintingStyle.fill;

    canvas.drawPath(flamePath, flamePaint);

    // Inner Zip / Speed Arrow Cutout (Sharp, fast Z/Arrow shape)
    final zipPath = Path();
    zipPath.moveTo(w * 0.55, h * 0.20); // Top right start
    zipPath.lineTo(w * 0.32, h * 0.48); // Diagonal down-left
    zipPath.lineTo(w * 0.52, h * 0.48); // Horizontal right step
    zipPath.lineTo(w * 0.42, h * 0.80); // Diagonal down to bottom arrow
    zipPath.lineTo(w * 0.68, h * 0.48); // Diagonal up-right
    zipPath.lineTo(w * 0.48, h * 0.48); // Horizontal left step
    zipPath.close();

    final innerPaint = Paint()
      ..color = AppTheme.background
      ..style = PaintingStyle.fill;

    canvas.drawPath(zipPath, innerPaint);

    // Fast Zip Glow Line inside arrow
    final linePaint = Paint()
      ..color = AppTheme.zipCyan
      ..style = PaintingStyle.stroke
      ..strokeWidth = w * 0.04
      ..strokeCap = StrokeCap.round;

    final glowLinePath = Path();
    glowLinePath.moveTo(w * 0.34, h * 0.48);
    glowLinePath.lineTo(w * 0.50, h * 0.48);
    glowLinePath.lineTo(w * 0.44, h * 0.72);

    canvas.drawPath(glowLinePath, linePaint);
  }

  @override
  bool shouldRepaint(covariant _FireZipPainter oldDelegate) {
    return oldDelegate.progress != progress;
  }
}
