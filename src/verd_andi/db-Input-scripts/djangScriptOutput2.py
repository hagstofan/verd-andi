"""
newOutput.py .. outside django
"""

from xml.dom import minidom

import sqlite3, csv

import sys
from os import path

from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as etree

import django
django.setup()
from django.utils import timezone
import datetime
from survey.models import Survey, User, Item, ItemObserver, Characteristic, Observation, ObservedCharacteristic, ItemCommentary




# conn = sqlite3.connect("db.sqlite3")
# c =conn.cursor()

"""
important tables

survey_item
survey_characteristic
survey_observation
survey_observedcharacteristic

item
..observation
...observedcharacteristic  ...  characteristic

"""

"""
<CrossSectionalData xmlns="http://www.SDMX.org/resources/SDMXML/schemas/v2_0/message" xmlns:cgs="urn:sdmx:org.sdmx.infomodel.keyfamily.KeyFamily=ESTAT:PPP_CGS:cross" xmlns:cross="http://www.SDMX.org/resources/SDMXML/schemas/v2_0/cross" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.SDMX.org/resources/SDMXML/schemas/v2_0/message SDMXMessage.xsd urn:sdmx:org.sdmx.infomodel.keyfamily.KeyFamily=ESTAT:PPP_CGS:cross ESTAT_PPP_CGS_COUNTRY_Cross.xsd http://www.SDMX.org/resources/SDMXML/schemas/v2_0/cross SDMXCrossSectionalData.xsd">
"""

root=Element('CrossSectionalData')
tree=ElementTree(root)
#xmlns=Element('xmlns')
# root.append(xmlns)
# xmlns.text("http://www.SDMX.org/resources/SDMXML/schemas/v2_0/message")

root.set('xmlns','http://www.SDMX.org/resources/SDMXML/schemas/v2_0/message')
root.set('xmlns:cgs',"urn:sdmx:org.sdmx.infomodel.keyfamily.KeyFamily=ESTAT:PPP_CGS:cross")
root.set('xmlns:cross',"http://www.SDMX.org/resources/SDMXML/schemas/v2_0/cross")
root.set('xmlns:xsi',"http://www.w3.org/2001/XMLSchema-instance")
root.set('xsi:schemaLocation',"http://www.SDMX.org/resources/SDMXML/schemas/v2_0/message SDMXMessage.xsd urn:sdmx:org.sdmx.infomodel.keyfamily.KeyFamily=ESTAT:PPP_CGS:cross ESTAT_PPP_CGS_COUNTRY_Cross.xsd http://www.SDMX.org/resources/SDMXML/schemas/v2_0/cross SDMXCrossSectionalData.xsd")

header = Element('Header')
root.append(header)
header_ID = Element('ID')


header.append(header_ID)
header_ID.text = 'PPP_SRVIC_3'

header_Test = Element('Test')
header_Test.text = 'false'
header.append(header_Test)

header_Truncated = Element('Truncated')
header_Truncated.text = 'false' 
header.append(header_Truncated)

header_Name = Element('Name')
header_Name.text = 'PPP Dataset'
header.append(header_Name)

header_Prepared = Element('Prepared') # date , timedate.now typathing  @dynam
header_Prepared.text = '2014-06-16T15:00:16+00:00'
header.append(header_Prepared)

header_Sender = Element('Sender')
header_Sender.set('id','IS')
header.append(header_Sender)

header_Sender_Name = Element('Name')
header_Sender_Name.text = 'Statistic Iceland'
header_Sender.append(header_Sender_Name)

header_Sender_Contact = Element('Contact')
header_Sender_Contact_Name = Element('Name')
header_Sender_Contact_Department = Element('Department')
header_Sender_Contact_Role = Element('Role')
header_Sender_Contact_Telephone = Element('Telephone')
header_Sender_Contact_Fax = Element('Fax')
header_Sender_Contact_Email = Element('Email')

header_Sender_Contact.append(header_Sender_Contact_Name)
header_Sender_Contact.append(header_Sender_Contact_Department)
header_Sender_Contact.append(header_Sender_Contact_Role)
header_Sender_Contact.append(header_Sender_Contact_Telephone)
header_Sender_Contact.append(header_Sender_Contact_Fax)
header_Sender_Contact.append(header_Sender_Contact_Email)

header_Sender.append(header_Sender_Contact)

header_Receiver = Element('Receiver')
header_Receiver.set('id','EUROSTAT')
header_Receiver_Name = Element('Name')
header_Receiver.append(header_Receiver_Name)

header.append(header_Receiver)

header_DataSetID = Element('DataSetID')
header_DataSetID.text = "PPP_SRVIC_3-2014-06-16T15:00:16"  # time stuff @dynam
header_DataSetAction = Element('DataSetAction')
header_DataSetAction.text = 'Append'
header_Extracted = Element('Extracted')
header_Extracted.text = '2014-06-16T15:00:16+00:00'
header_ReportingBegin = Element('ReportingBegin')
header_ReportingBegin.text = '2014-01-01'
header_ReportingEnd = Element('ReportingEnd')
header_ReportingEnd.text = '2014-12-31'

header.append(header_DataSetID)
header.append(header_DataSetAction)
header.append(header_Extracted)
header.append(header_ReportingBegin)
header.append(header_ReportingEnd)

# end header

cgs_dataset = Element('cgs:dataset')
cgs_group = Element('cgs:group')

cgs_dataset.append(cgs_group)


cgs_grouap.set('REFERENCE_YEAR','2014')   # @dynam year from survey
cgs_group.set('PPP_SURVEY','SRVIC')      # @dynam survey code
cgs_group.set('REPORTING_COUNTRY','IS')  
cgs_group.set('CURRENCY','ISK')

root.append(cgs_dataset)



c.execute('SELECT * FROM survey_item WHERE survey_id=1') # @dynam choose from current survey
item_rows1 = c.fetchall()

#items = Items.objects.filter(survey=1)
#item_rows = []
#for i in Item.objects.raw('SELECT * FROM survey_item WHERE survey_id=1'):
# for i in Item.objects.filter(survey=1):
# 	print i
# 	item_rows.append(i)

item_rows = Item.objects.filter(survey=1).values_list()


print("this is BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")




for i_row in item_rows:
	#x_string = 'SELECT * FROM survey_itemcommentary WHERE item_id='+ '"' + i_row[0] + '"'
	#c.execute(x_string)
	#commentarys = c.fetchall()
	# commentarys = []
	# commentarys1 = ItemCommentary.objects.raw(x_string)
	# for c in commentarys1:
	# 	commentarys.append(c)

	commentarys = ItemCommentary.objects.filter(item=i_row).values_list()
	if (len(commentarys) > 0):
		commentary = commentarys[0]
		commentary_seasonality = "true" if commentary[0] else "false"
		commentary_representativity = "true" if commentary[4] else "false"
		commentary_comment = commentary[1]
		commentary_vat = str(commentary[2])
	else:
		commentary_vat = commentary_comment = commentary_representativity = commentary_seasonality = False


	cgs_section = Element('cgs:Section')
	cgs_section.set("EPC_ITEM",i_row[0])
	cgs_section.set("VAT", commentary_vat if commentary_vat else "0.255")                   # almost static
	cgs_section.set("REPRESENTIVITY", commentary_representativity if commentary_representativity else "true")         # default to true  ---- later to be derived from new model ItemCommentary
	cgs_section.set("SEASONALITY", commentary_seasonality if commentary_seasonality else "false")          # default to false -----^
	cgs_section.set("ITEM_COMMENT", commentary_comment if commentary_comment else "")               # default to ""  ----------^
	cgs_section.set("FINALIZED","true")              # true

	cgs_group.append(cgs_section)
	print("this")


