from myproject import app
from flask import Flask, flash, jsonify
from flask import render_template, request, send_from_directory, json
from database import db_session, metadata
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import mapper, clear_mappers
from flask_sqlalchemy import SQLAlchemy

class Device(object):
  query = db_session.query_property()
  def __init__(self, erpm, engine_load):
    self.erpm = erpm
    self.engine_load = engine_load

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/data/<int:device_id>/chart')
def show_all(device_id):
  devices = Table("device"+str(device_id), metadata,autoload= True)
  clear_mappers();
  mapper(Device, devices)
  data = Device.query.all();
  value_list=[{'key':1,'values':[]}]

  for datas in data :
    value_list[0]['values'].append({'x': datas.erpm , 'y': datas.engine_load, 'size':0.5, 'shape':'circle'})
  clear_mappers();
  return  jsonify(value_list)
