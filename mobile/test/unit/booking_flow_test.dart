import 'package:flutter_test/flutter_test.dart';

import 'package:fitness_buddy/features/amenities/domain/entities/amenity.dart';
import 'package:fitness_buddy/features/amenities/domain/services/amenity_priority_service.dart';
import 'package:fitness_buddy/features/amenities/domain/services/slot_generator.dart';
import 'package:fitness_buddy/features/fitness_profile/domain/entities/fitness_profile.dart';

void main() {
  Amenity amenity({required String name, required String type}) {
    return Amenity(
      id: 1,
      communityId: 3,
      name: name,
      amenityType: type,
      description: null,
      capacity: 1,
      openTime: '06:00:00',
      closeTime: '10:00:00',
      slotDurationMinutes: 60,
      isActive: true,
    );
  }

  test('prioritizeAmenities moves matching fitness profile amenities first', () {
    final amenities = [
      amenity(name: 'Pool', type: 'pool'),
      amenity(name: 'Gym', type: 'gym'),
      amenity(name: 'Badminton', type: 'badminton_court'),
    ];
    const profile = FitnessProfile(
      id: 1,
      userId: 1,
      fitnessLevel: 'beginner',
      preferredWorkouts: ['badminton'],
    );

    final sorted = prioritizeAmenities(amenities, profile);

    expect(sorted.first.amenityType, 'badminton_court');
  });

  test('duration options are capped to maximum two hours', () {
    final options = durationOptionsForAmenity(amenity(name: 'Gym', type: 'gym'));

    expect(options, [60, 120]);
    expect(options.every((duration) => duration <= 120), isTrue);
  });

  test('generateAmenitySlots creates slots with selected duration', () {
    final slots = generateAmenitySlots(
      amenity: amenity(name: 'Gym', type: 'gym'),
      date: DateTime(2026, 7, 9),
      durationMinutes: 120,
      now: DateTime(2026, 7, 8),
    );

    expect(slots.first.label, '6:00 AM - 8:00 AM');
    expect(slots.last.label, '8:00 AM - 10:00 AM');
  });
}
