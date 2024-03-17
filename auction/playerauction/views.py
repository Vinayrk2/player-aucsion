from django.shortcuts import render,redirect
from django.http import HttpResponse
from playerauction.models import Player, Auction, AuctionAdmin, AuctionPlayer, Team, Login
from playerauction.validate import *
from sqlite3 import IntegrityError

# Create your views here.

def index(request):
    return render(request, 'index.html', {})

def login(request):

    if(request.method == "POST"):
        data = request.POST
        try:
            user = Login.objects.get(email=data.get('email'), password=data.get("password"))
            if(user ):
                # Auction Admin
                if(user.role == 1):
                    return redirect("auction_admin")
                
                # Player
                elif(user.role == 3):
                    player = Player.objects.filter(email=data.get("email"))
                    return redirect("player_profile")

                # Team
                elif(user.role == 2):
                    return redirect("team_profile")
        except:
            return HttpResponse(content="Invalid Credentials")

    return render(request, 'login.html', {})

def register(request):
    return render(request, 'register.html', {})

def player_register(request):
    if(request.method == "POST"):
        data = request.POST
    
        if(validateRegistration(1)):
            player = Player()
            player.name = data.get('name')
            player.email = data.get('email')
            player.age = data.get('age')
            player.role = data.get("role")
            player.battingStyle = data.get('battingStyle')
            player.bowlingStyle = data.get('bowlingStyle')
            player.password = data.get('password')
            player.gender = 1 if data.get('gender') == "male" else 0
            player.image = storeImage()
            player.playerId = getPlayerId()

            try:
                if(player.save()):
                    newlogin = Login
                    newlogin.email = player.email
                    newlogin.password = player.password
                    newlogin.role = 3
                    response = {
                        "Status":"Ok",
                        "message":"Registered successfully"
                    }
                else:
                    response = response = {
                        "Status":"Error",
                        "message":"Player Already Exists"
                    }
            except:
                return HttpResponse(content="Error To Register")
            else:
                return redirect("player_profile")
    return render(request, 'player_register.html', {})

def live_auction(request):
    return render(request, 'live_auction.html', {})

def old_auction(request):
    return render(request, 'old_auction.html', {})

def player_profile(request):
    return render(request, 'player_profile.html', {})

def create_auction(request):
    return render(request, 'create_auction.html', {})

def auction_admin(request):
    return render(request, 'auction_admin.html', {})

def player_summery(request):
    return render(request, 'player_summery.html', {})

def helppage(request):
    return render(request, 'helppage.html', {})

def teamHome(request):
    return render(request,'team_home.html')