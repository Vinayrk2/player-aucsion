from django.contrib import admin
from appdata.models import Auction, Login, AuctionAdmin, Player, AuctionPlayer, Team, Auction_teams, CurruntPlayer

admin.site.register(Auction)
admin.site.register(AuctionAdmin)
admin.site.register(AuctionPlayer)
admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Login)
admin.site.register(Auction_teams)
admin.site.register(CurruntPlayer)

# Register your models here.
