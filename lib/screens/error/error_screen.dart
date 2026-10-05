import 'package:flutter/material.dart';
import '../../theme/app_theme.dart';
import '../../models/browser_tab.dart';

class FireZipErrorScreen extends StatelessWidget {
  final WebErrorType errorType;
  final String? customMessage;
  final VoidCallback onTryAgain;
  final VoidCallback onGoHome;

  const FireZipErrorScreen({
    super.key,
    required this.errorType,
    this.customMessage,
    required this.onTryAgain,
    required this.onGoHome,
  });

  String get title {
    switch (errorType) {
      case WebErrorType.noInternet:
        return 'No Internet Connection';
      case WebErrorType.websiteUnavailable:
        return 'Website Unavailable';
      case WebErrorType.invalidUrl:
        return 'Invalid Address';
      case WebErrorType.connectionError:
        return 'Connection Failed';
      case WebErrorType.sslError:
        return 'Security Error (SSL)';
      case WebErrorType.none:
        return 'Error Occurred';
    }
  }

  String get description {
    if (customMessage != null && customMessage!.isNotEmpty) {
      return customMessage!;
    }
    switch (errorType) {
      case WebErrorType.noInternet:
        return 'Please check your network connection and try again.';
      case WebErrorType.websiteUnavailable:
        return 'The requested website could not be reached or is currently down.';
      case WebErrorType.invalidUrl:
        return 'The web address entered is invalid or malformed.';
      case WebErrorType.connectionError:
        return 'FireZip was unable to establish a secure connection to the destination server.';
      case WebErrorType.sslError:
        return 'The website presented an invalid or untrusted security certificate.';
      case WebErrorType.none:
        return 'An unknown error occurred while loading the page.';
    }
  }

  IconData get iconData {
    switch (errorType) {
      case WebErrorType.noInternet:
        return Icons.wifi_off_rounded;
      case WebErrorType.sslError:
        return Icons.gpp_maybe_rounded;
      case WebErrorType.invalidUrl:
        return Icons.link_off_rounded;
      case WebErrorType.connectionError:
        return Icons.cloud_off_rounded;
      default:
        return Icons.error_outline_rounded;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Center(
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              padding: const EdgeInsets.all(24),
              decoration: BoxDecoration(
                color: AppTheme.flameOrange.withValues(alpha: 0.15),
                shape: BoxShape.circle,
                border: Border.all(color: AppTheme.flameOrange.withValues(alpha: 0.4), width: 2),
              ),
              child: Icon(iconData, size: 48, color: AppTheme.flameOrange),
            ),
            const SizedBox(height: 24),
            Text(
              title,
              textAlign: TextAlign.center,
              style: const TextStyle(
                color: AppTheme.textPrimary,
                fontSize: 22,
                fontWeight: FontWeight.w800,
              ),
            ),
            const SizedBox(height: 12),
            Text(
              description,
              textAlign: TextAlign.center,
              style: const TextStyle(
                color: AppTheme.textSecondary,
                fontSize: 14,
                height: 1.5,
              ),
            ),
            const SizedBox(height: 32),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                OutlinedButton.icon(
                  icon: const Icon(Icons.home_rounded, size: 18),
                  label: const Text('Go Home'),
                  onPressed: onGoHome,
                ),
                const SizedBox(width: 16),
                ElevatedButton.icon(
                  icon: const Icon(Icons.refresh_rounded, size: 18),
                  label: const Text('Try Again'),
                  onPressed: onTryAgain,
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
