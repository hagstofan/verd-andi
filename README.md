# Verd-andi

PPP price collection tool.

Verdandi is a web based price collecting focused content management system.
Verdandi can take in a schema description of a survey from the item list xml of a SDMX sua file, creating a survey object in Verdandi.  Then users can collect prices for the
items in the survey.  Once price collection is finished or at any stage of the collection
process, Verdandi can produce xml containing the survey description and collected data.

## Installation

with Docker:
first create a db container:
 
  > dkr run -e POSTGRES_USER=verdandi -e POSTGRES_PASSwORD=<my_password> --network=ppp-network -v /home/postgres-volume:/var/lib/postgresql/data -d --name=ppp_db postgres

this will persist the db data on host machine in /home/postgres-volume
