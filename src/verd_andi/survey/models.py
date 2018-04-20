from __future__ import unicode_literals
import uuid
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User

import datetime


YEAR_CHOICES = []
for r in range(1980, (datetime.datetime.now().year+1)):
    YEAR_CHOICES.append((r, r))


def create_uuid():
    return uuid.uuid4()


@python_2_unicode_compatible
class Survey(models.Model):
    code = models.CharField(max_length=100)
    year = models.IntegerField(max_length=4,
                               choices=YEAR_CHOICES,
                               default=datetime.datetime.now().year)
    dataflowID = models.CharField(max_length=100)
    current = models.BooleanField()
    default_vat = models.DecimalField(decimal_places=4, max_digits=4, default=0.24)

    class Meta:
        unique_together = (("code", "year"),)

    def __str__(self):
        return self.code+"-"+str(self.year)


@python_2_unicode_compatible
class Item(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    label = models.CharField(max_length=200)
    unit = models.CharField(max_length=100)
    survey = models.ForeignKey(Survey)
    picture = models.ImageField(upload_to="item_pic_uploads" +
                                "/"+str(create_uuid()),
                                blank=True,
                                null=True)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return self.label + "-" + self.code


@python_2_unicode_compatible
class ItemCommentary(models.Model):
    item = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    seasonality = models.BooleanField(default=False)
    representativity = models.BooleanField(default=True)
    comment = models.CharField(max_length=300, blank=True, default="")
    vat = models.DecimalField(decimal_places=4, max_digits=4, default=0.24)

    def __str__(self):
        return str(self.item.label)


@python_2_unicode_compatible
class Characteristic(models.Model):
    name = models.CharField(max_length=200)
    enName = models.CharField(max_length=200)
    char_type = models.IntegerField()  # this field is called type in the xml
    isProperty = models.BooleanField(default=False)
    specify = models.BooleanField(default=False)
    item = models.ForeignKey(Item)
    value = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Observation(models.Model):
    obeservation_number = models.IntegerField(blank=True, null=True)
    obs_time = models.DateField()
    shop_type = models.IntegerField()
    shop_identifier = models.CharField(max_length=200)
    flag = models.CharField(max_length=4, choices=[('E', 'E'), ('O', 'O')])
    discount = models.CharField(max_length=4,
                                choices=[('N', 'N'),
                                         ('R', 'R'),
                                         ('Q', 'Q'),
                                         ('T', 'T')])
    observed_price = models.DecimalField(decimal_places=1, max_digits=25)
    observed_quantity = models.DecimalField(decimal_places=1, max_digits=25)
    item = models.ForeignKey(Item)
    observer = models.ForeignKey(User,
                                 blank=True,
                                 related_name='survey_observer',
                                 null=True)
    obs_comment = models.CharField(max_length=300, blank=True)
    specified_characteristics = models.CharField(max_length=400, blank=True)
    survey = models.ForeignKey(Survey)
    shop_own_brand = models.BooleanField(default=False)

    def __str__(self):
        return str(self.item) + " " + str(self.obs_time)


@python_2_unicode_compatible
class ObservedCharacteristic(models.Model):
    observation = models.ForeignKey(Observation, on_delete=models.CASCADE)
    characteristic = models.ForeignKey(
        Characteristic,
        on_delete=models.CASCADE,
        # limit_choices_to =
        # Characteristic.objects.filter(item = self.observation.item)
        )  # characteristic here intended to be
    # limited to  the characteristiics of
    # the item that the observation refers to
    value = models.CharField(max_length=200, default="")

    def __str__(self):
        return str(self.characteristic)


@python_2_unicode_compatible
class UserObservation(models.Model):
    observation = models.ForeignKey(Observation)
    user = models.ForeignKey(User, related_name='survey_user')

    def __str__(self):
        return str(self.user)


@python_2_unicode_compatible
class ItemObserver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.item) + '--' + str(self.user)


@python_2_unicode_compatible
class Observer(User):
    class Meta:
        proxy = True

    def __str__(self):
        return self.username
