from django.shortcuts import render
import json
from django.http import JsonResponse
from sqlite3 import IntegrityError
from django.contrib.auth.hashers import check_password
from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from appdata.models import Player, Auction, AuctionAdmin, AuctionPlayer, Team, Login, Auction_teams
from appdata.forms import AdminForm

# Create your views here.
def auction_admin(request):
    print(request.session.get("user"))
    if request.session.get('user') and request.session.get("user") == 1:
        return render(request, 'auction_admin.html', {})
    else:
        return render(request, "error.html", {'Error':"Unauthorized User Access : 403"})

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
        
        
        return HttpResponseRedirect('/auctionadmin/login')
    else:
        return render(request, 'adminReg.html', {})


def adminHome(request):

    if request.session.get('user') and request.session.get("user") == 1:
        return render(request,'admin_home.html',{})

    else:
        return render(request, "error.html", {'Error':"Unauthorized User Access : 403"})

def getForm(request):
    return render(request, "forms/createauction.html",{})

def create_auction(request):
    if request.session.get('user') and request.session.get("user") == 1:
        return render(request, 'create_auction.html', {})
    else:
        return render(request, "error.html", {'Error':"Unauthorized User Access : 403"})


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
                teamId = Team.objects.get(teamId=request.POST.get("teamId"))

                if Auction_teams.objects.get(teamId=teamId.id):
                    raise IntegrityError("Team Already In the Auction.")

                auctionid = request.POST.get("auctionid")
                auction = Auction.objects.get(id=auctionid)

                auctionTeam = Auction_teams()
                auctionTeam.auctionId = auction
                auctionTeam.teamId = teamId
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

