from myproject import app
from flask import Flask, flash, jsonify
from flask import render_template, request, send_from_directory, json
from database import db_session, metadata
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import mapper, clear_mappers
from flask_sqlalchemy import SQLAlchemy
from myproject.data import Device, deviceNumbers
##### FOR SAVING DATA FROM THE DEVICE ######
@app.route('/new', methods = ['POST'])
def new():
  if request.method == 'POST' :
    print(request.form);
    if not(request.form['erpm'] and request.form['runtime_crank'] and request.form['engine_load'] and request.form['table_name'] and (request.form['table_name']>0) ) :
      #flash('Please enter all the fields', 'error')
      return ("Empty attempt")
    else:
      if ((int(request.form['table_name']) <= 0) or (int(request.form['table_name']) > deviceNumbers)) :
        return ('Device not registered to database')
      else :
        erpm = request.form['erpm']
        engine_load = request.form['engine_load']
        runtime_crank = request.form['runtime_crank']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        vehicle_speed = request.form['vehicle_speed']
        data_date = request.form['data_date']
        data_time = request.form['data_time']
        table_name = request.form['table_name']

        data_date_str = str(data_date)
        year = '20'+data_date_str[-2:]
        month = data_date_str[-4:-2]
        day = data_date_str[:-4]
        final_date = year+'-'+month+'-'+day

        data_time_str = str(data_time)
        ms = str(int(data_time_str[-2:])*10)
        ss = data_time_str[-4:-2]
        mm = data_time_str[-6:-4]
        hh = data_time_str[:-6]
        final_time = hh+':'+mm+':'+ss+'.'+ms
        print(final_time)


        clear_mappers();
        devices = Table("device"+table_name, metadata,autoload= True
        )
        mapper(Device, devices)
        device = Device(erpm,engine_load,runtime_crank,latitude,longitude,vehicle_speed,final_date,final_time)
        db_session.add(device)
        db_session.commit()
        clear_mappers();
        return ('added successfully')
  return ('Yooo')

