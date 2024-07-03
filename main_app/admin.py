from django.contrib import admin
from .models import *


class TableAdmin(admin.ModelAdmin):
    list_display = ("table_number", "restaurant", "capacity")
    list_filter = ("restaurant",)
    search_fields = ("table_number", "restaurant__name")


class ReservationAdmin(admin.ModelAdmin):
    list_display = ("customer", "table", "reservation_time", "num_guests", "status")
    list_filter = ("status", "reservation_time", "table__restaurant")
    search_fields = (
        "customer__username",
        "table__table_number",
        "table__restaurant__name",
    )
    date_hierarchy = "reservation_time"


class BookingDiaryAdmin(admin.ModelAdmin):
    list_display = ("restaurant", "date")
    list_filter = ("restaurant", "date")
    search_fields = ("restaurant__name",)
    date_hierarchy = "date"


admin.site.register(Table, TableAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(BookingDiary, BookingDiaryAdmin)
