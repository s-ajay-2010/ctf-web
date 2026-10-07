from django.http import JsonResponse
from . import models

#ch_cr == challenge_create
def ch_cr(request):
    if not request.user.is_staff:
        return JsonResponse({
            "error": "you're NOT staff, fuck off bitch"
        }, status=403)

    athr  = request.user
    title = request.POST.get("title")
    desc  = request.POST.get("description")
    flag  = request.POST.get("flag")
    pi    = request.POST.get("points") #pi == pts_ip == points_input
    ctg   = request.POST.get("category")
    diff  = request.POST.get("difficulty")
    hints = request.POST.get("hints")
    hci   = request.POST.get("hint_cost") #hci == hc_ip == hint_cost
    ai    = request.POST.get("asset") #ai == asset_ip == asset_input
    fl    = request.POST.get("file_link")

    if not athr or not title or not desc or not flag or not pi or not ctg or not diff or not hints or not hci or not ai:
        return JsonResponse({
            "error": "where are my values vro? we cannot make ghost objects sobb"
        }, status=400)

    if ai.lower() not in ["true", "false"]:
        return JsonResponse({
            "error": "bro I asked if an file/asset was there, not random life choice explanations, okay?!"
        }, status=400)

    asset = ai.lower() == "true"
    
    if asset and not fl:
        return JsonResponse({
            "error": "files cannot spawn out of thin air, give link bruh"
        }, status=400)
    
    try:
        pts = int(pi)
        hc  = int(hci)
    except (TypeError, ValueError):
        return JsonResponse({
            "error": "are you dumb? how the fuck is a points and point deduction value not-a-number for you? dumass"
        }, status=400)

    if hc < 0 or pts < 0:
        return JsonResponse({
            "error": "yes bro we gonna give negative points, nice!!"
        }, status=400)


    ctf = models.CTF.objects.create(
        athr  = athr,
        title = title,
        desc  = desc,
        flag  = flag, 
        pts   = pts,
        ctg   = ctg,
        diff  = diff,
        hints = hints,
        hc    = hc,
        asset = asset,
        fl    = fl
    )

    return JsonResponse({
        "message": "challenge created, lets go babyy!!, collect your id below(loose it noone cares loll)",
        "id": ctf.id,
    }, status=201)