from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.http import JsonResponse


def register(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    email = request.POST.get("email")

    if not (username and password and email):
        return JsonResponse({
            "error": "missing fields",
            "error_2": "you're gay",
        }, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({
            "error": "username taken bud:("
        }, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)
    return JsonResponse({
        "message": "user created successfully",
        "username": user.username,
        "email": user.email,
    }, status=201)


def login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    if not (username and password):
        return JsonResponse({
            "error": "missing username and/or password",
            "error_2": "r u dumb or r u just gay? call it..."
        }, status=400)

    user = authenticate(request, username=username, password=password)

    if user is not None:
        auth_login(request, user)
        return JsonResponse({
            "message": "Logged in!!!",
            "is_admin": user.is_staff,
        })


    return JsonResponse({
        "error": "Invalid username or password:("
    }, status=401)

def logout(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            "error": "are you actually logged in?",
        }, status=400)

    auth_logout(request)    
    return JsonResponse({
        "message": "logged out",
    })