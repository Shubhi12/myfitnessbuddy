import 'package:flutter_test/flutter_test.dart';
import 'package:fitness_buddy/features/auth/domain/entities/user.dart';

void main() {
  test('User entity holds profile fields', () {
    const user = User(id: 1, email: 'a@b.com', fullName: 'Test User', communityId: 3);
    expect(user.email, 'a@b.com');
    expect(user.communityId, 3);
  });
}
