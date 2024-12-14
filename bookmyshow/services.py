from .models import Seat, ShowSeat, Show, ShowSeatStatus, Ticket, BookingStatus
from django.contrib.auth.models import User
import uuid
from django.db import transaction


class BookMyShowService:
    def create_booking(self, user_id, show_id, seat_ids):
        if len(seat_ids) > 10:
            raise ValueError("Cannot book more than 10 seats")
        user = User.objects.get(id=user_id)
        if user is None:
            raise ValueError("User not found")
        show = Show.objects.get(id=show_id)
        seats = Seat.objects.filter(id__in=seat_ids)
        show_seats = ShowSeat.objects.filter(show=show, seat__in=seats)

        for show_seat in show_seats:
            if show_seat.seat_status != ShowSeatStatus.AVAILABLE:
                raise ValueError("Seat is not available")
        for show_seat in show_seats:
            show_seat.seat_status = ShowSeatStatus.BOOKED
            show_seat.save()
        with transaction.atomic():
            # Create the ticket
            ticket = Ticket.objects.create(
                user=user,
                amount=1000,  # Replace with dynamic pricing logic if needed
                status=BookingStatus.PENDING,
                ticket_number=str(uuid.uuid4()),
                show=show,
            )

            for show_seat in show_seats:
                show_seat.seat_status = ShowSeatStatus.BLOCKED
                show_seat.ticket = ticket
                show_seat.save()
            ticket.seats = [
                {"row": s.seat.row_number, "number": s.seat.seat_number}
                for s in show_seats
            ]
        return ticket
