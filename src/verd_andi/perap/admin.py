from django.contrib import admin
import nested_admin

from django.contrib.auth.models import User
# Register your models here.
from .models import Observation, Item, UserObservation


class UserInline(nested_admin.NestedTabularInline):
	model = UserObservation
	max_num = 1

class ObservationInline(nested_admin.NestedTabularInline):
	model = Observation
	extra = 3
	inlines = [UserInline,]

class ItemAdmin(nested_admin.NestedModelAdmin):
	inlines = [ObservationInline,]
	


admin.site.register(Item, ItemAdmin)
