from django import forms

from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class TeamForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = [
			'team_name', 
			'team_member_1', 
			'team_member_2', 
			'team_member_3',
			'team_description',
		]
		labels = {
			'team_name': 'Team Name',
			'team_member_1': 'Team Member 1',
			'team_member_2': 'Team Member 2',
			'team_member 3': 'Team Member 3',
			'team_description': 'Team Description',
		}
