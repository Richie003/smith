from django.urls import path
from .views import *

urlpatterns = [
    path("sign-up/", sign_up, name="signup"),
    path("sign-in/", sign_in, name="signin"),
    path("sign-out/", SignOut, name="logout"),
]
