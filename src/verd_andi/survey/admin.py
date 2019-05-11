from django.contrib import admin
import nested_admin
from .models import (
        Observation,
        Item,
        Characteristic,
        Survey,
        ObservedCharacteristic,
        ItemObserver,
        Observer,
        ItemCommentary
    )


class ObservedCharacteristicInline(nested_admin.NestedTabularInline):
    model = ObservedCharacteristic
    # form = ObservedCharacteristicForm


class ObservationInline(nested_admin.NestedTabularInline):
    model = Observation
    extra = 3
    inlines = [ObservedCharacteristicInline, ]


class CharacteristicInline(nested_admin.NestedTabularInline):
    model = Characteristic
    extra = 3


class ItemCommentaryInline(nested_admin.NestedTabularInline):
    model = ItemCommentary


class ItemAdmin(nested_admin.NestedModelAdmin):
    inlines = [CharacteristicInline, ItemCommentaryInline, ObservationInline, ]
    exclude = ('characteristics', )
    search_fields = ['code', 'label']
    list_filter = (
        ('survey', admin.RelatedOnlyFieldListFilter),
    )


class ObservationAdmin(nested_admin.NestedModelAdmin):
    model = Observation
    inlines = [ObservedCharacteristicInline, ]
    search_fields = ('item__code', 'item__label', 'obs_time')
    list_filter = (
        ('observer', admin.RelatedOnlyFieldListFilter),
        ('survey', admin.RelatedOnlyFieldListFilter),
        ('shop_type'),
        )
    list_display = ('item',
                    'obs_time',
                    'shop_type',
                    'shop_own_brand',
                    'observer',
                    'show_link',
                    'edit_link')

    def show_link(self, obj):
        # return '<a href=/survey/observation/%s/>Click here</a>' % obj.id
        return '<a href=/survey/observation-view/%s/>view</a>' % obj.id

    def edit_link(self, obj):
        return '<a href=/survey/observation/%s/>edit</a>' % obj.id

    show_link.allow_tags = True
    edit_link.allow_tags = True


class Observation4PriceComp(Observation):

    class Meta:
        proxy = True


class ObservationBeta(Observation):

    class Meta:
        proxy = True


class PriceComparisonAdmin(ObservationAdmin):
    def get_queryset(self, request):
        return self.model.objects.all()

    inlines = [ObservedCharacteristicInline, ]
    search_fields = ('item__code', 'item__label', 'obs_time')
    # list_filter = (
    #     ('observer', admin.RelatedOnlyFieldListFilter),
    #     ('survey', admin.RelatedOnlyFieldListFilter),
    #     ('shop_type'),
    #     )
    list_display = ('item',
                    'shop_identifier',
                    'observed_price',
                    'observed_quantity',
                    'obs_time',
                    'shop_own_brand',
                    'show_link',
                    'edit_link')

    def show_link(self, obj):
        # return '<a href=/survey/observation/%s/>Click here</a>' % obj.id
        return '<a href=/survey/observation-view/%s/>view</a>' % obj.id

    def edit_link(self, obj):
        return '<a href=/survey/observation/%s/>edit</a>' % obj.id

    show_link.allow_tags = True
    edit_link.allow_tags = True


class ObservationBetaAdmin(ObservationAdmin):

    def get_queryset(self, request):
        return self.model.objects.all()

    inlines = [ObservedCharacteristicInline, ]
    search_fields = ('item__code', 'item__label', 'obs_time')
    # list_filter = (
    #     ('observer', admin.RelatedOnlyFieldListFilter),
    #     ('survey', admin.RelatedOnlyFieldListFilter),
    #     ('shop_type'),
    #     )
    list_display = ('item_code',
                    'shop_type',
                    'shop_identifier',
                    'discount',
                    'observed_price',
                    'observed_quantity',
                    'obs_time',
                    'flag',
                    'show_link',
                    'edit_link')

    def show_link(self, obj):
        # return '<a href=/survey/observation/%s/>Click here</a>' % obj.id
        return '<a href=/survey/observation-view/%s/>view</a>' % obj.id

    def edit_link(self, obj):
        return '<a href=/survey/observation/%s/>edit</a>' % obj.id

    def item_code(self, obj):
        return obj.item.code

    show_link.allow_tags = True
    edit_link.allow_tags = True


class SurveyAdmin(nested_admin.NestedModelAdmin):
    model = Survey


class ObserverAdmin(nested_admin.NestedModelAdmin):
    model = ItemObserver
    search_fields = ['item', ]
    raw_id_fields = ('item', )
    list_filter = (
        ('user', admin.RelatedOnlyFieldListFilter),
        )


class ItemObserverInline(nested_admin.NestedTabularInline):
    model = ItemObserver
    raw_id_fields = ('item', )
    extra = 3


class UserObserverAdmin(nested_admin.NestedModelAdmin):
    model = Observer

    inlines = [ItemObserverInline, ]
    exclude = ('item', )


class CharacteristicAdmin(nested_admin.NestedModelAdmin):
    model = Characteristic
    search_fields = ['id', ]
    inlines = [ObservedCharacteristicInline, ]


class ObservedCharacteristicAdmin(nested_admin.NestedModelAdmin):
    model = ObservedCharacteristic


class ItemCommentaryAdmin(nested_admin.NestedModelAdmin):
    model = ItemCommentary

    list_filter = (
        ('vat'),
        ('seasonality'),
        ('representativity'),
        )
    list_display = ('item', 'vat', 'seasonality', 'representativity')


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Observation, ObservationAdmin)
admin.site.register(ItemObserver, ObserverAdmin)
admin.site.register(Observer, UserObserverAdmin)
admin.site.register(Characteristic, CharacteristicAdmin)
admin.site.register(ObservedCharacteristic, ObservedCharacteristicAdmin)
admin.site.register(ItemCommentary, ItemCommentaryAdmin)
admin.site.register(Observation4PriceComp, PriceComparisonAdmin)
admin.site.register(ObservationBeta, ObservationBetaAdmin)
