from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from survey.models import Item
from .serializers import ItemSerializer

# Create your views here.

class ItemList(APIView):
	
	def get(self, request):
		Items = Item.objects.all()
		print("blaaaaa")
		serializer = ItemSerializer(Items, many=True)
		return Response(serializer.data)


	def post(self):
		pass




 

