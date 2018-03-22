from django.forms import ModelForm
from markdownx.fields import MarkdownxFormField
from .models import UserProfile

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
		labels = {
			'team_name': 'Team Name',
			'team_member_1': 'Team Member 1',
			'team_member_2': 'Team Member 2',
			'team_member_3': 'Team Member 3',
			'team_description': 'Team Description',
		}

	def __init__(self, *args, **kwargs):
		super(TeamForm, self).__init__(*args, **kwargs)
		self.fields['team_description'] = MarkdownxFormField()
		self.fields['team_description'].label = 'Team Description'

