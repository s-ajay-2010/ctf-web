from django.http import JsonResponse

def alive(request):
    return JsonResponse({
        "alive": "fuck yeah",
    }, status= 200)