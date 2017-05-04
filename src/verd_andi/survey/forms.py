# forms.py for survey app
from django import forms
from .models import Item, Characteristic

from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User


class ObservationForm(forms.Form):
	#shop_type = forms.IntegerField()
	CHOICES = (
        ('1', 'Department store'),
        ('2', 'Hypermarkets, supermarkets'),
        ('3', 'Discount stores'),
        ('4', 'Convenience stores, ect.'),
        ('5', 'Specialized shop chains'),
        ('6', 'Specialized shops'),
        ('7', 'Markets'),
        ('8','Private service providers'),
        ('9', 'Public and semi public service providers'),
        ('10','Mail order, Internet'),
        ('11', 'Other kinds of outlets'),
        ('12', 'Black Market'),
        ('99', 'CPI data'),
    )
	shop_type = forms.ChoiceField(choices=CHOICES)
	shop_identifier = forms.CharField()
	#flag = forms.CharField(max_length=4)
	discount = forms.CharField(max_length=4)
	value = forms.DecimalField(decimal_places=4, max_digits=25)
	observed_quantity = forms.DecimalField(decimal_places=4, max_digits=25)
	#item = forms.ForeignKey(Item)
	#observer = forms.ForeignKey(User, blank=True, related_name='survey_observer', null=True)
	obs_comment = forms.CharField(max_length=300, required=False)
	#specified_characteristics = forms.CharField(max_length=400, blank=True)
	#survey = forms.ForeignKey(Survey)

	def __init__(self, *args, **kwargs):
		extra = kwargs.pop('extra')
		super(ObservationForm, self).__init__(*args, **kwargs)

		if "initial" in kwargs:
			initial = kwargs.pop('initial')
		else:
			initial = {}

		for i, question in enumerate(extra):
			if question in initial:
				print('its in')
				self.fields['custom_%s' % i] = forms.CharField(label=question, initial=initial[question])
			else:
				self.fields['custom_%s' % i] = forms.CharField(label=question)


	def extra_answers(self):
		for name, value in self.cleaned_data.items():
			if name.startswith('custom_'):
				yield (self.fields[name].label, value)



class ItemCommentaryForm(forms.Form):
	seasonality = forms.BooleanField(required=False)
	representativity = forms.BooleanField(required=False)
	comment = forms.CharField(max_length=300,required=False)
	vat = forms.DecimalField(decimal_places=4, max_digits=4,required=False)
	"""
	seasonality = models.BooleanField(default=False)
	representivity = models.BooleanField(default=True)
	comment = models.CharField(max_length=300, blank=True, default="")
	vat = models.DecimalField(decimal_places=4, max_digits=4, default=0.24)

	"""

	# full_name = forms.CharField(required=False)
	# email = forms.EmailField()
	# message = forms.CharField()