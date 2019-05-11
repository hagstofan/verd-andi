from rest_framework import serializers
from survey.models import Item, ItemObserver, Observation, ItemCommentary


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

    """
    item_code = serializers.PrimaryKeyRelatedField(
    #  source="item.code", read_only=True)
    shop_type = serializers.IntegerField(source='shop_type')
    shop_identifier = serializers.
    """
    # commentarys = ItemCommentary.objects.all()
    # itemcommentary = ItemCommentarySerializer(
    #   commentarys, many=True, read_only=True)
    #  nr_konnunar = serializers.PrimaryKeyRelatedField(
    #    source="survey.code", read_only=True)
    nr_konnunar = serializers.SerializerMethodField()
    itemcode_i_konnun = serializers.PrimaryKeyRelatedField(source="item.code",
                                                           read_only=True)
    status_obs = serializers.CharField(source="flag")
    shopid = serializers.CharField(source="shop_identifier")
    obs_price = serializers.DecimalField(source="observed_price",
                                         decimal_places=2,
                                         max_digits=8)
    obs_quantity = serializers.DecimalField(source="observed_quantity",
                                            decimal_places=2,
                                            max_digits=8)
    discount_flag = serializers.CharField(source="discount")
    # month
    month = serializers.SerializerMethodField()
    # month = serializers.DateField(source="obs_time")
    # representative = serializers.PrimaryKeyRelatedField(
    #   source="item.itemcommentary.representativity", read_only=True)
    representative = serializers.SerializerMethodField()
    # obs_comments = serializers.PrimaryKeyRelatedField(
    #  source="item.itemcommentary.comment", read_only=True)
    #  eda obs_comment ?
    obs_comments = serializers.CharField(source="obs_comment")

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

    class Meta:
        model = Observation
        fields = (
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
            "obs_comments"
            )
