
from myproject import app
from flask import Flask, flash, jsonify
from flask import render_template, request, send_from_directory, json
from database import db_session, metadata
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import mapper, clear_mappers
from flask_sqlalchemy import SQLAlchemy
import json
FMT = "%H:%M:%S"

deviceNumbers = 2 ;
trip_check_1 = {'table_name': 1, 'trip_update': False, 'last_runtime_crank': -1, 'last_trip_time': '00:00:00', 'last_trip_date':'0000-00-00', 'count':0, 'avg_speed':0, 'avg_erpm':0, 'avg_engine_load':0, 'avg_throttle_position':0, 'trip_start_time':0};
trip_check_2 = {'table_name': 2, 'trip_update': False, 'last_runtime_crank': -1, 'last_trip_time': '00:00:00', 'last_trip_date':'0000-00-00', 'count':0, 'avg_speed':0, 'avg_erpm':0, 'avg_engine_load':0, 'avg_throttle_position':0, 'trip_start_time':0};

list_trip_check=[trip_check_1,trip_check_2];

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


class Device_derived(object) :
  def __init__(self, trip_duration, trip_distance, trip_avg_speed, trip_avg_erpm, trip_avg_engine_load, trip_avg_throttle_position, trip_date, trip_end_time):
    self.trip_duration = trip_duration
    self.trip_distance = trip_distance
    self.trip_avg_speed = trip_avg_speed
    self.trip_avg_erpm = trip_avg_erpm
    self.trip_avg_engine_load = trip_avg_engine_load
    self.trip_avg_throttle_position = trip_avg_throttle_position
    self.trip_date = trip_date
    self.trip_end_time = trip_end_time


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/data/<int:device_id>/chart/<int:chart_id>')
def show_all(device_id, chart_id):
  devices = Table("device"+str(device_id), metadata,autoload= True)
  clear_mappers();
  mapper(Device, devices)

  if (chart_id == 1) :

    data = Device.query.all();
    value_list=[['erpm','engine_load']]
    for datas in data :
      value_list.append([datas.erpm, datas.engine_load])
    clear_mappers();
    return  jsonify(value_list)

  elif (chart_id == 2):
    data = Device.query.with_entities(Device.vehicle_speed)
    value_list = [['speed','value']]
    for datas in data :
      value_list.append(['speed',datas.vehicle_speed])
    clear_mappers();
    #return json.dumps(value_list)
    return jsonify(value_list)
