from django.urls import path
from .views import *

urlpatterns = [
    path("", getRestaurants),
    path("<int:pk>/tables/", getTables, name="tables"),
    path("tables/restaurant/<int:pk>/", viewTableReservations, name="reservations"),
    path("check-dates/", dateChecks),
    path("add-table/", add_table),
    path("delete/<int:pk>/", deleteReservations),
]
