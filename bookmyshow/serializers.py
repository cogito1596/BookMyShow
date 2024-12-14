from rest_framework import serializers


class CreateBookingRequestDto(serializers.Serializer):
    movie_id = serializers.UUIDField()
    show_id = serializers.UUIDField()
    user_id = serializers.IntegerField()
    number_of_seats = serializers.IntegerField()
    booking_date = serializers.DateField()
    booking_time = serializers.TimeField()
    total_amount = serializers.FloatField()
    seat_ids = serializers.ListField(
        child=serializers.UUIDField(), help_text="List of UUIDs of the seats"
    )
