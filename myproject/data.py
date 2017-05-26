from myproject import app
from flask import Flask, flash, jsonify
from flask import render_template, request, send_from_directory, json
from database import db_session, metadata
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import mapper, clear_mappers
from flask_sqlalchemy import SQLAlchemy

deviceNumbers = 2 ;
class Device(object):
  query = db_session.query_property()
  def __init__(self, erpm, engine_load,latitude,longitude,vehicle_speed,data_date,data_time):
    self.erpm = erpm
    self.engine_load = engine_load
    self.latitude = latitude
    self.longitude = longitude
    self.vehicle_speed = vehicle_speed
    self.data_date = data_date
    self.data_time = data_time


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
    value_list=[{'key':1,'values':[]}]
    for datas in data :
      value_list[0]['values'].append({'x': datas.erpm , 'y': int(datas.engine_load), 'size':0.5, 'shape':'circle'})
    clear_mappers();
    return  jsonify(value_list)

  elif (chart_id == 2):
    data = Device.query.with_entities(Device.vehicle_speed)
    value_list = [['s','value']]
    for datas in data :
      value_list.append(['s',datas.vehicle_speed])
    clear_mappers();
    return jsonify(value_list)

