#Project Housingtrader
A web service for housing trading. Developed with Django.

##Requirements
------------

* Python >=2.7 but < 3.0
* Django >=1.5
* django-localflavor
* MySQL-python or equivalent driver for the database of your choice

##Instructions
The file localsettings.py.dist should be copied and/or renamed to localsettings.py, and the DATABASE settings in the file should be changed to something that works with your local database.

Use the Django command syncdb to create the database.
For more help, see: https://docs.djangoproject.com/en/1.5/intro/tutorial01/#database-setup
