from django.db import models

from users.models import UserProfile
from contests.models import Contest
from simple_history.models import HistoricalRecords


class Status(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    summary = models.TextField()
    ac_status = models.BigIntegerField(default=0, null=True, blank=True)
    contributor = models.BigIntegerField(default=0, null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = 'statuses'

    def __str__(self):
        return self.summary
