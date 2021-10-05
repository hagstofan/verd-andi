import os
from django.core.management.base import BaseCommand
from survey.models import Item
from django.core.files import File
from django.conf import settings

"""
    # if(len(sys.argv) < 2):
    #     print "usage: python manage.py input-pics "
    #     sys.exit()


    # for filename in os.listdir("/"):
    #     print(str(filename))
"""


class Command(BaseCommand):
    help = "inputs picture to items having the same code as picture number"

    def add_arguments(self, parser):
        parser.add_argument('pic_directory', nargs='+', type=str)

    def handle(self, *args, **options):
        fpath = options['pic_directory'][0]
        # self.stdout.write(os.path.isabs(fpath))
        print(fpath)
        print(os.path.isabs(fpath))
        if(os.path.isabs(fpath)):
            print(fpath)
            self.list_dir(fpath)
        else:
            # directory = os.path.dirname(os.getcwd())
            # directory = os.path.dirname(__file__)
            directory = settings.BASE_DIR
            filename = os.path.join(directory, fpath)
            print(directory)
            print(filename)
            # print(settings.BASE_DIR)
            if(os.path.isabs(filename)):
                print(filename)
                self.list_dir(filename)

    def list_dir(self, directory):
        for filename in os.listdir(directory):
            # print(str(filename).split("_")[0])
            try:
                item = Item.objects.get(code=str(filename).split("_")[0])
            except:
                print("Item does not exist, looking for {0}".format(str(filename).split("_")[0]))
                continue
            if(item):
                # print(filename)
                # print(directory + filename)
                file = directory + "/" + filename
                print(file)
                item.picture.save(filename, File(open(file, 'rb')))

# Item.objects.filter(code="A.05.1.1.1.01.ca")

# item = Item.objects.get(code="A.05.1.1.1.01.ca")
# from django.core.files import File
# item.picture.save('A.05.1.1.1.01.ca_.jpg',
# File(open('/home/bergurth/projects/verd-andi/test-data/frhea-pics-2017/A.05.1.1.1.01.ca_.jpg','r')))
