from django.db import models
from auth_user.models import RestaurantBio
from django.conf import settings
from django.utils import timezone


# Create your models here.
class Table(models.Model):
    restaurant = models.ForeignKey(
        RestaurantBio, on_delete=models.CASCADE, related_name="tables"
    )
    table_number = models.CharField(max_length=10)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return str(self.table_number)


class Reservation(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    table = models.ForeignKey(
        Table, on_delete=models.CASCADE, related_name="reservations"
    )
    reservation_time = models.DateTimeField()
    num_guests = models.PositiveIntegerField()
    special_requests = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
        ("no_show", "No Show"),
    ]
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="confirmed"
    )

    def __str__(self):
        return f"Reservation by {self.customer.username} for {self.num_guests} at {self.reservation_time}"


class BookingDiary(models.Model):
    restaurant = models.ForeignKey(
        RestaurantBio, on_delete=models.CASCADE, related_name="booking_diary"
    )
    date = models.DateField(default=timezone.now)
    reservations = models.ManyToManyField(Reservation, related_name="diaries")

    def __str__(self):
        return f"Booking Diary for {self.restaurant.name} on {self.date}"
