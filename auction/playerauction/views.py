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
            user = Login.objects.get(email=data.get('email'))
            print(user.email)
            if user.password == getPassword(data.get("password")):
                if(user):
                    # Auction Admin
                    if(user.role == 1):
                        return render(request, "admin_home.html",{})
                    
                    # Player
                    elif(user.role == 3):

                        player = Player.objects.filter(email=data.get("email"))
                        request.session['player'] = player
                        return render(request, "player_profile.html",{})

                    # Team
                    elif(user.role == 2):
                        return render(request, "team_home.html",{})
        except Exception as e:
            return HttpResponse(content=e)

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
            player.passwoord = data.get('password')
            player.age = data.get('age')
            player.role = data.get("role")
            player.battingStyle = data.get('battingStyle')
            player.bowlingStyle = data.get('bowlingStyle')
            player.password = data.get('password')
            player.gender = 1 if data.get('gender') == "male" else 0
            player.image = ""
            player.playerId = data.get('userId')
            print(data.get('image'))
            try:
                if(player.save()):
                    newlogin = Login
                    newlogin.email = player.email
                    newlogin.password = player.password
                    newlogin.role = 3
                    newlogin.save()

                    request.session['player'] = player
                    response = {
                        "Status":"Ok",
                        "message":"Registered successfully"
                    }
                else:
                    response = response = {
                        "Status":"Error",
                        "message":"Player Already Exists"
                    }
            except Exception as e:
                return HttpResponse(e)
            else:
                return redirect("player_profile")
    return render(request, 'player_register.html', {})

def live_auction(request):
    return render(request, 'live_auction.html', {})

def old_auction(request):
    return render(request, 'old_auction.html', {})

def player_profile(request):
    if request.session.get("user"):
        return render(request, 'player_profile.html', {})
    else:
        return HttpResponse(content="<script>alert('You have to login first'); window.location.assign('/login'); </script>")

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