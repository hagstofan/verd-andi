# Verd-andi

PPP price collection tool.

Verdandi is a web based price collecting focused content management system.
Verdandi can take in a schema description of a survey from the item list xml of a SDMX sua file, creating a survey object in Verdandi.  Then users can collect prices for the
items in the survey.  Once price collection is finished or at any stage of the collection
process, Verdandi can produce xml containing the survey description and collected data.

## Installation

with Docker, first create a db container:
 
  > sudo docker run -e POSTGRES_USER=verdandi -e POSTGRES_PASSwORD=<my_password> --network=ppp-network -v /home/postgres-volume:/var/lib/postgresql/data -d --name=ppp_db postgres

this will persist the db data on host machine in /home/postgres-volume

currently the solution relies on a non-tracked configuration file localVars.py to be located in the directory verd-andi/src/verd_andi/verd_andi/, having the following form.
```
email_host = "your_email_host"
email_user = "your_email_user"
email_password = "your_email_password"
django_secret_key = 'your_django_secret_key'
db_passwd = 'your_database_password'
dkr_db_passwd = 'database_password_in_the_docker_container'
```

next to build the verdandi image, in verdandi project root:

  > sudo docker build -t verdandi .

