from django import forms
from django.forms import Textarea

from django.contrib.auth.models import User

from .models import Status
from contests.models import Contest
# from users.models import UserProfile


class StatusForm(forms.ModelForm):

    class Meta:
        model = Status
        fields = ['summary']
        widgets = {
            'summary': Textarea(attrs={'cols': 50, 'rows': 5})
        }
        labels = {
            'summary': 'Summary'
        }

    def __init__(self, contest_id, user_id, *args, **kwargs):
        super(StatusForm, self).__init__(*args, **kwargs)
        self.fields['summary'] = forms.CharField(required=True)
        cts = Contest.objects.get(id=contest_id)
        user = User.objects.get(id=user_id)
        STATUS_OF_AC = [
            ('1', 'Solved'),
            ('2', 'Upsolved'),
            ('3', 'Not Solved'),
        ]
        for i in range(0, cts.num_of_problem):
            self.fields['p' + str(i)] = forms.ChoiceField(
                label='Problem ' + chr(ord('A') + i),
                choices=STATUS_OF_AC
            )
            self.initial['p' + str(i)] = '3'
            CONTRIBUTOR_FIELD = [
                ('1', user.userprofile.team_member_1),
                ('2', user.userprofile.team_member_2),
                ('4', user.userprofile.team_member_3),
            ]
            self.fields['c' + str(i)] = forms.MultipleChoiceField(
                label='Contributor',
                choices=CONTRIBUTOR_FIELD,
                widget=forms.CheckboxSelectMultiple(),
                required=False
            )
            self.initial['c' + str(i)] = []
