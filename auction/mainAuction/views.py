from django.shortcuts import render
from django.http import HttpResponse
from appdata.models import Auction

# Create your views here.
def auctionStart(request):
    return HttpResponse(content="Connection")

def dashboard(request, auctionid):
    return render(request, "live_auction.html", {})


