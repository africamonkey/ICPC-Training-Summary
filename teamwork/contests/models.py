from django.db import models

class Contest(models.Model):
	cid = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 200)
	date = models.DateTimeField()
	NUM_OF_PROBLEM = (
		('5 - E', 5),
		('6 - F', 6),
		('7 - G', 7),
		('8 - H', 8),
		('9 - I', 9),
		('10 - J', 10),
		('11 - K', 11),
		('12 - L', 12),
		('13 - M', 13),
	)
	num_of_problem = models.IntegerField(
		choices = NUM_OF_PROBLEM,
		default = '5 - E',
	)

	def __str__(self):
		return str(cid) + ' ' + self.name
