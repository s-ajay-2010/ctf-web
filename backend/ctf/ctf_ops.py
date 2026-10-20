from django.http import JsonResponse
from django.db.models import Sum
from django.db import transaction
from . import models
import csv
from io import StringIO

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
    hcs   = request.POST.get("hint_costs", "").strip() #hci == h_cs == hint_costs
    ai    = request.POST.get("asset", "").strip() #ai == asset_ip == asset_input
    fl    = request.POST.get("file_link", "").strip()

    if not athr or not title or not desc or not flag or not pi or not ctg or not diff or not hints or not hcs or not ai:
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
        hcs = next(csv.reader(StringIO(hcs)))
        hints = next(csv.reader(StringIO(hints)))
        hcs = [int(hc.strip()) for hc in hcs]
    except (TypeError, ValueError, StopIteration):
        return JsonResponse({
            "error": "are you dumb? how the fuck is a points and point deduction value not-a-number for you? and HOW THA HAIL IS hint random ahh for you? dumass"
        }, status=400)

    hints = [h.strip() for h in hints]

    if not hints or not hcs:
        return JsonResponse({
            "error": "have atleast a single hint and hint cost vro sobb"
        }, status=400)

    if pts < 0 or len(hints) != len(hcs) or any(not h for h in hints) or any(hc < 0 for hc in hcs):
        return JsonResponse({
            "error": "yes bro we gonna give negative points, nice!!"
        }, status=400)

    with transaction.atomic():
        ctf = models.CTF.objects.create(
            athr = athr,
            title = title,
            desc = desc,
            flag = flag,
            pts = pts,
            ctg = ctg,
            diff = diff,
            asset = asset,
            fl = fl
        )

        for hint, hc in zip(hints, hcs):
            models.Hints.objects.create(
                c = ctf,
                hints = hint,
                hc = hc
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
            "error": "challenge doesn't exist, idk what blud doin with his life"
        }, status=404)
    

    title = request.POST.get("title", "").strip()
    desc  = request.POST.get("description", "").strip()
    flag  = request.POST.get("flag", "").strip()
    pi    = request.POST.get("points", "").strip() #pi == pts_ip == points_input
    ctg   = request.POST.get("category", "").strip()
    diff  = request.POST.get("difficulty", "").strip()
    hints = request.POST.get("hints", "").strip()
    # hci   = request.POST.get("hint_cost", "").strip() #hci == hc_ip ==  hint_cost
    ai    = request.POST.get("asset", "").strip() #ai == asset_ip == asset_input
    fl    = request.POST.get("file_link", "").strip()

    if not title or not desc or not flag or not pi or not ctg or not diff or not hints or not ai:
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
        hints = next(csv.reader(StringIO(hints)))
    except (TypeError, ValueError, StopIteration):
        return JsonResponse({
            "error": "are you dumb? how the fuck is a points and point deduction value not-a-number for you? and HOW THA HAIL IS hint random ahh for you? dumass"
        }, status=400)

    hints = [h.strip() for h in hints]

    if pts < 0 or any(not h for h in hints):
        return JsonResponse({
            "error": "yes bro we gonna give negative points and/or hints are ghosts, nice!!"
        }, status=400)

    old_hints = list(models.Hints.objects.filter(c=ctf).order_by("id"))

    if len(hints) != len(old_hints):
        return JsonResponse({
            "error": "hint counts exist for a reason vro, we ain't gonna have ghost hint costs"
        }, status=400)

    with transaction.atomic():
        ctf.title = title
        ctf.desc = desc
        ctf.flag = flag
        ctf.pts = pts
        ctf.ctg = ctg
        ctf.diff = diff
        ctf.asset = asset
        ctf.fl = fl
        ctf.save()

        for hint_obj, hint_text in zip(old_hints, hints):
            hint_obj.hints = hint_text
            hint_obj.save(update_fields=["hints"])
    
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
            "error": "challenge doesn't exist, idk what blud doin with his life"
        }, status=404)

    ctf.delete()

    return JsonResponse({
        "message" : "challenge deleted just like your happiness, hope you feel better now",
        "id" : cid
    }, status=200)

def hint_get(request, cid, hid):
    if request.method != "POST":
        return JsonResponse({
            "error": "POST requests only gng"
        }, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({
            "error": "you're NOT logged in, login vro"
        }, status=401)

    try:
        ctf = models.CTF.objects.get(pk=cid)
        hint = models.Hints.objects.get(pk=hid, c=cid)

    except (models.CTF.DoesNotExist, models.Hints.DoesNotExist):
        return JsonResponse({
            "error": "challenge or hint doesn't exist, idk what blud doin with his life"
        }, status=404)

    models.Profile.objects.get_or_create(user=request.user)

    with transaction.atomic():
        profile = models.Profile.objects.select_for_update().get(user=request.user)

        if models.Submission.objects.filter(user=request.user, c=ctf).exists():
            return JsonResponse({
                "error": "you've already solved this challenge, no need for hints now"
            }, status=409)

        models.HintUse.objects.get_or_create(user=request.user, hint=hint)

        return JsonResponse({
            "message": "here are your hints, atleast get these hints",
            "hint": hint.hints,
            "cost": hint.hc
        }, status=200)

#ch_sb = challenge_submit
def ch_sb(request, cid):
    if request.method != "POST":
        return JsonResponse({
            "error": "POST requests only gng"
        }, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({
            "error": "you're NOT logged in, login vro"
        }, status=401)

    flag = request.POST.get("flag", "").strip()
    if not flag:
        return JsonResponse({
            "error": "where the fuck is my flag bro?"
        }, status=400)

    try:
        ctf = models.CTF.objects.get(pk=cid)
    except models.CTF.DoesNotExist:
        return JsonResponse({
            "error": "challenge doesn't exist, idk what blud doin with his life"
        }, status=404)

    if flag != ctf.flag:
        return JsonResponse({
            "error": "wrong flag:("
        }, status=400)

    models.Profile.objects.get_or_create(user=request.user)

    with transaction.atomic():
        profile = models.Profile.objects.select_for_update().get(user=request.user)

        if models.Submission.objects.filter(user=request.user, c=ctf).exists():
            return JsonResponse({
                "error": "already solved!!"
            }, status=409)

        used = models.HintUse.objects.filter(user=request.user, hint__c=ctf)
        hu   = used.count()
        cost = used.aggregate(total=Sum("hint__hc"))["total"] or 0
        pa   = max(0, ctf.pts - cost)

        models.Submission.objects.create(
            c     = ctf,
            user  = request.user,
            hu    = hu,
            pa    = pa
        )

        profile.points += pa
        profile.save(update_fields=["points"])

        return JsonResponse({
            "message": "challenge solved",
            "points": pa,
            "hints used": hu,
            "total_points": profile.points
        }, status=201)


