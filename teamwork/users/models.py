from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class UserProfile(models.Model):
	user = models.OneToOneField(
			User, 
			on_delete=models.CASCADE,
		)
	team_name = models.CharField(max_length = 200)
	team_member_1 = models.CharField(max_length = 200)
	team_member_2 = models.CharField(max_length = 200)
	team_member_3 = models.CharField(max_length = 200)
	team_description = models.TextField()
	history = HistoricalRecords()

	def __unicode__(self):
		return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile()
        profile.user = instance
        profile.save()
