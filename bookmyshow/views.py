from rest_framework import viewsets
from .serializers import CreateBookingRequestDto
from .models import Seat, ShowSeat, Show, Booking
from django.contrib.auth.models import User

# Create your views here.


class BookingViewSet(viewsets.ViewSet):
    def create_booking(self, request):
        serialized_data = CreateBookingRequestDto(data=request.data)
        serialized_data.is_valid(raise_exception=True)
