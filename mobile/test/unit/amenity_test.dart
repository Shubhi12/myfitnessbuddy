import 'package:flutter_test/flutter_test.dart';

import 'package:fitness_buddy/core/utils/amenity_image_mapper.dart';
import 'package:fitness_buddy/features/amenities/domain/entities/amenity.dart';

void main() {
  test('Amenity parses API response', () {
    final amenity = Amenity.fromJson({
      'id': 1,
      'community_id': 3,
      'name': 'Rain forest',
      'amenity_type': 'gym',
      'description': 'Community gym',
      'capacity': 25,
      'open_time': '06:00:00',
      'close_time': '22:00:00',
      'slot_duration_minutes': 60,
      'is_active': true,
    });

    expect(amenity.name, 'Rain forest');
    expect(amenity.amenityType, 'gym');
    expect(amenity.hoursLabel, '6:00 AM - 10:00 PM');
  });

  test('amenityImageAsset maps types to local images', () {
    expect(amenityImageAsset('gym'), 'images/gym.jpg');
    expect(amenityImageAsset('badminton_court'), 'images/badminton_court.jpg');
    expect(amenityImageAsset('tennis_court'), 'images/tennis_court.jpg');
    expect(amenityImageAsset('pool'), 'images/swimming_pool.jpg');
  });
}
