from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from .models import *
from .forms import *
from datetime import datetime
from auth_user.models import RestaurantBio, CustomerBio
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


@login_required
def getRestaurants(request):
    get_restaurants = RestaurantBio.objects.all()
    context = {"restaurants": get_restaurants}
    return render(request, "home.html", context)


@login_required
def getTables(request, pk):
    get_tables = Table.objects.filter(restaurant_id=int(pk))
    total_table = get_tables.count
    context = {"tables": get_tables, "total": total_table}
    return render(request, "tables.html", context)


@login_required
def viewTableReservations(request, pk):
    get_table = get_object_or_404(Table, id=pk)
    reservations = Reservation.objects.filter(table_id=int(pk))

    reservation_exists = Reservation.objects.filter(
        customer_id=request.user.id, table_id=get_table.id
    ).exists()
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.customer_id = request.user.id
            instance.table_id = get_table.id
            if not reservation_exists:
                instance.save()
                return JsonResponse("Success.", safe=False)
            else:
                return JsonResponse(
                    "Reservations can't be made twice until previous reservations are expired",
                    safe=False,
                )
        else:
            return JsonResponse("Failed.", safe=False)
    else:
        form = ReservationForm()
    context = {"form": form, "reservations": reservations, "table": get_table}
    return render(request, "reservations.html", context)


@csrf_exempt
def deleteReservations(request, pk):
    if request.method == "DELETE":
        _, deleted = Reservation.objects.get(id=int(pk)).delete()
        if deleted:
            return JsonResponse("Successfully deleted", safe=False)
        else:
            return JsonResponse("Delete unsuccessful!")


def dateChecks(request):
    if request.method == "GET":
        try:
            table_id = request.GET.get("ID")
            time_picked = request.GET.get("time_picked")
            data = [
                i.reservation_time.strftime("%Y-%m-%dT%H:%M")
                for i in Reservation.objects.filter(table_id=table_id)
            ]
            print(data)
            if time_picked in data:
                return JsonResponse("Taken", safe=False)
            else:
                return JsonResponse("Available", safe=False)
        except Exception as e:
            return JsonResponse(str(e), safe=False)
    return JsonResponse("")


def add_table(request):
    if request.method == "POST":
        user = RestaurantBio.objects.get(owned_by_id=request.user.id)
        table_name = request.POST["table_name"]
        table_capacity = request.POST["capacity"]
        add_table, created = Table.objects.get_or_create(
            restaurant_id=user.id, table_number=table_name, capacity=table_capacity
        )
        if created:
            return JsonResponse("Added successfully!", safe=False)
        else:
            return JsonResponse(
                f"*FAILED: Table {table_name} already exists", safe=False
            )
