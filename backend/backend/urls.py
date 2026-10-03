from django.contrib import admin
from django.urls import path
from . import auth
from . import root

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", auth.login),
    path("logout/", auth.logout),
    path("register/", auth.register),
    path("", root.alive),
]
