#The data.py module consists of variables and class declaration which are to be used by various other modules.
#It is like a store house of variables where all the classes and variables are defined and declared
#Other modules needs to import variables from data.py when needed
#It also contains the API endpoints (routes) to serve data from the database for charts or for further processing
#Instance of the app to be imported
from myproject import app
#Jsonify is used to send the response from the server in JSON format. The data points are served in JSON format through jsonify
from flask import Flask, jsonify
#Render_template is used to server html files when requested. Request is used to process POST form request
from flask import render_template, request, send_from_directory
#Various other SQL related modules and settings are imported for SQL Transactions
from database import db_session, metadata
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import mapper, clear_mappers
from flask_sqlalchemy import SQLAlchemy

#This is the format to store all the duration and timing related paramenters like trip_duration, engine_runtime into the database
FMT = "%H:%M:%S"
#Number of devices added or linked to the server as of now
deviceNumbers = 2;

#Class definition for raw individual vehicle data
#This class basically represents the raw data table in database
#SQLAlchemy maps this class to table in database and helps to manage the table in much more efficient way
#The attributes of this class represents column of the table of raw data like erpm, engine_load
class Device(object):
  query = db_session.query_property()
  def __init__(self, erpm, engine_load, runtime_crank, throttle_position, latitude, longitude, vehicle_speed, data_date, data_time):
    self.erpm = erpm
    self.engine_load = engine_load
    self.runtime_crank = runtime_crank
    self.throttle_position = throttle_position
    self.latitude = latitude
    self.longitude = longitude
    self.vehicle_speed = vehicle_speed
    self.data_date = data_date
    self.data_time = data_time

#Class definition for seconday table in database. It contains trip wise information for individual vehicles like number_of_trips, total_distance
#This class is automatically mapped to respective table in database by SQLAlchemy
class Device_derived(object) :
  query = db_session.query_property()
  def __init__(self, trip_duration, trip_distance, trip_avg_speed, trip_avg_erpm, trip_avg_engine_load, trip_avg_throttle_position, trip_date, trip_end_time):
    self.trip_duration = trip_duration
    self.trip_distance = trip_distance
    self.trip_avg_speed = trip_avg_speed
    self.trip_avg_erpm = trip_avg_erpm
    self.trip_avg_engine_load = trip_avg_engine_load
    self.trip_avg_throttle_position = trip_avg_throttle_position
    self.trip_date = trip_date
    self.trip_end_time = trip_end_time

#Class definition for cummulative table record in the database. This table contains one row for each vehcile representing overall stats 
#A query done on this table will give a list of overall stats of all the vehicles
class Cummulative_record(object) :
  query = db_session.query_property()
  def __init__(self, device_number, device_name, trips_number, trips_avg_duration, trips_avg_distance, trips_avg_engine_load, trips_avg_erpm, trips_avg_throttle_position, trips_avg_speed, avg_engine_load, avg_erpm, avg_throttle_position, avg_speed, trips_total_distance, trips_total_duration) :
    self.device_number = device_number
    self.device_name = device_name
    self.trips_number = trips_number
    self.trips_avg_duration = trips_avg_duration
    self.trips_avg_distance = trips_avg_distance
    self.trips_avg_engine_load = trips_avg_engine_load
    self.trips_avg_erpm = trips_avg_erpm
    self.trips_avg_throttle_position = trips_avg_throttle_position
    self.trips_avg_speed = trips_avg_speed
    self.avg_engine_load = avg_engine_load
    self.avg_erpm = avg_erpm
    self.avg_throttle_position = avg_throttle_position
    self.avg_speed = avg_speed
    self.trips_total_distance = trips_total_distance
    self.trips_total_duration = trips_total_duration


class Last_data(object) :
  query = db_session.query_property()
  def __init__(self, device_number, trip_update, last_runtime_crank, last_trip_time, last_trip_date, count, avg_speed, avg_erpm, avg_engine_load, avg_throttle_position, trip_start_time) :
    self.device_number = device_number
    self.trip_update = trip_update
    self.last_runtime_crank = last_runtime_crank
    self.last_trip_time = last_trip_time
    self.last_trip_date = last_trip_date
    self.count = count
    self.avg_speed = avg_speed
    self.avg_erpm = avg_erpm
    self.avg_engine_load = avg_engine_load
    self.avg_throttle_position = avg_throttle_position
    self.trip_start_time = trip_start_time


#TO shutdown or end the SQL session when app shutsdown
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

#API endpoint to get or extract data from database with mentioned vehicle_id and column name 
@app.route('/data/<int:device_id>/chart/<int:chart_id>')
def show_all(device_id, chart_id):
  #devices (Variable defined below) is object of class Table. For general purpose we can consider devices as equivalent to table in the database
  devices = Table("device"+str(device_id), metadata,autoload= True)
  #Removes the earlier mapping done (if Any) between tables and classes by SQLAlchemy
  clear_mappers();
  #Mapper maps the devices table to the Device class which is defined in data.py. This is the main purpose of SQLAlchemy
  #Now any query on class Device is equivalent to direct Query on devices table.
  mapper(Device, devices)
  # chart_id represents the id number of chart for which the data is required
  if (chart_id == 1) :
    #Querying from table in database is as simple as this with the help of mappers
    #data stores all the values stored in the table
    data = Device.query.all();
    value_list=[['erpm','engine_load']]
    #data is now a list which stores all the table data. So, we can iterate over the list to access the value of each row
    for datas in data :
      #The columns of a row are now attribute of class Device. we can access colums of a particular row by typing data[i].column_name
      #Value_list is a list, constructed in a format required by frontend.
      value_list.append([datas.erpm, datas.engine_load])
    clear_mappers();
    #jsonify is used to return the response list in JSON format.
    return  jsonify(value_list)

  elif (chart_id == 2):
    #Querying for a particular column with SQLAlchemy is as simples as that. Chart_id : 2 needs vehicle_speed only for a particular vehcile
    data = Device.query.with_entities(Device.vehicle_speed)
    value_list = [['speed','value']]
    for datas in data :
      #value_list is created in format as required by front-end
      value_list.append(['speed',datas.vehicle_speed])
    clear_mappers();
    #Response sent in JSON format
    return jsonify(value_list)
