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
        entity  = request.POST.get("user")
        
        try:
            if entity == '3':
                user = Player.objects.get(email=email)
                encoded = user.password
                request.session['user'] = 3
                

            elif entity == '2':
                user = Team.objects.get(email=email)
                encoded = user.password
                request.session['user'] = 2

            elif entity == '1':
                user = AuctionAdmin.objects.get(email=email)
                encoded = user.password
                request.session['user'] = 1
            
            if check_password(password, encoded):
                return HttpResponseRedirect('/')


        except Exception as e:
            return render(request, "error.html", {"Error":"User Not Found"})
            # return render(request, "error.html", {"Error":"User Does Not Exists"})
    return render(request, 'login.html', {"user":user})


def register(request):
    if(request.session.get('user') != None):
        return redirect('index')

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
            return HttpResponseRedirect('player/login',{'message':'player'})
        else:
            return render(request, 'Error.html', {"Error":"Player Already Exists"})
    else:
        return render(request, 'player_register.html', {})


def live_auction(request):
    return render(request, 'live_auction.html', {})

def old_auction(request):
    return render(request, 'old_auction.html', {})

def player_profile(request):
    if request.session.get("user") and request.session.get("user") == 3:
        return render(request, 'player_profile.html', {})
    else:
        return render(request, "error.html", {'Error':"Unauthorized User Access : 403"})

def create_auction(request):
    if request.session.get('user') and request.session.get("user") == 1:
        return render(request, 'create_auction.html', {})
    else:
        return render(request, "error.html", {'Error':"Unauthorized User Access : 403"})
def auction_admin(request):
    print(request.session.get("user"))
    if request.session.get('user') and request.session.get("user") == 1:
        return render(request, 'auction_admin.html', {})
    else:
        return render(request, "error.html", {'Error':"Unauthorized User Access : 403"})
def player_summery(request):
    return render(request, 'player_summery.html', {})

def helppage(request):
    return render(request, 'helppage.html', {})

def teamHome(request):
    if request.session.get('user') and request.session.get("user") == 2:
        return render(request,'team_home.html')
    else:
        return render(request, "error.html", {'Error':"Unauthorized User Access : 403"})
def logout(request):
    request.session.flush()
    return HttpResponseRedirect('/')

def getCaptain(request):
    if request.method == "POST":
        try:
            
            data = json.loads(request.body.decode('utf-8'))
            captain = data.get("captain","")

            captainObj = Player.objects.get(playerId=captain)
            return JsonResponse({"content":"Captain Choosen Succesfully", "code":200})
        except Exception as e:

            return JsonResponse({"content":"Player Does not exists", "code":404})

def adminReg(request):
    if(request.session.get('user') != None):
        return redirect('index')
    if request.method == "POST":
        try:
            auctionAdmin = AdminForm(request.POST)
            if auctionAdmin.is_valid():
                auctionAdmin.save()

        except Exception as e:
            return render(request, 'error.html', {"Error":e})
        
        
        return HttpResponseRedirect('auctionadmin/login')
    else:
        return render(request, 'adminReg.html', {})

def adminHome(request):

    if request.session.get('user') and request.session.get("user") == 1:
        return render(request,'admin_home.html',{})

    else:
        return render(request, "error.html", {'Error':"Unauthorized User Access : 403"})
