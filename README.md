#bookMyShow

Flask app to imitate bookMyShow functionalities.

#Requirements

Python version: 3.7.4 or above

Pip version: pip 19.0.3 or above

Install latest version of flask,flask_cors,flask_httpauth,werkzeug,logging,threading using pip

#To run the app:

From command line type driver.py. The application is hosted on port 8000.

#All the restEndPointsExplained:

By default we have three users: admin,user1 and user2.

Their respective authentication passwords are admin,abc and xyz.

We have 3 cities where the application can be used: Mumbai, Delhi and Chennai.

Movie slots should be either '9AM','12PM','3PM','6PM' or '9PM'.

1.registerUser:

HTTP Method: POST

Sample body:
{
  "username":"user3",
  "password":"fgh"
}
Eg:localhost:8000/registerUser

Auth Required:
Username: admin
Password: admin


2.registerTheatre

HTTP Method: POST

Sample body:
{
  "user":"admin",
	"city":"Mumbai",
	"theatre":"temp"
}
Eg:localhost:8000/registerTheatre

Auth Required:
Username: admin
Password: admin


3.addMovie

HTTP Method: POST

Sample body:
{
	"user":"admin",
	"city":"Mumbai",
	"theatre":"temp",
	"movie":"Hello",
	"slot":"6PM"
}
Eg:localhost:8000/addMovie

Auth Required:
Username: admin
Password: admin


4.getCities

HTTP Method: GET

Eg:localhost:8000/getCities

Auth Not Required.

5.getTheatres

HTTP Method: GET

Eg:localhost:8000/getTheatres?movie=Vande&city=Mumbai

Auth Not Required.


6.availableShows

HTTP Method: GET

Eg:localhost:8000/availableShows?theatre=temp&city=Mumbai&movie=Hello

Auth Not Required.


7.seatMap

HTTP Method: GET

Eg:localhost:8000/seatMap?movie=Hello&city=Mumbai&theatre=temp&show=9AM

Auth Not Required.


8.bookTicket

HTTP Method: POST

Sample body:
{
	"city":"Mumbai",
	"theatre":"temp",
	"movie":"Hello",
	"show":"9AM"
}
Eg:localhost:8000/bookTicket

Auth Required:

All registered users (existing 3 users and new users registered via API)
