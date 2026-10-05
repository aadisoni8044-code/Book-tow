import 'package:flutter/material.dart';

class PrivateBadge extends StatelessWidget {
  final bool compact;

  const PrivateBadge({super.key, this.compact = false});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.symmetric(
        horizontal: compact ? 6 : 10,
        vertical: compact ? 2 : 4,
      ),
      decoration: BoxDecoration(
        color: const Color(0xFF9D4EDD).withValues(alpha: 0.15),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: const Color(0xFF9D4EDD).withValues(alpha: 0.4),
          width: 1,
        ),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Icon(
            Icons.shield_outlined,
            size: 14,
            color: Color(0xFF9D4EDD),
          ),
          if (!compact) ...[
            const SizedBox(width: 4),
            const Text(
              'PRIVATE MODE',
              style: TextStyle(
                color: Color(0xFF9D4EDD),
                fontSize: 11,
                fontWeight: FontWeight.bold,
                letterSpacing: 0.8,
              ),
            ),
          ],
        ],
      ),
    );
  }
}
