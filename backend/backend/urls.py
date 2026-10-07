from django.contrib import admin
from django.urls import path
from . import auth
from . import root
from ctf import ctf_ops

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", auth.login),
    path("logout/", auth.logout),
    path("register/", auth.register),
    path("", root.alive),
    path("ctf/create/", ctf_ops.ch_cr),
]
