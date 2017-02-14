import xmltodict

with open('./E15-2_IS_Final_country_list/itemList.xml') as fd:
    doc = xmltodict.parse(fd.read())


for key in doc.keys():
    print key

