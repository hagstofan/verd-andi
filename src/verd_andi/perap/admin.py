from django.contrib import admin

# Register your models here.
from .models import Observation, Item


class ObservationInline(admin.TabularInline):
	model = Observation
	extra = 3

class ItemAdmin(admin.ModelAdmin):
	inlines = [ObservationInline,]
	


admin.site.register(Item, ItemAdmin)
