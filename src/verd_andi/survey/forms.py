# forms.py for survey app
from django import forms
from .models import Item, Characteristic

from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError
from decimal import Decimal

# some validators.
def validate_observed_quantity(value):
	print("monkeys")
	#print(value)
	return value


class ObservationForm(forms.Form):
	CHOICES = (
        ('1', '1 Department store'),
        ('2', '2 Hypermarkets, supermarkets'),
        ('3', '3 Discount stores'),
        ('4', '4 Convenience stores, ect.'),
        ('5', '5 Specialized shop chains'),
        ('6', '6 Specialized shops'),
        ('7', '7 Markets'),
        ('8','8 Private service providers'),
        ('9', '9 Public and semi public service providers'),
        ('10','10 Mail order, Internet'),
        ('11', '11 Other kinds of outlets'),
        ('12', '12 Black Market'),
        ('99', '99 CPI data'),
    )
	DISCOUNTCHOICES = (
		('N', '  N  '),
		('R', '  R  '),
		('Q', '  Q  '),
		('T', '  T  '),
	)
	discount = forms.ChoiceField(choices=DISCOUNTCHOICES, initial='N')
	shop_type = forms.ChoiceField(choices=CHOICES)
	shop_identifier = forms.CharField()
	#flag = forms.CharField(max_length=4)
	
	value = forms.DecimalField(decimal_places=4, max_digits=25) # later should validate within min max
	observed_quantity = forms.DecimalField(decimal_places=4, max_digits=25)
	#item = forms.ForeignKey(Item)
	#observer = forms.ForeignKey(User, blank=True, related_name='survey_observer', null=True)
	obs_comment = forms.CharField(max_length=300, required=False)
	#specified_characteristics = forms.CharField(max_length=400, blank=True)
	#survey = forms.ForeignKey(Survey)

	def __init__(self, *args, **kwargs):
		#self.extra = extra = kwargs.pop('extra') # for validation of extra
		extra = kwargs.pop('extra')
		self.max_quantity = kwargs.pop('max_quantity') # for validation
		self.min_quantity = kwargs.pop('min_quantity') # for validation
		#print(self.max_quantity)
		super(ObservationForm, self).__init__(*args, **kwargs)

		if "initial" in kwargs:
			initial = kwargs.pop('initial')
		else:
			initial = {}

		for i, question in enumerate(extra):
			if question in initial:
				self.fields['custom_%s' % i] = forms.CharField(label=question, initial=initial[question])
			else:
				self.fields['custom_%s' % i] = forms.CharField(label=question)




	def extra_answers(self):
		for name, value in self.cleaned_data.items():
			if name.startswith('custom_'):
				yield (self.fields[name].label, value)


	def clean_observed_quantity(self):
		observed_quantity = self.cleaned_data['observed_quantity']
		if self.max_quantity:
			if(observed_quantity > Decimal(self.max_quantity)):
				raise forms.ValidationError("quantity exceeds maximum quantity.")
		if self.min_quantity:
			if(observed_quantity < Decimal(self.min_quantity)):
				raise forms.ValidationError("quantity is below minimum quantity.")
		
		return observed_quantity







class ItemCommentaryForm(forms.Form):
	seasonality = forms.BooleanField(required=False)
	representativity = forms.BooleanField(required=False)
	comment = forms.CharField(max_length=300,required=False)
	vat = forms.DecimalField(decimal_places=4, max_digits=4,required=False)
