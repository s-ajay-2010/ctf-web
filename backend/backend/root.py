from django.http import JsonResponse

def alive(request):
    return JsonResponse({
        "backend_alive": "fuck yeah",
    }, status= 200)