from django import forms
from appdata.models import Team, Player

class TeamForm(forms.ModelForm):
    logo = forms.ImageField(required=False)
    class Meta:
        model = Team 
        fields = ['teamId','name','email','password','logo']
        exclude = ['captainId']

class PlayerForm(forms.ModelForm):
    battingStyle = forms.CharField(required=False)
    bowlingStyle = forms.CharField(required=False)
    image = forms.CharField(required=False)
    class Meta:
        model = Player
        fields = '__all__' 
        exclude = ['id','captainId']