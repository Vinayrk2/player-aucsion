from django.contrib import admin
from appdata.models import Auction, Login, AuctionAdmin, Player, AuctionPlayer, Team

admin.site.register(Auction)
admin.site.register(AuctionAdmin)
admin.site.register(AuctionPlayer)
admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Login)

# Register your models here.
