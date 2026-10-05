import 'package:flutter/foundation.dart';
import 'package:webview_flutter/webview_flutter.dart';

class FireZipStorageManager {
  /// Clears localStorage, sessionStorage, and IndexedDB in WebViews.
  Future<bool> clearWebStorage([List<WebViewController>? controllers]) async {
    try {
      if (controllers != null) {
        const jsStorageClear = '''
          try {
            if (window.localStorage) window.localStorage.clear();
            if (window.sessionStorage) window.sessionStorage.clear();
            if (window.indexedDB && window.indexedDB.databases) {
              window.indexedDB.databases().then(dbs => {
                dbs.forEach(db => window.indexedDB.deleteDatabase(db.name));
              });
            }
          } catch(e) {}
        ''';
        for (final controller in controllers) {
          try {
            await controller.runJavaScript(jsStorageClear);
          } catch (_) {
            // Controller might be disposed or uninitialized
          }
        }
      }
      debugPrint('[FireZip] WebStorage (localStorage, sessionStorage, IndexedDB) cleared.');
      return true;
    } catch (e) {
      debugPrint('[FireZip] Error clearing web storage: $e');
      return false;
    }
  }
}
