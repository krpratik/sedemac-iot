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
from datetime import timedelta, datetime

#This is the format to store all the duration and timing related paramenters like trip_duration, engine_runtime into the database
FMT = "%H:%M:%S"
#Number of devices added or linked to the server as of now
deviceNumbers = 4;

#Class definition for raw individual vehicle data
#This class basically represents the raw data table in database
#SQLAlchemy maps this class to table in database and helps to manage the table in much more efficient way
#The attributes of this class represents column of the table of raw data like erpm, engine_load
class Device(object):
  query = db_session.query_property()
  def __init__(self, erpm, engine_load, runtime_crank, throttle_position, latitude, longitude, altitude, vehicle_speed, data_date, data_time):
    self.erpm = erpm
    self.engine_load = engine_load
    self.runtime_crank = runtime_crank
    self.throttle_position = throttle_position
    self.latitude = latitude
    self.longitude = longitude
    self.altitude = altitude
    self.vehicle_speed = vehicle_speed
    self.data_date = data_date
    self.data_time = data_time

#Class definition for seconday table in database. It contains trip wise information for individual vehicles like number_of_trips, total_distance
#This class is automatically mapped to respective table in database by SQLAlchemy
class Device_derived(object) :
  query = db_session.query_property()
  def __init__(self, trip_duration, trip_distance, trip_avg_speed, trip_avg_erpm, trip_avg_engine_load, trip_avg_throttle_position, trip_date, trip_end_time, trip_start_time, trip_latitude, trip_longitude, trip_altitude):
    self.trip_duration = trip_duration
    self.trip_distance = trip_distance
    self.trip_avg_speed = trip_avg_speed
    self.trip_avg_erpm = trip_avg_erpm
    self.trip_avg_engine_load = trip_avg_engine_load
    self.trip_avg_throttle_position = trip_avg_throttle_position
    self.trip_date = trip_date
    self.trip_end_time = trip_end_time
    self.trip_start_time = trip_start_time
    self.trip_latitude = trip_latitude
    self.trip_longitude = trip_longitude
    self.trip_altitude = trip_altitude

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

#Class definition for Last data record of devices. This table has one row for each device to store it's last data and 
#information like running average statistics.
class Last_data(object) :
  query = db_session.query_property()
  def __init__(self, device_number, trip_update, last_runtime_crank, last_trip_time, last_trip_date, count, avg_speed, avg_erpm, avg_engine_load, avg_throttle_position, trip_start_time, trip_latitude, trip_longitude, trip_altitude) :
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
    self.trip_latitude = trip_latitude
    self.trip_longitude = trip_longitude
    self.trip_altitude = trip_altitude



#TO shutdown or end the SQL session when app shutsdown
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

###### From Here, various Routes(API endpoints) are defined to access tables across database to get data and plot charts or analyse

#This API endpoint to get the last recorded location of all the devices
@app.route('/data/location')
def location():
  #Unmaps all the previous mappping between classes and tables earlier done by SQLalchemy
  clear_mappers()
  last_data = Table("last_data", metadata, autoload= True)
  #Maps the respective mentioned class to the respective table
  mapper(Last_data, last_data)
  #querying from the table
  data= Last_data.query.all()
  #creating the response to be sent in the proper format required by the frontend
  value_list= [['Lat','Long']]
  for datas in data :
    value_list.append([float(datas.trip_latitude), float(datas.trip_longitude)])
  #Mapping removed after the response is created
  clear_mappers();
  #Created response sent
  return jsonify(value_list)

#API endpoint to serve the trip-wise detail of a particular vehicle. like trip duration and trip distance
@app.route('/data/<int:device_id>/tripdetail/<int:chart_id>')
def trip_detail(device_id, chart_id) :
  #Unmapping previous mapping
  clear_mappers();
  devices_derived = Table("device_derived"+str(device_id), metadata,autoload=True)
  #Now mapping the required tables to respective classes
  mapper(Device_derived, devices_derived)
  ##If ID == 1 we have to respond with trip_duration data and if ID == 2 we have to respond with trip_distance
  if (chart_id == 1) :
    data = Device_derived.query.with_entities(Device_derived.trip_duration)
    value_list = [['trip_duration','value']]
    for datas in data :
      #Calculation of duration from datetime.time object
      trip_duration = datetime.strptime(str(datas.trip_duration), FMT) - datetime.strptime('00:00:00', FMT)
      value_list.append(['trip_duration', trip_duration.total_seconds()/60])
    clear_mappers();
    return jsonify(value_list)
  elif (chart_id == 2) :
    data = Device_derived.query.with_entities(Device_derived.trip_distance)
    value_list = [['trip_distance','value']]
    for datas in data :
      value_list.append(['trip_distance', float(datas.trip_distance)])
    clear_mappers();
    return jsonify(value_list)
  else :
    return ("Chart not found")

#API endpoint to return the co-ordinates of the way-points through which the vehicle passed in the mentioned trip_id
#If the passed trip_id == 0, then we return the path of the last commited trip of the mentioned vehicle
@app.route('/data/<int:device_id>/trip/<int:trip_id>')
def track_path(device_id, trip_id):
  clear_mappers();
  last_data = Table("last_data", metadata, autoload= True)
  mapper(Last_data, last_data)
  devices = Table("device"+str(device_id), metadata,autoload= True)
  mapper(Device, devices)
  if (trip_id == 0):
    data_last = Last_data.query.filter(Last_data.device_number == int(device_id)).first();
    data = Device.query.filter(Device.data_date >= data_last.last_trip_date);
    value_list = [['Lat','Long']]
    for datas in data :
      if not ((datas.data_date == data_last.last_trip_date) and (datas.data_time < data_last.trip_start_time)):
        value_list.append([float(datas.latitude), float(datas.longitude)])
    clear_mappers();
    return jsonify(value_list)
  else :
    return ('No Such trip Found')

#API endpoint to serve cummulative detail of all the trips done so far by a particular device 
@app.route('/data/<int:device_id>/details')
def cummulative_individual_data(device_id):
  clear_mappers();
  cummulative_Record = Table("cummulative_record", metadata, autoload=True)
  mapper(Cummulative_record, cummulative_Record)
  data = Cummulative_record.query.filter(Cummulative_record.device_number == device_id).first()
  value_list = {}
  value_list['device_number'] = data.device_number
  value_list['trips_number'] = data.trips_number
  value_list['trips_avg_duration'] = str(data.trips_avg_duration)
  value_list['trips_avg_distance'] = data.trips_avg_distance
  value_list['trips_avg_engine_load'] = data.trips_avg_engine_load
  value_list['trips_avg_erpm'] = data.trips_avg_erpm
  value_list['trips_avg_throttle_position'] = data.trips_avg_throttle_position
  value_list['trips_avg_speed'] = data.trips_avg_speed
  value_list['avg_engine_load'] = data.avg_engine_load
  value_list['avg_erpm'] = data.avg_erpm
  value_list['avg_throttle_position'] = data.avg_throttle_position
  value_list['avg_speed'] = data.avg_speed
  value_list['trips_total_distance'] = data.trips_total_distance
  value_list['trips_total_duration'] = str(data.trips_total_duration)
  clear_mappers();
  return jsonify(value_list)

#API endpoints to retrun various cummulative parameter as denoted by chart_id. 
@app.route('/data/chart/<int:chart_id>')
def cummulative_data(chart_id):
  clear_mappers()
  cummulative_Record = Table("cummulative_record", metadata, autoload=True)
  mapper(Cummulative_record, cummulative_Record)
  #chart_id == 1 returns avg_trip_duration of every vehicle. It will help us to determine the average trip duration of a general trip
  if (chart_id == 1) :
    data = Cummulative_record.query.with_entities(Cummulative_record.trips_avg_duration)
    value_list = [['trips_avg_duration','value']]
    for datas in data :
      trips_avg_duration = datetime.strptime(str(datas.trips_avg_duration), FMT) - datetime.strptime('00:00:00', FMT)
      value_list.append(['trip_avg_duration', trips_avg_duration.total_seconds()])
    clear_mappers();
    return jsonify(value_list)
  #chart_id == 2 returns avg_trip_distance of all the registered vehicles.It will help us to determine the average trip distance of a general trip
  elif (chart_id == 2) :
    data = Cummulative_record.query.with_entities(Cummulative_record.trips_avg_distance)
    value_list = [['trips_avg_distance','value']]
    for datas in data :
      value_list.append(['trip_avg_distance', datas.trips_avg_distance])
    clear_mappers();
    return jsonify(value_list)
  #chart_id == 3 returns average engine load of all the vehicles. It was help us to predict engine load of a general trip with significant probability
  elif (chart_id == 3) :
    data = Cummulative_record.query.with_entities(Cummulative_record.trips_avg_engine_load)
    value_list = [['trips_avg_engine_load','value']]
    for datas in data :
      value_list.append(['trip_avg_engine_load', datas.trips_avg_engine_load])
    clear_mappers();
    return jsonify(value_list)
  #chart_id == 4 returns average engine load of all the vehicles. It will help us to predict the average erpm of a general trip with significant probability
  elif (chart_id == 4) :
    data = Cummulative_record.query.with_entities(Cummulative_record.trips_avg_erpm)
    value_list = [['trips_avg_erpm','value']]
    for datas in data :
      value_list.append(['trip_avg_erpm', datas.trips_avg_erpm])
    clear_mappers();
    return jsonify(value_list)
  #chart_id == 5 will return average spped of all the vehicles
  elif (chart_id == 5) :
    data = Cummulative_record.query.with_entities(Cummulative_record.trips_avg_speed)
    value_list = [['trips_avg_speed','value']]
    for datas in data :
      value_list.append(['trip_avg_speed', datas.trips_avg_speed])
    clear_mappers();
    return jsonify(value_list)
  #chart_id == 6 will return average engine load of all the vehicles
  elif (chart_id == 6) :
    data = Cummulative_record.query.with_entities(Cummulative_record.avg_engine_load)
    value_list = [['avg_engine_load','value']]
    for datas in data :
      value_list.append(['avg_engine_load', datas.avg_engine_load])
    clear_mappers();
    return jsonify(value_list)
  #chart_id = 8 will return average erpm of all the vehicles .
  elif (chart_id == 7) :
    data = Cummulative_record.query.with_entities(Cummulative_record.avg_erpm)
    value_list = [['avg_erpm','value']]
    for datas in data :
      value_list.append(['avg_erpm', datas.avg_erpm])
    clear_mappers();
    return jsonify(value_list)
  #chart_id == 8 will return average throttle position
  elif (chart_id == 8) :
    data = Cummulative_record.query.with_entities(Cummulative_record.avg_throttle_position)
    value_list = [['avg_throttle_position','value']]
    for datas in data :
      value_list.append(['avg_throttle_position', datas.avg_throttle_position])
    clear_mappers();
    return jsonify(value_list)
  #chart_id == 9 will return average speed for all the vehicles
  elif (chart_id == 9) :
    data = Cummulative_record.query.with_entities(Cummulative_record.avg_speed)
    value_list = [['avg_speed','value']]
    for datas in data :
      value_list.append(['avg_speed', datas.avg_speed])
    clear_mappers();
    return jsonify(value_list)

  else :
    return ("Chart not found")


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
  #Chart_id == 3 will return erpm and vehicle_speed data. It will be used to plot erpm vs vehicle_speed 
  elif (chart_id == 3):
    data = Device.query.all();
    value_list = [['erpm','vehicle_speed']]
    for datas in data :
      value_list.append([datas.erpm, datas.vehicle_speed])
    clear_mappers();
    return jsonify(value_list)
  #chart_id  == 4 returns erpm vs throttle_position data in the required format
  elif (chart_id == 4):
    data = Device.query.all();
    value_list = [['erpm','throttle_position']]
    for datas in data :
      value_list.append([datas.erpm, datas.throttle_position])
    clear_mappers();
    return jsonify(value_list)
  #chart_id == 5 returns raw erpm data for a particular device. It can be used to predict the erpm of vehicle at any given instant with significant probability
  elif (chart_id == 5):
    data = Device.query.with_entities(Device.erpm)
    value_list = [['erpm','value']]
    for datas in data :
      value_list.append(['erpm', datas.erpm])
    clear_mappers();
    return jsonify(value_list)
  #chart_id == 6 returns raw throttle_position for a particular device. Can be used for same as mentioned above
  elif (chart_id == 6):
    data = Device.query.with_entities(Device.throttle_position);
    value_list = [['throttle_position','value']]
    for datas in data :
      value_list.append(['throttle_position', datas.throttle_position])
    clear_mappers();
    return jsonify(value_list)
  #chart_id == 7 returns raw engine_load for a particular device. Can be used as mentioned above
  elif (chart_id == 7):
    data = Device.query.with_entities(Device.engine_load);
    value_list = [['engine_load','value']]
    for datas in data :
      value_list.append(['engine_load', datas.engine_load])
    clear_mappers();
    return jsonify(value_list)

  else :
    return ('Chart Id Not Found')