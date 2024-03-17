from django.db import models
from django.contrib.auth.hashers import make_password
from datetime import date

# Create your models here.
max_length_for_id = 6

class AuctionAdmin(models.Model):
    adminId = models.CharField(max_length=4)
    email    = models.EmailField(max_length=200)
    password = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

class Team(models.Model):
    teamId = models.CharField(max_length=max_length_for_id)
    name    = models.CharField(max_length=35)
    email   = models.EmailField(max_length=200)
    password = models.CharField(max_length=128)
    points  = models.IntegerField(default=0)
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)
    logo    = models.TextField()
    captainId = models.CharField(max_length=max_length_for_id, default=None)


class Player(models.Model):
    playerId = models.CharField(max_length=max_length_for_id)
    name      = models.CharField(max_length=30)
    password = models.CharField(max_length=128)
    email    = models.EmailField(max_length=200,unique=True)
    role      = models.CharField(max_length=50)
    age      = models.IntegerField(max_length=2)
    battingStyle = models.TextField(null=True)
    bowlingStyle = models.TextField(null=True)
    gender    = models.SmallIntegerField(max_length=1)
    image     = models.TextField(default=None, null=True)
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)


class Login(models.Model):
    role  = models.SmallIntegerField(max_length=1)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)


class Auction(models.Model):
    auctionId = models.CharField(max_length=max_length_for_id)
    auctionName = models.CharField(max_length=50)
    adminId   = models.ForeignKey('AuctionAdmin', on_delete=models.PROTECT)
    date = models.DateField(auto_created=True)
    initialPoint = models.IntegerField()
    maxBid = models.IntegerField()
    location = models.CharField(max_length=50)
    status  = models.SmallIntegerField(max_length=1)

class AuctionPlayer(models.Model):
    auctionId = models.ForeignKey('Auction', on_delete=models.CASCADE)
    playerId = models.ForeignKey('Player', on_delete=models.CASCADE)
    status = models.SmallIntegerField(max_length=1)
    teamId = models.ForeignKey('Team', on_delete=models.DO_NOTHING)
