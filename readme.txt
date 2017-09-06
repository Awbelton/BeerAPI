************
ABOUT
************

REST API created for Canpango by Anthony Belton.

Created with Python, Flask, and storing data in a cloud-based PostgreSQL database for data persistence.

Main code in config.py, calls to DB in beer.py, user.py, and reviews.py

************
INSTALLATION
************

This API was created using Python, Flask, and Flask-Restful. In order to properly run this application locally, you need to install the following:
- Flask
- Flask-Restful

You can use pip to install these.

Once installed, set the FLASK_APP variable to the config file provided:
set FLASK_APP=config.py

You can then run the application (make sure to be in the local directory):
Flask run

Navigate to http://localhost:5000 and ensure the application is running properly.

************
INSTRUCTIONS
************

You can use Postman, Curl, or simply the browser to make the appropriate GET, POST, PUT, and DELETE requests for this application.

Some examples (GET, POST, DELETE, PUT) for each of the main objects:

Beer:

Get full beer list (GET):
http://localhost:5000/beer
Get a single beer (GET):
http://localhost:5000/beer/<id> (http://localhost:5000/beer/1, for example)

Add a new beer (POST):
http://localhost:5000/beer?uid=0&ibu=1&calories=155&abv=25&brewery=Madison,WI&style=Lager

Edit Beer (PUT):
http://localhost:5000/beer/<id>?ibu=20&calores=250&abv=50&brewery=Colorado&style=Stout

Delete a Beer (DELETE):
http://localhost:5000/beer/<id>

Users:
Get full userlist (GET):
http://localhost:5000/user
Get a single beer (GET):
http://localhost:5000/user/<id> (http://localhost:5000/user/1, for example)

Add a new user (POST):
http://localhost:5000/user?user=awbelton&pw=1234

Reviews:

Get full review list (GET):
http://localhost:5000/review
Get a single review (GET):
http://localhost:5000/review/<id> (http://localhost:5000/review/1, for example)

Add a new review (POST):
http://localhost:5000/beer?uid=0&ibu=1&calories=155&abv=25&brewery=Madison,WI&style=Lager

Edit Review (PUT):
http://localhost:5000/review/<id>?uid=2&beerid=2&aroma=4&appearance=4&taste=7

Delete a Review (DELETE):
http://localhost:5000/review/<id>
