import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../theme/app_theme.dart';
import '../../privacy/privacy_session_manager.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final privacyManager = Provider.of<PrivacySessionManager>(context);

    return Scaffold(
      backgroundColor: AppTheme.background,
      appBar: AppBar(
        title: const Text('Privacy & Security'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Status Header
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: AppTheme.surface,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: AppTheme.privacyGreen.withValues(alpha: 0.5)),
              ),
              child: Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: AppTheme.privacyGreen.withValues(alpha: 0.15),
                      shape: BoxShape.circle,
                    ),
                    child: const Icon(Icons.shield_rounded, color: AppTheme.privacyGreen, size: 28),
                  ),
                  const SizedBox(width: 16),
                  const Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Private Session: ON',
                          style: TextStyle(
                            color: AppTheme.textPrimary,
                            fontWeight: FontWeight.w700,
                            fontSize: 16,
                          ),
                        ),
                        SizedBox(height: 4),
                        Text(
                          'Browsing data is kept temporarily in memory and is automatically cleared when FireZip exits.',
                          style: TextStyle(color: AppTheme.textSecondary, fontSize: 13),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 28),

            // Section 1: Manual Clearance
            const Text(
              'SESSION DATA CLEARANCE',
              style: TextStyle(
                color: AppTheme.textMuted,
                fontSize: 12,
                fontWeight: FontWeight.w700,
                letterSpacing: 1.5,
              ),
            ),
            const SizedBox(height: 12),
            Container(
              decoration: BoxDecoration(
                color: AppTheme.surface,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: AppTheme.border),
              ),
              child: Column(
                children: [
                  ListTile(
                    leading: const Icon(Icons.cleaning_services_rounded, color: AppTheme.flameOrange),
                    title: const Text('Clear Current Session', style: TextStyle(color: AppTheme.textPrimary)),
                    subtitle: const Text('Resets current temporary tabs and in-memory history', style: TextStyle(color: AppTheme.textSecondary, fontSize: 12)),
                    onTap: () async {
                      await privacyManager.clearSession();
                      if (context.mounted) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text('Current session cleared successfully.')),
                        );
                      }
                    },
                  ),
                  const Divider(color: AppTheme.border, height: 1),
                  ListTile(
                    leading: const Icon(Icons.cookie_outlined, color: AppTheme.zipCyan),
                    title: const Text('Clear Cookies', style: TextStyle(color: AppTheme.textPrimary)),
                    subtitle: const Text('Removes all session cookies stored by websites', style: TextStyle(color: AppTheme.textSecondary, fontSize: 12)),
                    onTap: () async {
                      await privacyManager.clearCookies();
                      if (context.mounted) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text('Cookies cleared.')),
                        );
                      }
                    },
                  ),
                  const Divider(color: AppTheme.border, height: 1),
                  ListTile(
                    leading: const Icon(Icons.cached_rounded, color: AppTheme.zipCyan),
                    title: const Text('Clear Cache', style: TextStyle(color: AppTheme.textPrimary)),
                    subtitle: const Text('Clears temporary webpage images and cached files', style: TextStyle(color: AppTheme.textSecondary, fontSize: 12)),
                    onTap: () async {
                      await privacyManager.clearCache();
                      if (context.mounted) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text('Web cache cleared.')),
                        );
                      }
                    },
                  ),
                  const Divider(color: AppTheme.border, height: 1),
                  ListTile(
                    leading: const Icon(Icons.storage_rounded, color: AppTheme.zipCyan),
                    title: const Text('Clear Website Data', style: TextStyle(color: AppTheme.textPrimary)),
                    subtitle: const Text('Clears localStorage, sessionStorage, and IndexedDB', style: TextStyle(color: AppTheme.textSecondary, fontSize: 12)),
                    onTap: () async {
                      await privacyManager.clearWebStorage();
                      if (context.mounted) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text('Website data cleared.')),
                        );
                      }
                    },
                  ),
                  const Divider(color: AppTheme.border, height: 1),
                  ListTile(
                    leading: const Icon(Icons.delete_forever_rounded, color: AppTheme.flameOrange),
                    title: const Text('Clear All Session Data', style: TextStyle(color: AppTheme.flameOrange, fontWeight: FontWeight.w700)),
                    subtitle: const Text('Wipes cookies, cache, web storage, and temporary tabs in one tap', style: TextStyle(color: AppTheme.textSecondary, fontSize: 12)),
                    onTap: () async {
                      await privacyManager.clearSession();
                      if (context.mounted) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text('All temporary session data cleared.')),
                        );
                      }
                    },
                  ),
                ],
              ),
            ),
            const SizedBox(height: 28),

            // Section 2: Privacy Controls
            const Text(
              'PRIVACY CONTROLS',
              style: TextStyle(
                color: AppTheme.textMuted,
                fontSize: 12,
                fontWeight: FontWeight.w700,
                letterSpacing: 1.5,
              ),
            ),
            const SizedBox(height: 12),
            Container(
              decoration: BoxDecoration(
                color: AppTheme.surface,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: AppTheme.border),
              ),
              child: Column(
                children: [
                  SwitchListTile(
                    activeColor: AppTheme.flameOrange,
                    title: const Text('Block Third-Party Cookies', style: TextStyle(color: AppTheme.textPrimary)),
                    subtitle: const Text('Prevents ad networks from tracking across sites where supported', style: TextStyle(color: AppTheme.textSecondary, fontSize: 12)),
                    value: privacyManager.blockThirdPartyCookies,
                    onChanged: (val) => privacyManager.updateSettings(blockThirdPartyCookies: val),
                  ),
                  const Divider(color: AppTheme.border, height: 1),
                  SwitchListTile(
                    activeColor: AppTheme.flameOrange,
                    title: const Text('Send Do Not Track (DNT) Header', style: TextStyle(color: AppTheme.textPrimary)),
                    subtitle: const Text('Requests that websites do not track your activity', style: TextStyle(color: AppTheme.textSecondary, fontSize: 12)),
                    value: privacyManager.doNotTrack,
                    onChanged: (val) => privacyManager.updateSettings(doNotTrack: val),
                  ),
                  const Divider(color: AppTheme.border, height: 1),
                  SwitchListTile(
                    activeColor: AppTheme.flameOrange,
                    title: const Text('Enable JavaScript', style: TextStyle(color: AppTheme.textPrimary)),
                    subtitle: const Text('Required for interactive web pages to function correctly', style: TextStyle(color: AppTheme.textSecondary, fontSize: 12)),
                    value: privacyManager.javaScriptEnabled,
                    onChanged: (val) => privacyManager.updateSettings(javaScriptEnabled: val),
                  ),
                  const Divider(color: AppTheme.border, height: 1),
                  SwitchListTile(
                    activeColor: AppTheme.flameOrange,
                    title: const Text('Block Pop-ups', style: TextStyle(color: AppTheme.textPrimary)),
                    subtitle: const Text('Blocks unwanted pop-up windows where supported', style: TextStyle(color: AppTheme.textSecondary, fontSize: 12)),
                    value: privacyManager.popUpBlocking,
                    onChanged: (val) => privacyManager.updateSettings(popUpBlocking: val),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 28),

            // Section 3: Honest Privacy Notice
            const Text(
              'ABOUT FIREZIP PRIVACY',
              style: TextStyle(
                color: AppTheme.textMuted,
                fontSize: 12,
                fontWeight: FontWeight.w700,
                letterSpacing: 1.5,
              ),
            ),
            const SizedBox(height: 12),
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: AppTheme.surfaceLight,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: AppTheme.border),
              ),
              child: const Text(
                'FireZip is designed from the ground up as a temporary session browser. FireZip does not retain your browsing history, saved passwords, autofill data, or bookmarks after your session ends.\n\n'
                'Please note: FireZip cannot remove data controlled by your operating system, Internet Service Provider (ISP), Wi-Fi network administrator, DNS provider, or remote websites you visit.',
                style: TextStyle(color: AppTheme.textSecondary, fontSize: 13, height: 1.5),
              ),
            ),
            const SizedBox(height: 32),
          ],
        ),
      ),
    );
  }
}
