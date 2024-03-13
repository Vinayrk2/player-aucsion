from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('playerregister', views.player_register, name='player_register'),
    path('liveauction', views.live_auction, name='live_auction'),
    path('oldauction', views.old_auction, name='old_auction'),
    path('playerprofile', views.player_profile, name='player_profile'),
    path('createauction', views.create_auction, name='create_auction'),
    path('auctionadmin', views.auction_admin, name='auction_admin'),
]