# Verd-andi

PPP price collection tool.

Verdandi is a web based price collecting focused content management system.
Verdandi can take in a schema description of a survey from the item list xml of a SDMX sua file, creating items in a survey object in Verdandi.  Then users can collect prices for the
items in the survey.  Once price collection is finished or at any stage of the collection
process, Verdandi can produce xml containing the survey description and collected data.

## Installation

with Docker, first create a db container:
 
  > sudo docker run -e POSTGRES_USER=verdandi -e POSTGRES_PASSwORD=<my_password> --network=ppp-network -v /home/postgres-volume:/var/lib/postgresql/data -d --name=ppp_db postgres

this will persist the db data on host machine in /home/postgres-volume

currently the solution relies on a non-tracked configuration file localVars.py to be located in the directory verd-andi/src/verd_andi/verd_andi/ in the project, having the following form.
```
email_host = "your_email_host"
email_user = "your_email_user"
email_password = "your_email_password"
django_secret_key = "your_django_secret_key"
db_passwd = "your_database_password"
dkr_db_passwd = "database_password_in_the_docker_container"
```

next to build the verdandi image, in verdandi project root:

  > sudo docker build -t verdandi .

next run a verdandi container, on the same network as ppp_db:

	> sudo docker run -e DB=ppp_db -e DEBUG=True --network=ppp-network -p 8000:8000 --name=verdandi_app -v <host address>:<in container address> verdandi

I have used /data as the in container address, the host address should contain the sua files and survey pictures needed for the intended survey.

next run a shell inside the verdandi_app container, to run migrations, and management commands:

	> sudo docker exec -it verdandi_app bash

then inside the verdandi_app container:

	> python manage.py migrate

	> python manage.py createsuperuser

before running the needed management commands importing items to your survey, you must create a survey in verdandi using the verdandi admin interface, and your newly created superuser. Take note of the survey primary key, it will be 1 if it is the first survey in there. 
 Now you are set to add items to your survey, and then possibly pictures to the items, using managment commands. inside the running shell in verdandi_app container:

 	> python manage.py dbInput path_to_survey_itemlist.xml <survey pk>

 adding pictures:

 	> python manage.py import-pics path_to_directory_w_pics

 note that the pictures must have names coresponding to the item codes.

### About the persisting volumes

If the db container gets destroyed/removed the data persists on the host machine
in the /home/postgres-volume, all that needs to be done is to run the command to
create the db container again, with the same arguments as before, and all will be well.

If the verdandi_app container gets destroyed/removed, then it need only be created again
with the run command. in this case the import-pics management command can be run to recover the item pictures.









