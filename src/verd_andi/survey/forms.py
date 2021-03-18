# forms.py for survey app
from django import forms
from decimal import Decimal
from collections import OrderedDict

from multiupload.fields import MultiFileField


class ObservationForm(forms.Form):
    CHOICES = (
        ('1', '1 Department store'),
        ('2', '2 Hypermarkets, supermarkets'),
        ('3', '3 Discount stores'),
        ('4', '4 Convenience stores, ect.'),
        ('5', '5 Specialized shop chains'),
        ('6', '6 Specialized shops'),
        ('7', '7 Markets'),
        ('8', '8 Private service providers'),
        ('9', '9 Public and semi public service providers'),
        ('10', '10 Mail order, Internet'),
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

    observed_price = forms.DecimalField(decimal_places=2, max_digits=25)
    observed_quantity = forms.DecimalField(decimal_places=2, max_digits=25)
    barcode = forms.CharField(max_length=200, required=False)
    obs_comment = forms.CharField(max_length=300, required=False)

    shop_own_brand = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):

        extra = kwargs.pop('extra')  # for validation of extra
        self.max_quantity = kwargs.pop('max_quantity')  # for validation
        self.min_quantity = kwargs.pop('min_quantity')  # for validation

        super(ObservationForm, self).__init__(*args, **kwargs)

        if "initial" in kwargs:
            initial = kwargs.pop('initial')
            self.update = True
        else:
            initial = {}

        self.field_order = [
            'discount',
            'shop_type',
            'shop_identifier',
            'observed_price',
            'observed_quantity',
            'barcode'
            ]

        for i, question in enumerate(extra):
            if question in initial:
                self.fields['custom_%s' % i] = forms\
                    .CharField(label=question, initial=initial[question])
            else:
                self.fields['custom_%s' % i] = forms.CharField(label=question)

            self.field_order.append('custom_%s' % i)

        self.field_order.append('obs_comment')
        self.field_order.append('shop_own_brand')

        fields = OrderedDict()
        for key in self.field_order:
            fields[key] = self.fields.pop(key)

        self.fields = fields

    def extra_answers(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('custom_'):
                yield (self.fields[name].label, value)

    def clean_observed_quantity(self):
        observed_quantity = self.cleaned_data['observed_quantity']
        if self.max_quantity:
            if(observed_quantity > Decimal(self.max_quantity)):
                raise forms\
                      .ValidationError("quantity exceeds maximum quantity.")
        if self.min_quantity:
            if(observed_quantity < Decimal(self.min_quantity)):
                raise forms\
                      .ValidationError("quantity is below minimum quantity.")

        return observed_quantity


class UploadForm(forms.Form):
    pictures = MultiFileField(min_num=1, max_num=3, max_file_size=1024*1024*5)


class ItemCommentaryForm(forms.Form):
    seasonality = forms.BooleanField(required=False)
    representativity = forms.BooleanField(required=False)
    comment = forms.CharField(max_length=300, required=False)
    vat = forms.DecimalField(decimal_places=4, max_digits=4, required=False)


class CollectorCommentForm(forms.Form):
    comment = forms.CharField(max_length=500)


class SurveyAddItemsActionForm(forms.Form):
    file = forms.FileField()
