The server backend is developed on Flask-python framework. The database used is PostgreSQL. 
The Flask-App is structured as standard flask application. The first directory contains basic configurations for running the app. The seconds directory named 'myproject' contains core application modules which are as follows :-

1). __init__.py : It contains the basic app running code. It doesn't contain any API endpoints. All the api-endpoints are further imported from other modules. 

2). data.py : It is the store house of variables. All the variables and classes are defined and declared in this module. It also contains API endpoints to return required data from the database. 

3). database.py : It contains the initialization of SQLAlchemy engine. It binds the app session with SQL server for fast, secured and efficient SQL transactions.

4). record.py : It contains API endpoints where individual devices POST their raw data. It parses the sent data and store the data in respective tables. 

5). views.py : It contains API endpoints to serve the Static HTML pages or images related to the website . 

The static and templates folder contains the HTML and JavaScript files. 

In the first directory the setup.py modules install the package (Server Package) on your system. It is developed in standard format as mentioned by setuptools.

The wsgi.py acts as entry point for our application. This will tell our uWSGI server how to interact with the application.We are using uWsgi server to serve our flask App. The myproject.ini is the configuration file for uWsgi server. 

Now Nginx server is used to handle proxy request over the internet and then forward the request to the uWsgi server.

The whole documentation of how to deploy our Flask App on nginx is mentioned in the link presented below :

https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-16-04

We are using digitalocean as of now to get online server space but this process can be repeated on any Linux server to host the app. 

Step by step instructions to install the app on your local system is mentioned in README.md file. 

The database is designed in three layers to make the data visualisation easier and accessible as follows :

a) Primary Table
b) Secondary Table
c) Tertiary Table

Detailed description of database structure is as follows :
a)	Primary Table : Every device has it's own table named deviceID . For example Device1, Device2. This table stores the raw data directly from the device. As of now it have few parameters which are :-

    Serial. number (PRIMARY KEY IN TABLE)
    erpm
    engine_load
    runtime_crank
    throttle_position
    latitude
    longitude
    altitude
    vehicle_speed
    data_date
    data_time

b)	Secondary Table : whenever the new_data parameter in the POST form request is equal to 1, it indicates the beginning of a new trip. So based on the value stored in the last_data table we have all the statistics of the trip which just get commenced. We add all the trip details to the seconday table named as device_derivedID. For example : device_derived1, device_derived2 . It contains the following columns :-
    trip_duration
    trip_distance
    trip_avg_speed
   	trip_avg_erpm
    trip_avg_engine_load
    trip_avg_throttle_position
    trip_date
    trip_end_time
    trip_start_time
    trip_latitude
    trip_longitude
    trip_altitude

c) Tertiary Table : Whenever the device signals the end of the previous trip. The whole of trip detail is stored in secondary table. There is also a tertiary table to store the over all cummulative record of all the devices at one place.
It has one row for one device. It contains columns as mentioned :-

	device_number
	device_name
	trips_number
	trips_avg_duration
	trips_avg_distance
	trips_avg_engine_load
	trips_avg_erpm
	trips_avg_throttle_position
	trips_avg_speed
	avg_engine_load
	avg_erpm
	avg_throttle_position
	avg_speed
	trips_total_distance
	trips_total_duration

Communication protocol between device and server :
The device sends 12 parameters in general :-
    device_id
    new_data
    data_date
    data_time
    latitude
    longitude
    altitude
    engine_load
    erpm
    vehicle_speed
    runtime_crank
    throttle_position
    
new_data shows whether the data recived represents new trip or the ongoing previous trip.
Whenever the engine starts (or cranks), it represents that previous trip is over and a new trip is going to be started.
So, the first data which is sent by the device when engine starts, has new_data parameter set to 1. This first data doesn't represent any ecu information it just shows that old trip is complete. It is not stored in database. That's why it has only six parameters as mentioned :-
	device_id
    new_data
    data_date
    data_time
    latitude
    longitude
