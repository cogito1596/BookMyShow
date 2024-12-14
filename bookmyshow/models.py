from django.db import models
import uuid


# Create your models here.
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Region(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Location(BaseModel):
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name


class Theatre(BaseModel):
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Feature(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Screen(BaseModel):
    name = models.CharField(max_length=255)
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    features = models.ManyToManyField(Feature)

    def __str__(self):
        return self.name


class Languages(models.TextChoices):
    ENGLISH = "EN", "English"
    HINDI = "HI", "Hindi"
    TAMIL = "TA", "Tamil"
    TELUGU = "TE", "Telugu"
    KANNADA = "KA", "Kannada"
    MALAYALAM = "MA", "Malayalam"


class Movie(BaseModel):
    name = models.CharField(max_length=255)
    duration = models.DurationField()
    language = models.CharField(max_length=2, choices=Languages.choices)

    def __str__(self):
        return self.name


class Show(BaseModel):
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    feature = models.ManyToManyField(Feature, through="ShowFeature")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.screen} - {self.movie} - {self.start_time}"


class ShowFeature(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    is_applicable = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.feature} for {self.show}"


class SeatType(models.TextChoices):
    VIP = "VIP", "VIP"
    EXECUTIVE = "EXEC", "Executive"
    NORMAL = "NORMAL", "Normal"
    Recliner = "RECL", "Recliner"


class Seat(BaseModel):
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    row_number = models.PositiveIntegerField()
    seat_number = models.PositiveIntegerField()
    col_number = models.PositiveIntegerField()
    seat_type = models.CharField(max_length=6, choices=SeatType.choices)

    def __str__(self):
        return f"{self.screen} - {self.name} - {self.type}"


class ShowSeatStatus(models.TextChoices):
    AVAILABLE = "AVL", "Available"
    BOOKED = "BOK", "Booked"
    BLOCKED = "BLK", "Blocked"
    RESERVED = "RES", "Reserved"


class ShowSeat(BaseModel):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    seat_status = models.CharField(max_length=3, choices=ShowSeatStatus.choices)

    def __str__(self):
        return f"{self.show} - {self.seat}"


class ShowSeatType(BaseModel):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    seat_type = models.CharField(max_length=6, choices=SeatType.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.show} - {self.seat_type} - {self.price}"


class BookingStatus(models.TextChoices):
    PENDING = "PEN", "Pending"
    CONFIRMED = "CON", "Confirmed"
    CANCELLED = "CAN", "Cancelled"
    REFUNDED = "REF", "Refunded"


class PaymentStatus(models.TextChoices):
    PENDING = "PEN", "Pending"
    SUCCESS = "SUC", "Success"
    FAILED = "FAL", "Failed"


class PaymentMethod(models.TextChoices):
    CASH = "CAS", "Cash"
    CARD = "CAR", "Card"
    UPI = "UPI", "UPI"
    NETBANKING = "NET", "Netbanking"
    WALLET = "WAL", "Wallet"


class Payment(BaseModel):
    ticket = models.ForeignKey("Ticket", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=3, choices=PaymentStatus.choices)
    method = models.CharField(max_length=3, choices=PaymentMethod.choices)

    def __str__(self):
        return f"{self.ticket} - {self.amount} - {self.status}"


class Ticket(BaseModel):
    ticket_number = models.CharField(max_length=255, unique=True)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    status = models.CharField(max_length=3, choices=BookingStatus.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.show} - {self.seat} - {self.user}"


class TicketSeat(BaseModel):
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="ticket_seats"
    )
    show_seat = models.ForeignKey(ShowSeat, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Ticket: {self.ticket.ticket_number} - Seat: {self.show_seat.seat}"
