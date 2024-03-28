from django.urls import path
from . import views

urlpatterns = [
    path('auctionadmin', views.auction_admin, name='auction_admin'),
    path('adminhome',views.adminHome, name='adminhome'),
    path('addplayer',views.addPlayer, name='addplayer'),
    path('addteam',views.addTeam, name='addteam'),
    path('adminreg',views.adminReg, name='adminreg'),
    path('createauction', views.create_auction, name='create_auction'),
    path('getform',views.getForm, name='getform')

]