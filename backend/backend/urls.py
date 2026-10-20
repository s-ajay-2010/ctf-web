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
    path("ctf/edit/<int:cid>/", ctf_ops.ch_ed),
    path("ctf/delete/<int:cid>/", ctf_ops.ch_del),
    path("ctf/<int:cid>/hints/<int:hid>/", ctf_ops.hint_get),
    path("ctf/<int:cid>/submit/", ctf_ops.ch_sb),
]
