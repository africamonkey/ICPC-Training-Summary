from django import forms

from django.contrib.auth.models import User

from .models import Status
from contests.models import Contest
from users.models import UserProfile

class StatusForm(forms.Form):

    def __init__(self, contest_id, *args, **kwargs):
        super(StatusForm, self).__init__(*args, **kwargs)
        self.fields['summary'] = forms.CharField(required=True)
        cts = Contest.objects.get(id = contest_id)
        STATUS_OF_AC = [
		    ('1', 'Solved'),
		    ('2', 'Upsolved'),
		    ('3', 'Not Solved'),
	    ]
        for i in range(0, cts.num_of_problem):
            self.fields['p'+str(i)] = forms.ChoiceField(choices = STATUS_OF_AC)
            self.initial['p'+str(i)] = '3'
        