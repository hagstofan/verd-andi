from xml.dom import minidom

import sqlite3, csv
from decimal import Decimal
connection = sqlite3.connect("db.sqlite3")
cursor =connection.cursor()


xmldoc = minidom.parse('../test-data/E15-2_IS_Final_country_list/itemList.xml')
itemlist = xmldoc.getElementsByTagName('item')
print(len(itemlist))
print(itemlist[0].attributes['label'].value)
for s in itemlist:
	print(s.attributes['label'].value)
	print(s.attributes['code'].value)
	print(s.attributes['unit'].value)
	itemcols = [s.attributes['code'].value.encode('utf-8').decode('utf-8') , s.attributes['label'].value.encode('utf-8').decode('utf-8'), s.attributes['unit'].value.encode('utf-8').decode('utf-8')]
	# input into db
	#cursor.execute("INSERT INTO perap_item (code, label, unit) VALUES (?,?,?);", itemcols)

	chars = s.getElementsByTagName('characteristic')
	for c in chars:
		print("-----"+c.attributes['enName'].value)
		print("      "+c.attributes['name'].value)
		enName = c.attributes['enName'].value
		name = c.attributes['name'].value
		item = s.attributes['code'].value
		lizt = [item, name, enName]
		
		isProp = False
		specify = False

		value = ""

		try:
			print("      "+c.attributes['type'].value)
			char_type = int(c.attributes['type'].value)
			if (char_type):
				lizt.append(char_type)
		except:
			pass
		# lizt.append(False)
		# lizt.append(False)

		try:
			print("      "+c.attributes['isProperty'].value)
			isProp = c.attributes['isProperty'].value
			# if (isProp):
			# 	lizt.append(isProp)
		except:
			pass
		try:
			print("      "+c.attributes['specify'].value)
			specify = c.attributes['specify'].value
			# if (specify):
			# 	lizt.append(specify)
		except:
			pass

		try:
			print("      "+c.data+"-----------------------   (>-----")
			value = c.nodeValue.encode('utf-8').decode('utf-8')
		except:
			pass

		lizt.append(True if isProp else False)
		lizt.append(True if specify else False)
		# input into db
		#cursor.execute("INSERT INTO perap_characteristic (item_id, name, enName, char_type, isProperty, specify) VALUES (?,?,?,?,?,?);", lizt) 

		#cursor.execute("INSERT INTO perap_characteristic (item_id, name, enName, char_type, isProperty, specify, value) VALUES (?,?,?,?,?,?,?);", lizt) 


connection.commit()
connection.close()