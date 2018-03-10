from django import forms

from .models import Contest

class ContestForm(forms.ModelForm):
	class Meta:
		model = Contest
		fields = ['name', 'source', 'date', 'num_of_problem']
		labels = {'name': 'Contest Name',
			'source': 'Contest Source',
			'date': 'Contest Start Time',
			'num_of_problem': 'Number of Problems',
		}
