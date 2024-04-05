from django.db import models
from django.contrib.auth.hashers import make_password
from datetime import date

# Create your models here.
max_length_for_id = 40

class AuctionAdmin(models.Model):
    adminId = models.CharField(max_length=40, unique=True, null=False)
    email    = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=256)
    subscription = models.BooleanField(default=True)
    name = models.CharField(max_length=max_length_for_id, null=True)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
    # def __str__
    

class Team(models.Model):
    teamId = models.CharField(max_length=max_length_for_id, unique=True, null=False)
    name    = models.CharField(max_length=35)
    email   = models.EmailField(max_length=200, null=False, unique=True)
    password = models.CharField(max_length=256)
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)
    logo    = models.ImageField(upload_to="team/",default=None, null=True)
    captainId = models.OneToOneField('Player', on_delete=models.DO_NOTHING, null=True, default=None)



class Player(models.Model):
    playerId = models.CharField(max_length=30, unique=True, null=False)
    name      = models.CharField(max_length=30)
    password = models.CharField(max_length=256)
    email    = models.EmailField(max_length=200, unique=True, null=False)
    role      = models.CharField(max_length=50)
    age      = models.IntegerField(null=True)
    battingStyle = models.TextField(null=True, default='')
    bowlingStyle = models.TextField(null=True, default='')
    gender    = models.SmallIntegerField(null=True)
    image     = models.ImageField( upload_to="player/", default='', null=True)
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)


class Login(models.Model):
    role  = models.SmallIntegerField()
    email = models.EmailField(max_length=200, unique=True, null=False)
    password = models.CharField(max_length=256)
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

class Auction(models.Model):
    auctionId = models.CharField(max_length=max_length_for_id, unique=True, null=False)
    auctionName = models.CharField(max_length=50, default='')
    adminId   = models.ForeignKey('AuctionAdmin', on_delete=models.PROTECT)
    date = models.DateField(auto_now=True)
    initialPoint = models.IntegerField(default=0)
    maxBid = models.IntegerField(default=0)
    location = models.CharField(max_length=50)
    status  = models.SmallIntegerField(default=0)
    team  = models.ManyToManyField('Team', through='Auction_teams')


# 0 - Remains, 1 - sold, 2 - unsold
class AuctionPlayer(models.Model):
    auctionId = models.ForeignKey('Auction', on_delete=models.CASCADE)
    playerId = models.ForeignKey('Player', on_delete=models.CASCADE)
    status = models.SmallIntegerField(default=0)
    teamId = models.ForeignKey('Team', on_delete=models.DO_NOTHING, null=True, blank=True)

class CurruntPlayer(models.Model):
    player = models.IntegerField()

class Auction_teams(models.Model):
    auctionId = models.ForeignKey('Auction', on_delete=models.CASCADE)
    teamId    = models.ForeignKey('Team', on_delete=models.CASCADE)
    points    = models.IntegerField(default=0)

