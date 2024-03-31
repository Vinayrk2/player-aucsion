from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from appdata.models import Player, Auction, AuctionAdmin, AuctionPlayer, Team, Login, Auction_teams
from playerauction.validate import *
from sqlite3 import IntegrityError
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from appdata.forms import *
import json
from django.http import JsonResponse
from django.core import serializers


# Create your views here.

def index(request):
    return render(request, 'index.html', {})

def login(request, user):
    if request.session.get('user') != None:
        return redirect('index')

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        entity  = request.POST.get("user")
        
        try:
            if entity == '3':
                user = Player.objects.get(email=email)
                encoded = user.password
                if check_password(password, encoded):
                    request.session['user'] = 3
                    request.session['id'] = user.playerId
                else:
                    raise Exception("Incorrect Password")
                

            elif entity == '2':
                user = Team.objects.get(email=email)
                encoded = user.password
                if check_password(password, encoded):
                    request.session['user'] = 2
                    request.session['id'] = user.teamId
                else:
                    raise Exception("Incorrect Password")

            elif entity == '1':
                user = AuctionAdmin.objects.get(email=email)
                encoded = user.password
                if check_password(password, encoded):
                    request.session['user'] = 1
                    request.session['id'] = user.adminId
                    request.session['entity'] = user.name
                else:
                    raise Exception("Incorrect Password")                    
            else:
                raise Exception("Invalid Entity")
            
        except Player.DoesNotExist as e:
            return render(request, "error.html", {"Error":"Player Doesnt Exists"})
        except AuctionAdmin.DoesNotExist as e:
            return render(request, "error.html", {"Error":"Admin Doesnt Exists"})
        except Team.DoesNotExist as e:
            return render(request, "error.html", {"Error":"Team Doesnt Exists"})

        except Exception as e:
            return render(request, "error.html", {"Error":e})

            # return render(request, "error.html", {"Error":e})
    
        else:
            return redirect('index')
    else:
        return render(request, 'login.html', {"user":user})


def register(request):
    if(request.session.get('user') != None):
        return redirect('index')

    if request.method == "POST":
        try:
            captain = Player.objects.get(playerId=request.POST.get("captainId"))
            team = TeamForm(request.POST, request.FILES)
            print(captain)
            
            if(team.is_valid()):
                team = team.save(commit=False)
                team.captainId = captain
                team.save()
                return HttpResponseRedirect('team/login')
            else:
                raise IntegrityError(team.errors)
       
        except IntegrityError as e:
            return render(request, 'Error.html', {"Error":e})
       

        except Exception as e:
            return render(request, 'Error.html', {"Error":e})
            
    reg = request.GET.get("reg")
    if reg:
        return render(request, 'register.html', {"reg":reg})



def player_register(request):
    if(request.session.get('user') != None):
        return redirect('index')
    if request.method == "POST":
        try:
            player = PlayerForm(request.POST, request.FILES)

            if player.is_valid():
                player.save()
                return HttpResponseRedirect('player/login',{'message':'player'})
            else:
                # return render(request, 'Error.html', {"Error":"Player Already Exists"})
                return render(request, 'Error.html', {"Error":player.errors})
        except Exception as e:
            return render(request, 'Error.html', {"Error":e})

    else:
        return render(request, 'player_register.html', {})


def live_auction(request):
    return render(request, 'live_auction.html', {})

def old_auction(request):
    return render(request, 'old_auction.html', {})

def player_profile(request):
    if request.session.get("user") and request.session.get("user") == 3:
        player_details = Player.objects.get(playerId=request.session.get("id"))
        player_profile = {
            "name": player_details.name,
            "age" : player_details.age,
            "email": player_details.email,
            "role": player_details.role,
            "battingStyle": player_details.battingStyle,
            "bowlingStyle": player_details.bowlingStyle,
            "gender": player_details.gender,
            "playerId": player_details.playerId
        }
        player_profile["image"] = "" if player_details.image == None else player_details.image.url 
        print(player_profile['image'])
        return render(request, 'player_profile.html', {'profile': player_profile})
    else:
        return render(request, "error.html", {'Error':"Unauthorized User Access : 403"})

def create_auction(request):
    if request.session.get('user') and request.session.get("user") == 1:
        if request.method == "POST":
            auctionid = request.POST.get("auctionId")
            auctionname = request.POST.get("auctionName")
            initPoint = request.POST.get("initialPoint")
            maxBid = request.POST.get("maxBid")
            location = request.POST.get("location")

            auction = Auction()
            auction.auctionId = auctionid
            auction.auctionName = auctionname
            auction.initialPoint = initPoint
            auction.maxBid = maxBid
            auction.adminId = AuctionAdmin.objects.get(adminId=request.session.get("id"))

            auction.save()
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

        team_details = Team.objects.get(teamId=request.session.get('id'))
        team = {
            "id": team_details.teamId,
            "name": team_details.name,
            "email": team_details.email
        }
        team["logo"] =  "" if team_details.logo == None else team_details.logo.url
        return render(request,'team_home.html',{'team':team})
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

def getForm(request):
    return render(request, "forms/createauction.html",{})

def addPlayer(request):
    if request.session.get('user') and request.session.get("user") == 1:
        if request.method == "POST":
            try:
                playerId = request.POST.get('playerId')
                player = Player.objects.get(playerId=playerId)
            except Exception as e:
                return render(request, "error.html", {"Error":"Invalid playerId"})
    else:
        return render(request, "error.html", {'Error':"Unauthorized User Access : 403"})
    players = Player.objects.all()
    return render(request, "forms/addplayer.html", {'playerlist':players})

def addTeam(request):
    if request.session.get('user') and request.session.get("user") == 1:
        if request.method == "POST":
            try:
                teamId = request.POST.get("teamId")

                if Auction_teams.objects.get(teamId=teamId):
                    raise IntegrityError("Team Already In the Auction.")
                team = Team.objects.get(teamId=teamId)

                auctionid = request.POST.get("auctionid")
                auction = Auction.objects.get(id=auctionid)

                auctionTeam = Auction_teams()
                auctionTeam.auctionId = auction
                auctionTeam.teamId = team
                auctionTeam.save()

            except IntegrityError as e:
                # return render(request, "error.html", {"Error":"Team Does Not Exists"})
                return render(request, "error.html", {"Error":e})
       
            except Exception as e:
                # return render(request, "error.html", {"Error":"Team Does Not Exists"})
                return render(request, "error.html", {"Error":e})
        auctions = Auction.objects.filter(adminId=request.session.get('id'))
        teams = Auction_teams.objects.select_related('teamId')

        print(teams)

        return render(request, "forms/addteam.html", {'teams': teams, 'auctions':auctions})
        # return render(request, "forms/addteam.html", {'auctions':auctions})
    else:
        return render(request, "error.html", {'Error':"Unauthorized User Access : 403"})
    
    return render(request, "forms/addTeam.html",{})
    # return HttpResponseRedirect('getform?form=addteam')

