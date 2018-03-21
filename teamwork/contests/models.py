from django.db import models
from simple_history.models import HistoricalRecords

class Contest(models.Model):
	name = models.CharField(max_length = 200)
	source = models.CharField(max_length = 200)
	date = models.DateField()
	NUM_OF_PROBLEM = (
		(5, '5 - E'),
		(6, '6 - F'),
		(7, '7 - G'),
		(8, '8 - H'),
		(9, '9 - I'),
		(10, '10 - J'),
		(11, '11 - K'),
		(12, '12 - L'),
		(13, '13 - M'),
	)
	num_of_problem = models.IntegerField(
		choices = NUM_OF_PROBLEM,
		default = 5,
	)

	CONTEST_TYPE = (
		('Online', 'Online Practice Contest (Virtual Contest)'),
		('Onsite', 'Onsite Official Contest (ICPC / CCPC / GDCPC)'),
	)
	contest_type = models.CharField(
		choices = CONTEST_TYPE,
		default = 'Online',
		max_length = 6,
	)

	contest_link = models.CharField(max_length = 200)
	history = HistoricalRecords()

	def __str__(self):
		return self.name

