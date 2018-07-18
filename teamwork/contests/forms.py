from bootstrap_datepicker_plus.widgets import DatePickerInput
from django import forms

from .models import Contest

class ContestForm(forms.ModelForm):
	class Meta:
		model = Contest
		fields = ['name', 'source', 'date', 'num_of_problem', 'contest_type', 'contest_link']
		widgets = {
			'date': DatePickerInput(
				options={
					"format": "yyyy/mm/dd",
					"autoclose": True
				}
			)
		}
		labels = {
			'name': 'Contest Name',
			'source': 'Contest Source',
			'date': 'Contest Start Time',
			'num_of_problem': 'Number of Problems',
			'contest_link': 'Link',
		}

	def __init__(self, *args, **kwargs):
		super(ContestForm, self).__init__(*args, **kwargs)
		self.fields['date'] = forms.DateField(input_formats=['%Y/%m/%d'], widget=DatePicker(
			options={
				"format": "yyyy/mm/dd",
				"autoclose": True
			}
		))
