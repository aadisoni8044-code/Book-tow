import 'package:flutter/widgets.dart';
import '../privacy/privacy_session_manager.dart';

class LifecycleService with WidgetsBindingObserver {
  final PrivacySessionManager sessionManager;

  LifecycleService({required this.sessionManager});

  void initialize() {
    WidgetsBinding.instance.addObserver(this);
  }

  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    debugPrint('[FireZip] AppLifecycleState changed to: $state');
    if (state == AppLifecycleState.detached ||
        state == AppLifecycleState.paused ||
        state == AppLifecycleState.hidden) {
      sessionManager.cleanupOnExit();
    }
  }
}
