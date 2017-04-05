from xml.dom import minidom

import sqlite3, csv
from decimal import Decimal
connection = sqlite3.connect("db.sqlite3")
cursor =connection.cursor()


xmldoc = minidom.parse('./E15-2_IS_Final_country_list/itemList.xml')
itemlist = xmldoc.getElementsByTagName('item')
print(len(itemlist))
print(itemlist[0].attributes['label'].value)
for s in itemlist:
	print(s.attributes['label'].value)
	print(s.attributes['code'].value)
	print(s.attributes['unit'].value)
	# input into db
	cursor.execute("INSERT INTO perap_item (code, label, unit) VALUES (?,?,?);", [s.attributes['code'].value , s.attributes['label'].value, s.attributes['unit'].value])

	chars = s.getElementsByTagName('characteristic')
	for c in chars:
		print("-----"+c.attributes['enName'].value)
		print("      "+c.attributes['name'].value)
		enName = c.attributes['enName'].value
		name = c.attributes['name'].value
		item = s.attributes['code'].value
		lizt = [item, name, enName]
		try:
			print("      "+c.attributes['type'].value)
			char_type = int(c.attributes['type'].value)
			if (char_type):
				lizt.append(char_type)
		except:
			pass
		try:
			print("      "+c.attributes['isProperty'].value)
			isProp = c.attributes['isProperty'].value
			if (isProp):
				lizt.append(isProp)
		except:
			pass
		try:
			print("      "+c.attributes['specify'].value)
			specify = c.attributes['specify'].value
			if (specify):
				lizt.append(specify)
		except:
			pass

		# input into db
		crusor.execute("INSERT INTO perap_characteristic (item, name, enName, char_type, isProperty, specify VALUES (?,?,?,?,?,?);" 


connection.commit()
"""
# from other project ..


import sqlite3, csv
from decimal import Decimal
connection = sqlite3.connect("db.sqlite3")
cursor =connection.cursor()

reader = csv.reader(open('join.csv','r'), delimiter=',')

for row in reader:
    to_db = [row[0], row[1], row[2],float(row[3])]
    cursor.execute("INSERT INTO vorulisti_product (product_id, title, sku, weight) VALUES (?,?,?,?);", to_db)

connection.commit()



"""