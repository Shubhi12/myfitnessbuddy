import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'package:fitness_buddy/app.dart';
import 'package:fitness_buddy/features/auth/domain/repositories/auth_repository.dart';
import 'package:fitness_buddy/features/auth/presentation/providers/auth_provider.dart';

class _FakeAuthRepository implements AuthRepository {
  @override
  Future<void> login(String email, String password) async {}

  @override
  Future<void> register({
    required String email,
    required String password,
    required String fullName,
    required int communityId,
    String? phone,
  }) async {}

  @override
  Future<void> logout() async {}

  @override
  Future<bool> isLoggedIn() async => false;
}

void main() {
  testWidgets('App loads login screen after auth init', (tester) async {
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          authRepositoryProvider.overrideWithValue(_FakeAuthRepository()),
        ],
        child: const FitnessBuddyApp(),
      ),
    );

    await tester.pump();
    await tester.pump(const Duration(milliseconds: 100));

    expect(find.text('My Fitness Buddy'), findsOneWidget);
    expect(find.text('Sign In'), findsOneWidget);
  });
}
