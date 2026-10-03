from django.db import models
from django.contrib.auth.models import User


#I really want to use "user", but fuck django, "user" is taken by it, so y'all get the lame ahh "profile":(
class Profile(models.Model):
    user   = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    bio    = models.CharField(max_length=200, blank=True)
    ia     = models.BooleanField(default=False) #is_admin


class CTF(models.Model):
    id    = models.BigAutoField(primary_key=True)
    athr  = models.ForeignKey(User, on_delete=models.CASCADE, related_name="challenges") #author
    title = models.CharField(max_length=40, blank=False)
    desc  = models.CharField(max_length=100, blank=False) #decription
    flag  = models.CharField(max_length=50, blank=False)
    pts   = models.IntegerField(default=10) #points
    ctg   = models.CharField(max_length=30, blank=False) #category
    diff  = models.CharField(max_length=10, blank=False) #diffculty
    hints = models.CharField(max_length=200, blank=False)
    hc    = models.IntegerField(blank=False) #hint_cost, i.e. the points you loose for hint reveal
    asset = models.BooleanField(default=False) #any file present to be downloaded?
    fl    = models.CharField(max_length=500, blank=True) #file_link

class Submission(models.Model):
    id    = models.BigAutoField(primary_key=True)
    c     = models.ForeignKey(CTF, on_delete=models.CASCADE) #challenge(_id)
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    hu    = models.IntegerField(default=0) #the hints used count
    pa    = models.IntegerField() #points awarded, NOT the project's property, defined for a user's submission