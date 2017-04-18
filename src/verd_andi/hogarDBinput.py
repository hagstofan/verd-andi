from xml.dom import minidom

import sqlite3, csv
from decimal import Decimal
connection = sqlite3.connect("db.sqlite3")
cursor =connection.cursor()


xmldoc = minidom.parse('../test-data/E16-1_IS_Final_country_list/itemList.xml')
itemlist = xmldoc.getElementsByTagName('item')

for s in itemlist:
	itemcols = [s.attributes['code'].value.encode('utf-8').decode('utf-8') , s.attributes['label'].value.encode('utf-8').decode('utf-8'), s.attributes['unit'].value.encode('utf-8').decode('utf-8')]
	# input into db
	itemcols.append(2)
	cursor.execute("INSERT INTO survey_item (code, label, unit, survey_id) VALUES (?,?,?,?);", itemcols)

	chars = s.getElementsByTagName('characteristic')
	for c in chars:
		enName = c.attributes['enName'].value
		name = c.attributes['name'].value
		item = s.attributes['code'].value
		lizt = [item, name, enName]
		
		isProp = False
		specify = False

		value = ""

		try:
			char_type = int(c.attributes['type'].value)
			if (char_type):
				lizt.append(char_type)
		except:
			pass

		try:
			isProp = c.attributes['isProperty'].value

		except:
			pass
		try:
			specify = c.attributes['specify'].value

		except:
			pass

		try:
			value = c.toxml().split(">")[1].split("<")[0].encode('utf-8').decode('utf-8')
		except:
			pass

		lizt.append(True if isProp else False)
		lizt.append(True if specify else False)
		lizt.append(value if value else False)

		cursor.execute("INSERT INTO survey_characteristic (item_id, name, enName, char_type, isProperty, specify, value) VALUES (?,?,?,?,?,?,?);", lizt) 


connection.commit()
connection.close()