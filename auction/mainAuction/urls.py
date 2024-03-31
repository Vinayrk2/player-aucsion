from django.urls import path
from . import views

websocket_urlpatterns = [
    path('', views.auctionStart, name='auctionstart'),
    path('auction/<auctionid>', views.dashboard, name="dashboard"),
    path('startauction', views.startauction, name="startauction"),
]