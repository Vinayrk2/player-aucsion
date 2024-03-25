from django import forms
from appdata.models import Team, Player, AuctionAdmin

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team 
        fields = ['teamId','name','email','password','logo']
        exclude = ['captainId']

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = '__all__' 
        exclude = ['id']

class AdminForm(forms.ModelForm):
    class Meta:
        model = AuctionAdmin
        fields = '__all__'
