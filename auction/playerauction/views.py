from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from appdata.models import Player, Auction, AuctionAdmin, AuctionPlayer, Team, Login
from playerauction.validate import *
from sqlite3 import IntegrityError
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from appdata.forms import *
import json
from django.http import JsonResponse

# Create your views here.

def index(request):
    return render(request, 'index.html', {})

def login(request, user):
    if(request.session.get('user') != None):
        return redirect('index')

    if request.method == "POST":
        print(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        role  = request.POST.get("role")
        
        try:
            if role == '3':
                player = Player.objects.get(email=email)
                encoded = player.password
                request.session['user'] = player.name
                

            elif role == '2':
                team = Team.objects.get(email=email)
                encoded = team.password
                request.session['user'] = team.name

            elif role == '1':
                admin = AuctionAdmin.objects.get(email=email)
                encoded = admin.password
                request.session['user'] = admin.name
                

            if check_password(password, encoded):
                return render(request, 'index.html', {})
        except Exception as e:
            return render(request, "error.html", {"Error":"Player Does Not Exists"})
    return render(request, 'login.html', {"user":user})


def register(request):
    
    if request.method == "POST":
        try:
            captain = Player.objects.get(playerId=request.POST.get("captainId"))
            team = TeamForm(request.POST)
            print(captain)
            
            if(team.is_valid()):
                team = team.save(commit=False)
                team.captainId = captain
                team.save()
                request.session['name'] = team.name 
                request.session['teamId'] = team.teamId 
                request.session['user'] = team.email 
                return HttpResponseRedirect('teamprofile')
            else:
                raise IntegrityError("User Already Exists")

        except IntegrityError as e:
            print("Team Already Exists")
            return render(request, 'Error.html', {"Error":"User Already Exists"})


        except Exception as e:
            print(e)
    reg = request.GET.get("reg")
    if reg:
        return render(request, 'register.html', {"reg":reg})



def player_register(request):
    if(request.session.get('user') != None):
        return redirect('index')
    if request.method == "POST":
        print("POST method")
        player = PlayerForm(request.POST)

        if player.is_valid():
            player.save()
            request.session['session'] = player
            return render(request, "player_profile.html", {"session": request.session})
        else:
            return render(request, 'Error.html', {"Error":"Player Already Exists"})
    else:
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

def logout(request):
    request.session.flush()
    return render(request, 'index.html', {})

def getCaptain(request):
    if request.method == "POST":
        try:
            
            data = json.loads(request.body.decode('utf-8'))
            captain = data.get("captain","")

            captainObj = Player.objects.get(playerId=captain)
            return JsonResponse({"content":"Captain Choosen Succesfully", "code":200})
        except Exception as e:

            return JsonResponse({"content":"Player Does not exists", "code":404})
