from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import UpdateAPIView, DestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAdminUser


from survey.models import Item, ItemObserver
from .serializers import ItemSerializer, ItemObserverSerializer

# Create your views here.

class ItemList(APIView):
	
	def get(self, request):
		Items = Item.objects.all()
		serializer = ItemSerializer(Items, many=True)
		return Response(serializer.data)


	def post(self):
		pass


class ItemObserverUpdateAPIView(UpdateAPIView):
	queryset = ItemObserver.objects.all()
	serializer_class = ItemObserverSerializer
	permission_classes = (IsAdminUser,)


class ItemObserverDestroyAPIView(DestroyAPIView):
	queryset = ItemObserver.objects.all()
	serializer_class = ItemObserverSerializer
	permission_classes = (IsAdminUser,)

class ItemObserverCreateAPIView(CreateAPIView):
	queryset = ItemObserver.objects.all()
	serializer_class = ItemObserverSerializer
	permission_classes = (IsAdminUser,)
 

