# forms.py for survey app
from django import forms
from .models import Item, Characteristic

from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User


class ObservationForm(forms.Form):
	shop_type = forms.IntegerField()
	shop_identifier = forms.CharField()
	flag = forms.CharField(max_length=4)
	discount = forms.CharField(max_length=4)
	value = forms.DecimalField(decimal_places=4, max_digits=25)
	brand = forms.CharField(max_length=200)
	observed_quantity = forms.DecimalField(decimal_places=4, max_digits=25)
	#item = forms.ForeignKey(Item)
	#observer = forms.ForeignKey(User, blank=True, related_name='survey_observer', null=True)
	obs_comment = forms.CharField(max_length=300)
	#specified_characteristics = forms.CharField(max_length=400, blank=True)
	#survey = forms.ForeignKey(Survey)


	# full_name = forms.CharField(required=False)
	# email = forms.EmailField()
	# message = forms.CharField()