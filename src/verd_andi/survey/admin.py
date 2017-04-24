from django.contrib import admin
import nested_admin

from django.contrib.auth.models import User
# Register your models here.
from .models import Observation, Item, UserObservation, Characteristic, Survey, ObservedCharacteristic, ItemObserver, Observer


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

class ObservedCharacteristicInline(nested_admin.NestedTabularInline):
	model = ObservedCharacteristic
	#form = ObservedCharacteristicForm


class ObservationInline(nested_admin.NestedTabularInline):
	model = Observation
	extra = 3
	inlines = [ObservedCharacteristicInline,]

class CharacteristicInline(nested_admin.NestedTabularInline):
	model = Characteristic
	extra = 3

class ItemAdmin(nested_admin.NestedModelAdmin):
	inlines = [CharacteristicInline, ObservationInline,]
	exclude = ('characteristics',)
	search_fields = ['code','label']	
	list_filter = (
        ('survey', admin.RelatedOnlyFieldListFilter),
    )


class ObservationAdmin(nested_admin.NestedModelAdmin):
	model = Observation
	inlines = [ObservedCharacteristicInline,]


class SurveyAdmin(nested_admin.NestedModelAdmin):
	model = Survey

class ObserverAdmin(nested_admin.NestedModelAdmin):
	model = ItemObserver 
	search_fields = ['item',]
	raw_id_fields = ('item',)
	list_filter = (
		('user', admin.RelatedOnlyFieldListFilter),
		)

class ItemObserverInline(nested_admin.NestedTabularInline):
	model = ItemObserver
	raw_id_fields = ('item',)
	extra = 3


class UserObserverAdmin(nested_admin.NestedModelAdmin):
	model = Observer

	inlines = [ItemObserverInline,]
	exclude = ('item',)

class CharacteristicAdmin(nested_admin.NestedModelAdmin):
	model = Characteristic
	search_fields = ['id',]
	inlines = [ObservedCharacteristicInline,]

class ObservedCharacteristicAdmin(nested_admin.NestedModelAdmin):
	model = ObservedCharacteristic

admin.site.register(Survey, SurveyAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Observation, ObservationAdmin)
admin.site.register(ItemObserver, ObserverAdmin)
admin.site.register(Observer, UserObserverAdmin)
admin.site.register(Characteristic, CharacteristicAdmin)
admin.site.register(ObservedCharacteristic, ObservedCharacteristicAdmin)