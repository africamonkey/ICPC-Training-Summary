from django import forms

from .models import Status
from users.models import UserProfile

class StatusForm(forms.Form):
    summary = forms.CharField(min_length = 50)

    def __init__(self,profile, *args, **kwargs):
        STATUS_OF_AC = (
		    ('0', 'Solved'),
		    ('1', 'Upsolved'),
		    ('2', 'Not Solved'),
	    )
        for i in range(0,num_of_problem):
            CONTRIBUTOR_OF_PROBLEM = [
                ()
            ]
            self.fields['p'+str(i)] = forms.ChoiceField(choices = STATUS_OF_AC)
            self.initial['p'+str(i)] = '2'
        super(StatusForm, self).__init__(args,kwargs)
        