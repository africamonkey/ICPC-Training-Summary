from django.forms import ModelForm, Textarea
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class TeamForm(ModelForm):
	class Meta:
		model = UserProfile
		fields = (
			'team_name', 
			'team_member_1', 
			'team_member_2', 
			'team_member_3',
			'team_description',
		)
		widgets = {
			'team_description':Textarea(attrs={'rows':5})
		}
		labels = {
			'team_name': 'Team Name',
			'team_member_1': 'Team Member 1',
			'team_member_2': 'Team Member 2',
			'team_member 3': 'Team Member 3',
			'team_description': 'Team Description',
		}

