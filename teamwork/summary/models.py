from django.db import models

from users.models import UserProfile
from contests.models import Contest

class Status(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete = models.CASCADE)
    summary = models.TextField()
    ac_status = models.BigIntegerField()
    contributor = models.BigIntegerField()
    