# werkplaats-3-inhaalopdracht-actiontypes

Dit project is een webapplicatie waarmee studenten een vragenlijst invullen om hun "action type" te bepalen. 
Docenten kunnen vervolgens via een dashboard de studenten hun resultaten bekijken en beheren.
Ook kunnen de docenten hier studenten toevoegen, en verwijderen. 


**Quick-start guide:**

Virtuele omgeving instellen: Open PyCharm en laad het project. Ga naar File > Settings > Project: jouw_project > Python Interpreter en kies Add Interpreter. Selecteer Virtualenv en kies een nieuw of bestaand pad.


Installeren van alle requirments: Open de Terminal in PyCharm en vul het volgende in:

pip install -r requirements.txt


Daarna kun je het importscript uitvoeren om de JSON-bestanden (studenten en stellingen) in de database te laden:

python import_script.py of gewoon het bestand openen via pycharm en dan op run boven in klikken:)


Vervolgens start je de applicatie met:

python run.py of gewoon het bestand openen via pycharm en dan op run boven in klikken:)

De app draait dan lokaal op http://127.0.0.1:5000.

**Uitleg van de app zelf:**

**_Studenten_**
Zodra de app (hopelijk) runt, en je de bovenstaande link hebt geopent, kom je op de welkom/begin pagina.
hier kan je een studentnummer invoeren. als voorbeeld kan je deze gebruiken: 2824197, 8826007, 5074078.
Als je het studentnummer invoert en op start vragenlijst klikt, begint de vragenlijst. 
Hier kan de student 1 van de 2 antwoorden invoeren over de bovenstaande stelling, ook is er bovenin een progress bar.
Zodra je een ongeldig studentnummer invoert krijg je een foutmelding; te testen met 000001 of 11111 etc.

Als je klaar bent met de vragenlijst zie je meteen het actiontype, je kan daarna weer terug gaan naar het beginscherm.

**_Docenten_**
Op het beginscherm staat rechtboven in Docenten login, de huidige test login is user:admin password:test123
Zodra je bent ingelogd krijg je een overzicht van alle studenten. 
hier kan je hun Studentnummer, naam, klas, actiontype en laatst ingevulde datum van de vragenlijst zien.
Je vanuit dit scherm ook studenten toevoegen en verwijderen. Hoe je dit doet spreekt voorzich :)
In de studenten details kan je een team aangeven, alhoewel ik hier nog mee bezig ben, dus werkt het nu nog niet.

Het is uiteindelijk niet gelukt om de teams werkend te krijgen.


**Bronnen:** 

Flask routing: 
https://www.geeksforgeeks.org/flask-app-routing/ https://stackoverflow.com/questions/49915758/what-is-flask-route https://www.youtube.com/watch?v=XTLg6TLfy7M https://www.youtube.com/watch?v=pBDytquUHA0 https://flask.palletsprojects.com/en/stable/tutorial/database/ https://python-adv-web-apps.readthedocs.io/en/latest/flask_db1.html https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world !!!
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
https://realpython.com/tutorials/flask/

SQLAlchemy en Database:
https://docs.sqlalchemy.org/en/20/orm/quickstart.html
https://flask-sqlalchemy.palletsprojects.com/
https://hackersandslackers.com/sqlalchemy-data-models/

REST API en JSON in Flask:
https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask
https://codeburst.io/flask-ajax-application-386db1b88c13

Flask login/ sessions: 
https://www.geeksforgeeks.org/user-login-and-registration-using-flask/

CSV export:
https://docs.python.org/3/library/csv.html