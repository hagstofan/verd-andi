from django.contrib import admin
import nested_admin

from django.contrib.auth.models import User
# Register your models here.
from .models import Observation, Item, UserObservation, Characteristic, Survey


# class UserInline(nested_admin.NestedTabularInline):
# 	model = UserObservation
# 	max_num = 1

# class ObservationInline(nested_admin.NestedTabularInline):
# 	model = Observation
# 	# extra = 3
# 	inlines = [UserInline,]

# class ItemAdmin(nested_admin.NestedModelAdmin):
# 	inlines = [ObservationInline,]
	


# admin.site.register(Item, ItemAdmin)

class ObservationInline(nested_admin.NestedTabularInline):
	model = Observation
	extra = 3

class CharacteristicInline(nested_admin.NestedTabularInline):
	model = Characteristic
	extra = 3

class ItemAdmin(nested_admin.NestedModelAdmin):
	inlines = [CharacteristicInline, ObservationInline,]
	exclude = ('characteristics',)


class ObservationAdmin(nested_admin.NestedModelAdmin):
	model = Observation


class SurveyAdmin(nested_admin.NestedModelAdmin):
	model = Survey

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Observation, ObservationAdmin)
