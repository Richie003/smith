from django.shortcuts import render, redirect
from .forms import *
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def sign_up(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data.get("username")
            form.save()
            return JsonResponse(
                {"message": f"Account creation successful for {name}"}, safe=False
            )
        else:
            message = form.error_messages
            print(message)
    context = {"form": form}
    return render(request, "auths/signup.html", context)


def sign_in(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            else:
                return redirect("/")
        else:
            return JsonResponse("User doesn't exist.", safe=False)
    return render(request, "auths/signin.html", context={})


def SignOut(request):
    logout(request)
    return redirect("signin")
