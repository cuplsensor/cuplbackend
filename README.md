# wsbackend
This (the app) is a Python [WSGI](https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface) web application.
The app has been built atop of Armin Ronacher's excellent [Flask](https://palletsprojects.com/p/flask/) framework. 
It primarily uses [wscodec](https://github.com/websensor/wscodec) to extract timestamped temperature and humidity 
samples from base64 strings. The app receives these from [wsfrontend](https://github.com/websensor/wsfrontend) via an 
Application Programming Interface (API). 

Extracted data are persisted in a [postgres](https://www.postgresql.org/) database. The app employs [SQLAlchemy](https://www.sqlalchemy.org/) 
[object-relational mapper](https://www.fullstackpython.com/object-relational-mappers-orms.html) to map database records to Python objects. 
Very little SQL is used. 