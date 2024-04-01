from django.shortcuts import render
from django.http import HttpResponse
from appdata.models import Auction

# Create your views here.
def auctionStart(request):
    return HttpResponse(content="Connection")

def dashboard(request, auctionid):

    return render(request, "live_auction.html", {})

def startauction(request, dashboard):
    if(request.session.get("user") and request.session.get("user") == 1):
        auctionid = int(request.POST.get("auctionid"))
        auction = Auction.objects.get(auctionId=auctionid)
        auction.status = 1
        return render(request, "live_auction.html", {})
    else:
        return HttpResponseRedirect('auctionadmin')

