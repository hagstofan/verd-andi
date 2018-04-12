from rest_framework import serializers
from survey.models import Item, ItemObserver, Observation


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
