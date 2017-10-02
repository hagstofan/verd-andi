"""
Output1.py
"""
from django.core import serializers
from xml.dom import minidom

import sqlite3, csv

import sys
from os import path
from verd_andi import settings
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from survey.models import Item 


connection = sqlite3.connect("../db.sqlite3")
cursor =connection.cursor()



#data = serializers.serialize("xml", Item.objects.all())

#print(str(data))
print('bla')
