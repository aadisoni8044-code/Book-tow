import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/search_engine.dart';
import '../providers/browser_provider.dart';
import '../providers/settings_provider.dart';
import '../theme/firezip_colors.dart';

class PrivacySettingsScreen extends StatelessWidget {
  const PrivacySettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final settings = Provider.of<SettingsProvider>(context);
    final browser = Provider.of<BrowserProvider>(context, listen: false);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Privacy & Security'),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          const ListTile(
            leading: Icon(Icons.shield, color: FireZipColors.privatePurple),
            title: Text('Private Browsing Mode', style: TextStyle(fontWeight: FontWeight.bold)),
            subtitle: Text('Default session privacy active'),
          ),
          SwitchListTile(
            title: const Text('Do Not Track (DNT)'),
            subtitle: const Text('Send Do Not Track header to websites'),
            value: settings.doNotTrack,
            activeColor: FireZipColors.flameOrange,
            onChanged: (val) => settings.toggleDoNotTrack(val),
          ),
          SwitchListTile(
            title: const Text('Block Third-Party Cookies'),
            subtitle: const Text('Prevent third-party tracking scripts'),
            value: settings.blockThirdPartyCookies,
            activeColor: FireZipColors.flameOrange,
            onChanged: (val) => settings.toggleBlockThirdPartyCookies(val),
          ),
          SwitchListTile(
            title: const Text('JavaScript Support'),
            subtitle: const Text('Enable or disable website scripts'),
            value: settings.javaScriptEnabled,
            activeColor: FireZipColors.flameOrange,
            onChanged: (val) => settings.toggleJavaScript(val),
          ),
          SwitchListTile(
            title: const Text('Block Pop-ups'),
            subtitle: const Text('Prevent automatic pop-up windows'),
            value: settings.popUpBlocking,
            activeColor: FireZipColors.flameOrange,
            onChanged: (val) => settings.togglePopUpBlocking(val),
          ),
          const Divider(height: 32),
          ElevatedButton.icon(
            onPressed: () {
              showDialog(
                context: context,
                builder: (context) => AlertDialog(
                  title: const Text('Clear All Private Data'),
                  content: const Text(
                    'This will close all active tabs, wipe temporary web view cookies, cache, and in-memory session data.',
                  ),
                  actions: [
                    TextButton(
                      onPressed: () => Navigator.pop(context),
                      child: const Text('Cancel'),
                    ),
                    ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.red,
                        foregroundColor: Colors.white,
                      ),
                      onPressed: () {
                        browser.closeAllTabs();
                        Navigator.pop(context);
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text('All private browsing session data cleared.')),
                        );
                      },
                      child: const Text('Clear All Data'),
                    ),
                  ],
                ),
              );
            },
            icon: const Icon(Icons.cleaning_services, color: Colors.white),
            label: const Text('Clear All Private Data'),
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.red,
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(vertical: 14),
            ),
          ),
        ],
      ),
    );
  }
}

class SettingsScreen extends StatelessWidget {
  final VoidCallback onOpenPrivacy;
  final VoidCallback onOpenDownloads;

  const SettingsScreen({
    super.key,
    required this.onOpenPrivacy,
    required this.onOpenDownloads,
  });

  @override
  Widget build(BuildContext context) {
    final settings = Provider.of<SettingsProvider>(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('FireZip Settings'),
      ),
      body: ListView(
        children: [
          ListTile(
            leading: const Icon(Icons.security, color: FireZipColors.flameOrange),
            title: const Text('Privacy & Security'),
            subtitle: const Text('Do Not Track, cookies, JavaScript, clear session'),
            trailing: const Icon(Icons.chevron_right),
            onTap: onOpenPrivacy,
          ),
          ListTile(
            leading: const Icon(Icons.download, color: Colors.blue),
            title: const Text('Downloads'),
            subtitle: const Text('Manage downloaded files'),
            trailing: const Icon(Icons.chevron_right),
            onTap: onOpenDownloads,
          ),
          const Divider(),
          SwitchListTile(
            title: const Text('Dark Mode Theme'),
            secondary: const Icon(Icons.dark_mode, color: FireZipColors.zipYellow),
            value: settings.isDarkMode,
            activeColor: FireZipColors.flameOrange,
            onChanged: (val) => settings.toggleDarkMode(val),
          ),
          ListTile(
            leading: const Icon(Icons.search, color: Colors.green),
            title: const Text('Default Search Engine'),
            subtitle: Text(settings.selectedSearchEngine.name),
            trailing: DropdownButton<String>(
              value: settings.selectedSearchEngine.id,
              underline: const SizedBox(),
              items: SearchEngine.defaultEngines.map((e) {
                return DropdownMenuItem(
                  value: e.id,
                  child: Text(e.name),
                );
              }).toList(),
              onChanged: (val) {
                if (val != null) {
                  final engine = SearchEngine.defaultEngines.firstWhere((e) => e.id == val);
                  settings.setSearchEngine(engine);
                }
              },
            ),
          ),
        ],
      ),
    );
  }
}
