import 'package:flutter_test/flutter_test.dart';
import 'package:fitness_buddy/core/config/app_config.dart';

void main() {
  test('AppConfig has default API base URL', () {
    expect(AppConfig.apiBaseUrl, isNotEmpty);
    expect(AppConfig.appName, 'My Fitness Buddy');
  });
}
