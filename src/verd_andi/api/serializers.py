from rest_framework import serializers
from survey.models import (
                           Item,
                           ItemObserver,
                           Observation,
                           ItemCommentary,
                           Characteristic,
                           ObservedCharacteristic,
                           ObservationPicture
                           )


class ObservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Observation
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'


class ItemObserverSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemObserver
        fields = '__all__'


class ItemCommentarySerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemCommentary
        fields = '__all__'


class AdaptiveObservationSerializer(serializers.ModelSerializer):

    observation_id = serializers.IntegerField(source="id")
    nr_konnunar = serializers.SerializerMethodField()
    itemcode_i_konnun = serializers.PrimaryKeyRelatedField(source="item.code",
                                                           read_only=True)
    status_obs = serializers.CharField(source="flag")
    shopid = serializers.CharField(source="shop_identifier")
    obs_price = serializers.DecimalField(source="observed_price",
                                         decimal_places=2,
                                         max_digits=25)
    obs_quantity = serializers.DecimalField(source="observed_quantity",
                                            decimal_places=2,
                                            max_digits=25)
    discount_flag = serializers.CharField(source="discount")
    month = serializers.SerializerMethodField()
    representative = serializers.SerializerMethodField()
    obs_comments = serializers.CharField(source="obs_comment")

    brand = serializers.SerializerMethodField()
    barcode = serializers.CharField()
    observer = serializers.PrimaryKeyRelatedField(source="observer.username",
                                                  read_only=True)
    observation_pictures = serializers.SerializerMethodField()

    def get_nr_konnunar(self, obj):
        return '{}{}'.format(obj.survey.code, obj.survey.year)

    def get_month(self, obj):
        return '{}'.format(str(obj.obs_time).split('-')[1])

    def get_representative(self, obj):

        try:
            rep = obj.item.itemcommentary.representativity
        except ItemCommentary.DoesNotExist:
            rep = True

        return rep

    def get_brand(self, obj):

        try:
            obs_chars = ObservedCharacteristic.objects.filter(observation=obj)
            for obs_char in obs_chars:
                char = Characteristic.objects.get(
                    id=obs_char.characteristic.id)
                if(char.name == "Brand"):
                    brand = obs_char.value
                    return brand

            brand = None
        except ObservedCharacteristic.DoesNotExist:
            brand = None

        return brand

    def get_observation_pictures(self, obj):

        try:
            obs_pics = ObservationPicture.objects.filter(observation=obj)
            pics = []
            for obs_pic in obs_pics:
                pics.append(obs_pic.picture.url)
        except ObservationPicture.DoesNotExist:
            pics = []

        return pics

    class Meta:
        model = Observation
        fields = (
            "observation_id",
            "nr_konnunar",
            "itemcode_i_konnun",
            "status_obs",
            "shop_type",
            "shopid",
            "obs_price",
            "obs_quantity",
            "discount_flag",
            "month",
            "representative",
            "obs_comments",
            "brand",
            "observer",
            "barcode",
            "observation_pictures"
            )
