import os, sys
from django.core.management.base import BaseCommand, CommandError
from survey.models import *
from django.core.files import File
from django.conf import settings

from xml.dom import minidom
import csv
from decimal import Decimal

from survey.models import *

"""
if(len(sys.argv) < 2):
    print "usage: python manage.py input-pics "
    sys.exit()


for filename in os.listdir("/"):
    print(str(filename))
"""


class Command(BaseCommand):

    help = "specify the itemList.xml file and then the survey number"

    def add_arguments(self, parser):
        parser.add_argument('file_path', nargs='+', type=str)
        parser.add_argument('survey_number', nargs='+', type=int)


    def handle(self, *args, **options):
        #self.stdout.write("hey dudes" + " " + str(options['pic_directory'][0]))
        fpath = options['file_path'][0]
        #self.stdout.write(os.path.isabs(fpath))
        survey = options['survey_number'][0]
        if(os.path.isabs(fpath)):
            # absolute path givern
            self.parse_input(fpath, survey)
        else:
            directory = settings.BASE_DIR
            filename = os.path.join(directory, fpath)
            if(os.path.isabs(filename)):
                print(filename)
                self.parse_input(filename, survey)


    def parse_input(self, file, survey_id):
        xmldoc = minidom.parse(file)
        itemlist = xmldoc.getElementsByTagName('item')
        for s in itemlist:
            itemcols = [s.attributes['code'].value.encode('utf-8').decode('utf-8') , s.attributes['label'].value.encode('utf-8').decode('utf-8'), s.attributes['unit'].value.encode('utf-8').decode('utf-8')]
            # input into db
            itemcols.append(3)
            print("adding item - " + str(s.attributes['code'].value.encode('utf-8').decode('utf-8')))
            survey = Survey.objects.get(pk=survey_id)
            item = Item.objects.create(
                code = s.attributes['code'].value.encode('utf-8').decode('utf-8'),
                label = s.attributes['label'].value.encode('utf-8').decode('utf-8'),
                unit = s.attributes['unit'].value.encode('utf-8').decode('utf-8'),
                survey = survey,
                )
            item.save()

            # Now the characteristics
            chars = s.getElementsByTagName('characteristic')
            for c in chars:
                enName = c.attributes['enName'].value
                name = c.attributes['name'].value
                item_code = s.attributes['code'].value
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

                # add the char.
                # cursor.execute("INSERT INTO survey_characteristic (item_id, name, enName, char_type, isProperty, specify, value) VALUES (?,?,?,?,?,?,?);", lizt)
                characteristic = Characteristic.objects.create(
                    item = item,
                    name = name,
                    enName = enName,
                    char_type = char_type,
                    isProperty = True if isProp else False,
                    specify = True if specify else False,
                    value = value,
                )
                characteristic.save()

            # print(itemcols)
                


    # xmldoc = minidom.parse('../../test-data/E17-2_Final_country_list/itemList.xml')




