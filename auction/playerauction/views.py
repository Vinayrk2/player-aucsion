from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from appdata.models import Player, Auction, AuctionAdmin, AuctionPlayer, Team, Login, Auction_teams, CurruntPlayer
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
                    request.session['id'] = user.adminid
                    request.session['entity'] = user.name
                else:
                    raise Exception("Incorrect Password")                    
            else:
                raise Exception("Invalid Entity")
            
        except Player.DoesNotExist as e:
            return render(request, "error.html", {"Error":"Invalid Email or Password", "code":"400", "status":"Bad Request"})
        except AuctionAdmin.DoesNotExist as e:
            return render(request, "error.html", {"Error":"Invalid Email or Password", "code":"400", "status":"Bad Request"})
        except Team.DoesNotExist as e:
            return render(request, "error.html", {"Error":"Invalid Email or Password", "code":"400", "status":"Bad Request" })

        except Exception as e:
            return render(request, "error.html", {"Error":e, "code":"401"})

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
            return render(request, 'Error.html', {"Error":e,"code":"400", "status":"Bad Request"})
       

        except Exception as e:
            return render(request, 'Error.html', {"Error":e, "code":"400", "status":"Bad Request"})
            
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
                return render(request, 'Error.html', {"Error":player.errors, "code":"400", "status":"Bad Request"})
        except Exception as e:
            return render(request, 'Error.html', {"Error":e, "code":"400", "status":"Bad Request"})

    else:
        return render(request, 'player_register.html', {})


def live_auction(request, auctionid):
    # try:
    auction = Auction.objects.get(id=auctionid)
    # teams = auction.team.all()
    teams = Auction_teams.objects.filter(auction__id=auction.id)

    if request.method == 'POST' and request.POST.get('team',0) :
        print(request.POST)
        team = request.POST.get('team')
        bid  = request.POST.get('bid')
        player = request.POST.get('player')
        CurruntPlayer.objects.filter(player=player).delete()

        team = Team.objects.get(id=team)
        player = Player.objects.get(id=player)
        bid = int(bid)
        auctionplayer = AuctionPlayer.objects.get(player=player)
        auctionplayer.teamId = team
        auctionplayer.status = 1
        auctionplayer.save()

        player = AuctionPlayer.objects.filter(auction=auction, status=0, team=None).order_by('?').first()
        currentPlayer = CurruntPlayer.objects.create(player=player.id)
        playerData = Player.objects.get(id=currentPlayer.player)
        return render(request, 'live_auction.html', {"auction":auction, 'teams':teams, 'player':playerData})
        
        
    if request.method == 'POST' and request.POST.get('random',0) : 
        player = AuctionPlayer.objects.filter(auction=auction, status=0,  team=None).order_by('?').first()
        if player:
            playerData = Player.objects.get(id=player.id)
            currentPlayer = CurruntPlayer.objects.create(player=player.id)
            print(player)
            return render(request, 'live_auction.html', {"auction":auction, 'teams':teams, 'player':playerData})
        else:
            auction.status = 2
            auction.save()
            return HttpResponseRedirect('/auctiondone/'+str(auction.id)) 

    if request.method == "POST" and request.POST.get("auction") and auction.status == 0:
        auction.status = 1
        auction.save()
        
    # currentPlayer = CurruntPlayer.objects.all().last()
    # playerData = Player.objects.get(id=currentPlayer.player)
    
    # print(auction)
    return render(request, 'live_auction.html', {"auction":auction, 'teams':teams})
    # except Exception as e:
    #     return render(request, "error.html", {"Error":e, "code":404})

def auctionDone(request, auctionid):
    auction = Auction.objects.get(id=auctionid)
    players = AuctionPlayer.objects.filter(auction__id=auction.id)
    # players = 
    teams = Auction_teams.objects.filter(auction=auction).select_related('team')
    # print(teams)
    
    return render(request, 'auctiondone.html',{'auction':auction, 'players':players, 'teams':teams})

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
        return render(request, "error.html", {'Error':"Unauthorized User Access ", "code":"403"})

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
        return render(request, "error.html", {'Error':"Unauthorized User Access ", "code":"403"})
def auction_admin(request):
    print(request.session.get("user"))
    if request.session.get('user') and request.session.get("user") == 1:
        return render(request, 'auction_admin.html', {})
    else:
        return render(request, "error.html", {'Error':"Unauthorized User Access ", "code":"403"})


def player_summery(request, auctionid ,detail):
    try:
        players = ''
        filterVal = ''
        auction = Auction.objects.get(id=auctionid)
        if detail == 'unsold':
            players = auction.auctionplayer_set.filter(status=2)
        elif detail == 'sold':
            players = auction.auctionplayer_set.filter(status=1)
        elif detail == 'teams':
            teams = auction.team.all()
        else:
            players = auction.auctionplayer_set.all()
            
            
        lis = []
        if players != '' :
            for player in players:
                p = Player.objects.get(id=player.id)
                p.status = player.status
                lis.append(p) 
        else:
            for team in teams:
                p = Team.objects.get(id=team.id)
                lis.append(p) 

        return render(request, 'player_summery.html', {'players':lis, 'user':'team'})    
    except Exception as e:
        return render(request, "error.html", {'Error':e, "code":"403"})    

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
        return render(request, "error.html", {'Error':"Unauthorized User Access", "code":"403"})
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
            return render(request, 'error.html', {"Error":e, "code":"403"})
        
        
        return HttpResponseRedirect('auctionadmin/login')
    else:
        return render(request, 'adminReg.html', {})

def adminHome(request):

    if request.session.get('user') and request.session.get("user") == 1:

        admin = AuctionAdmin.objects.get(adminid = request.session['id'])
        auctions = Auction.objects.filter(adminId = admin.id)
        return render(request,'admin_home.html',{'auctions':auctions})

    else:
        return render(request, "error.html", {'Error':"Unauthorized User Access ", "code":"403"})

def getForm(request):
    return render(request, "forms/createauction.html",{})

def addPlayer(request):
    if request.session.get('user') and request.session.get("user") == 1:
        if request.method == "POST":
            try:
                playerId = request.POST.get('playerId')
                player = Player.objects.get(playerId=playerId)
            except Exception as e:
                return render(request, "error.html", {"Error":"Invalid Operation", "code":"400"})
    else:
        return render(request, "error.html", {'Error':"Unauthorized User Access ", "code":"403"})
    players = Player.objects.all()
    return render(request, "forms/addplayer.html", {'playerlist':players})

def addTeam(request):
    if request.session.get('user') and request.session.get("user") == 1:
        if request.method == "POST":
            try:
                admin = AuctionAdmin.objects.get(adminid=request.session.get("id")) 
                teamId = request.POST.get("teamId")

                team = Team.objects.get(teamId=teamId)

                auctionid = request.POST.get("auctionid")
                auction = Auction.objects.get(id=auctionid)

                auctionTeam = Auction_teams()
                auctionTeam.auctionId = auction
                auctionTeam.teamId = team
                auctionTeam.save()

            except IntegrityError as e:
                return render(request, "error.html", {"Error":"TEam Already Exists", "code":"400"})
                # return render(request, "error.html", {"Error":e})
       
            except Exception as e:
                return render(request, "error.html", {"Error":e, "code":"404"})
                # return render(request, "error.html", {"Error":e})
        # auctions = Auction.objects.filter(adminId=request.session.get('id'))
        # teams = Auction_teams.objects.select_related('teamId')
        admin = AuctionAdmin.objects.get(id=request.session.get("id")) 
        auctions = admin.auction_set.all()


        return render(request, "forms/addteam.html", {'auctions':auctions})
        # return render(request, "forms/addteam.html", {'auctions':auctions})
    else:
        return render(request, "error.html", {'Error':"Unauthorized User Access", "code":"403"})
    
    return render(request, "forms/addTeam.html",{})
    # return HttpResponseRedirect('getform?form=addteam')

def allAuctions(request):
    auctions = Auction.objects.all()

    return render(request, "auctions.html", {'auctions':auctions})

