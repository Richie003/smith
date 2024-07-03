from django import forms
from .models import Reservation
from auth_user.models import User


class ReservationForm(forms.ModelForm):
    reservation_time = forms.DateTimeField(
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "id": "calendar"},
            format="%Y-%m-%dT%H:%M",
        ),
    )

    class Meta:
        model = Reservation
        fields = [
            "reservation_time",
            "num_guests",
        ]
        error_messages = {
            "reservation_time": {
                "invalid": "Enter a valid date and time..",
            },
        }
