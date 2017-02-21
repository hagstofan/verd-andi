from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User

import datetime
from django.utils import timezone


# Create your models here.

@python_2_unicode_compatible
class Item(models.Model):
	code = models.CharField(max_length=20, primary_key=True)
	label = models.CharField(max_length=200)
	unit = models.CharField(max_length=100)

	def __str__(self):
		return self.label


@python_2_unicode_compatible
class Observation(models.Model):
	obeservation_number = models.IntegerField(blank=True)
	obs_time = models.DateTimeField()
	shop_type = models.IntegerField()
	shop_identifier = models.CharField(max_length=200)
	flag = models.CharField(max_length=4)
	discount = models.CharField(max_length=4)
	value = models.DecimalField(decimal_places=4, max_digits=25)
	brand = models.CharField(max_length=200)
	observed_quantity = models.DecimalField(decimal_places=4, max_digits=25)
	item = models.ForeignKey(Item)
	observer = models.ForeignKey(User, blank=True, related_name='observer', null=True)

	def __str__(self):
		return str(self.item) + " " + str(obs_time)



