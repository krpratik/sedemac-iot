from myproject import app
from database import db_session, metadata 
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import mapper, clear_mappers
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash, jsonify

# Here n is the number of devices
deviceNumbers = 2 ;

class Device(object):
  query = db_session.query_property()
  def __init__(self, erpm, engine_load):
    self.erpm = erpm
    self.engine_load = engine_load



@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"



@app.route('/track/<int:device_id>')
def show_all(device_id):
  devices = Table("device"+str(device_id), metadata,autoload= True
  )
  clear_mappers();
  mapper(Device, devices)
  data = Device.query.all();
  value_list=[]
  for datas in data :
    value_list.append({'erpm': datas.erpm , 'engine_load': datas.engine_load}) 
  print(value_list)
  return jsonify(results=value_list)
  #return render_template('track.html', jsonify(value = data), len(data))


@app.route('/new', methods = ['POST'])
def new():
  if request.method == 'POST' :
    if not(request.form['erpm'] and request.form['engine_load'] and request.form['table_name'] and (request.form['table_name']>0) ) :
      print ("Reached")
      #flash('Please enter all the fields', 'error')
      return ("Empty attempt")
    else:
      if ((int(request.form['table_name']) <= 0) or (int(request.form['table_name']) > deviceNumbers)) :
        return ('Device not registered to database')
      else :
        erpm = request.form['erpm']
        engine_load = request.form['engine_load']
        table_name = request.form['table_name']
        clear_mappers();
        devices = Table("device"+table_name, metadata,autoload= True
        )
        mapper(Device, devices)
        device = Device(erpm,engine_load)
        db_session.add(device)
        db_session.commit()
        clear_mappers();
        #flash('Record was successfully added')
        return ('added successfully')
  return ('Yooo')


