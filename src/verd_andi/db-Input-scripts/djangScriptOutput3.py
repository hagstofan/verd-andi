
from xml.dom import minidom

import sqlite3, csv

import sys
from os import path


import django
django.setup()
from django.utils import timezone
import datetime
from survey.models import Survey, User, Item, ItemObserver, Characteristic, Observation, ObservedCharacteristic, ItemCommentary


conn = sqlite3.connect("db.sqlite3")
c =conn.cursor()


c.execute('SELECT * FROM survey_observation WHERE item_id="A.09.3.2.0.01.fa"')
all_rows = c.fetchall()


c.execute('SELECT * FROM survey_characteristic WHERE item_id="A.09.3.2.0.01.fa"')
all_rows = c.fetchall()




from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as etree


root=Element('CrossSectionalData')
tree=ElementTree(root)

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

header_Prepared = Element('Prepared') 
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
header_DataSetID.text = "PPP_SRVIC_3-2014-06-16T15:00:16"  
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



cgs_dataset = Element('cgs:dataset')
cgs_group = Element('cgs:group')

cgs_dataset.append(cgs_group)


cgs_group.set('REFERENCE_YEAR','2014')   
cgs_group.set('PPP_SURVEY','SRVIC')      
cgs_group.set('REPORTING_COUNTRY','IS')  
cgs_group.set('CURRENCY','ISK')

root.append(cgs_dataset)


item_rows = Item.objects.filter(survey=1).values_list()
print(len(item_rows))
for i_row in item_rows:
	print("hey dude")
	commentarys = ItemCommentary.objects.filter(item=i_row).values_list()
	print(len(commentarys))
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
	cgs_section.set("FINALIZED","true") 
	print("monkey")             
	cgs_group.append(cgs_section)
	
print "donkey"