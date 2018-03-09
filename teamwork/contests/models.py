from django.db import models

class Contest(models.Model):
	name = models.CharField(max_length = 200)
	source = models.CharField(max_length = 200)
	date = models.DateTimeField()
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

	def __str__(self):
		return self.name

