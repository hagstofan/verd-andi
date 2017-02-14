import sys
import xmltodict


def walk(node, level):
    if isinstance(node, str) or isinstance(node, unicode):
        print ("   "* level) + node
        return
    for key, item in node.items():
        if isinstance(item, dict):
            print ("  "* level) + "branch "+("-"* level)  + key 
            walk(item , level + 1)
        elif isinstance(item, list):
            print ("  "* level) + "list "+("-"* level)  + key
            for p in item:
                walk(p, level +1)
        else:
            continue
            #print ("   "* level) + key




if __name__ == "__main__":
    #
    if(len(sys.argv) < 2):
        print "usage: python keytree.py <file>"
        sys.exit(0)

    with open(sys.argv[1]) as fd:
        doc = xmltodict.parse(fd.read())

    walk(doc,0)
