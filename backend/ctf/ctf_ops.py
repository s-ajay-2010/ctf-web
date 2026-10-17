from django.http import JsonResponse
from . import models

#ch_cr == challenge_create
def ch_cr(request):
    if request.method != "POST":
        return JsonResponse({
            "error": "POST requests only gng"
        }, status=405)

    if not request.user.is_staff:
        return JsonResponse({
            "error": "you're NOT staff, fuck off bitch"
        }, status=403)

    athr  = request.user
    title = request.POST.get("title", "").strip()
    desc  = request.POST.get("description", "").strip()
    flag  = request.POST.get("flag", "").strip()
    pi    = request.POST.get("points", "").strip() #pi == pts_ip == points_input
    ctg   = request.POST.get("category", "").strip()
    diff  = request.POST.get("difficulty", "").strip()
    hints = request.POST.get("hints", "").strip()
    hci   = request.POST.get("hint_cost", "").strip() #hci == hc_ip == hint_cost
    ai    = request.POST.get("asset", "").strip() #ai == asset_ip == asset_input
    fl    = request.POST.get("file_link", "").strip()

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

#ch_ed == challenge_edit
def ch_ed(request, cid):
    if request.method != "POST":
        return JsonResponse({
            "error": "POST requests only gng"
        }, status=405)

    if not request.user.is_staff:
        return JsonResponse({
            "error": "you're NOT staff, fuck off bitch"
        }, status=403)

    try:
        ctf = models.CTF.objects.get(id=cid)
    except models.CTF.DoesNotExist:
        return JsonResponse({
            "error": "challenge doesn't exist, idk what blud doin with his life🥀🥀"
        }, status=404)
    

    title = request.POST.get("title", "").strip()
    desc  = request.POST.get("description", "").strip()
    flag  = request.POST.get("flag", "").strip()
    pi    = request.POST.get("points", "").strip() #pi == pts_ip == points_input
    ctg   = request.POST.get("category", "").strip()
    diff  = request.POST.get("difficulty", "").strip()
    hints = request.POST.get("hints", "").strip()
    hci   = request.POST.get("hint_cost", "").strip() #hci == hc_ip ==  hint_cost
    ai    = request.POST.get("asset", "").strip() #ai == asset_ip == asset_input
    fl    = request.POST.get("file_link", "").strip()

    if not title or not desc or not flag or not pi or not ctg or not diff or not hints or not hci or not ai:
        return JsonResponse({
            "error": "where are my values vro? we add ghost values to objects sobb"
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

    ctf.title = title
    ctf.desc = desc
    ctf.flag = flag
    ctf.pts = pts
    ctf.ctg = ctg
    ctf.diff = diff
    ctf.hints = hints
    ctf.hc = hc
    ctf.asset = asset
    ctf.fl = fl

    ctf.save()

    return JsonResponse({
        "message": "edited successfulyy!! you've succeeded for once in life",
        "id": ctf.id
    }, status=200)

#ch_del == challenge_delete
def ch_del(request, cid):
    if request.method != "POST":
        return JsonResponse({
            "error": "POST requests only gng"
        }, status=405)

    if not request.user.is_staff:
        return JsonResponse({
            "error": "you're NOT staff, fuck off bitch"
        }, status=403)

    try:
        ctf = models.CTF.objects.get(id=cid)
    except models.CTF.DoesNotExist:
        return JsonResponse({
            "error": "challenge doesn't exist, idk what blud doin with his life🥀🥀"
        }, status=404)

    ctf.delete()

    return JsonResponse({
        "message" : "challenge deleted just like your happiness, hope you feel better now",
        "id" : cid
    }, status=200)