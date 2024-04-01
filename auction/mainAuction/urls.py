from django.urls import path
from . import views

websocket_urlpatterns = [
    path('', views.auctionStart, name='auctionstart'),
    path('liveauction/<auctionid>', views.dashboard, name="dashboard"),
]