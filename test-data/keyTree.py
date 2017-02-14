import xmltodict

with open('./E15-2_IS_Final_country_list/itemList.xml') as fd:
    doc = xmltodict.parse(fd.read())


def walk(node, level):
    for key, item in node.items():
        if isinstance(item, dict):
            print ("  "* level) + "branch "+("-"* level)  + key 
            walk(item , level + 1)
        elif isinstance(item, list):
            print ("  "* level) + "list "+("-"* level)  + key
            for p in item:
                walk(p, level +1)
        else:
            print ("   "* level) + key



walk(doc, 0)
