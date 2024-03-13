from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html', {})

def login(request):
    return render(request, 'login.html', {})

def register(request):
    return render(request, 'register.html', {})

def player_register(request):
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

    