from myproject import app
from flask import Flask, flash, jsonify
from flask import render_template, request, send_from_directory, json
from database import db_session, metadata
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import mapper, clear_mappers
from flask_sqlalchemy import SQLAlchemy
from myproject.data import Device, deviceNumbers, list_trip_check, Device_derived, FMT
from datetime import timedelta
##### FOR SAVING DATA FROM THE DEVICE ######


@app.route('/new', methods = ['POST'])
def new():
  if request.method == 'POST' :
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
        throttle_position = request.form['throttle_position']
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
        
        clear_mappers();
        devices = Table("device"+table_name, metadata,autoload= True
        )
        mapper(Device, devices)

        devices_derived = Table("device_derived"+table_name, metadata,autoload=True
        )
        mapper(Device_derived, devices_derived)


        device = Device(erpm,engine_load,runtime_crank,throttle_position, latitude,longitude,vehicle_speed,final_date,final_time)
        table_name = int(table_name)
        runtime_crank = int(runtime_crank)
        erpm = int(erpm)
        engine_load = int(engine_load)
        throttle_position = int(throttle_position)
        vehicle_speed = int(vehicle_speed)
        print(list_trip_check[table_name-1]['last_runtime_crank'] == -1)

        if ((list_trip_check[table_name-1]['last_runtime_crank'] > runtime_crank) or (runtime_crank == 0) or (list_trip_check[table_name - 1]['last_runtime_crank'] == -1)):
            
            if (list_trip_check[table_name-1]['trip_update']) :
                #duration = datetime.strptime(list_trip_check[table_name-1]['trip_start_time'], FMT) - datetime.strptime(list_trip_check[table_name-1]['last_trip_time'], FMT)
                duration = timedelta(seconds = list_trip_check[table_name-1]['last_runtime_crank'])
                trip_duration = str(duration)
                trip_distance = list_trip_check[table_name-1]['avg_speed'] * duration.total_seconds() / 3600
                trip_avg_speed = list_trip_check[table_name-1]['avg_speed']
                trip_avg_erpm = list_trip_check[table_name-1]['avg_erpm']
                trip_avg_engine_load = list_trip_check[table_name-1]['avg_engine_load']
                trip_avg_throttle_position = list_trip_check[table_name-1]['avg_throttle_position']
                trip_date = list_trip_check[table_name-1]['last_trip_date']
                trip_end_time = list_trip_check[table_name-1]['last_trip_time']
                device_derived = Device_derived(trip_duration, trip_distance, trip_avg_speed, trip_avg_erpm, trip_avg_engine_load, trip_avg_throttle_position, trip_date, trip_end_time)
                db_session.add(device_derived)

            list_trip_check[table_name-1]['trip_update'] = True

            list_trip_check[table_name-1]['trip_start_time'] = hh+':'+mm+':'+ss
            list_trip_check[table_name-1]['count'] = 0
            list_trip_check[table_name-1]['avg_speed'] = 0
            list_trip_check[table_name-1]['avg_erpm'] = 0
            list_trip_check[table_name-1]['avg_engine_load'] = 0
            list_trip_check[table_name-1]['avg_throttle_position'] = 0
            # record starting time
            # restore count

        # if old general data
        list_trip_check[table_name-1]['last_trip_time'] = hh+':'+mm+':'+ss
        list_trip_check[table_name-1]['last_trip_date'] = final_date
        list_trip_check[table_name-1]['count'] = list_trip_check[table_name-1]['count']+1
        list_trip_check[table_name-1]['avg_speed'] = float(list_trip_check[table_name-1]['avg_speed'] * (list_trip_check[table_name-1]['count'] - 1) + vehicle_speed) / list_trip_check[table_name-1]['count']
        list_trip_check[table_name-1]['avg_erpm'] = float(list_trip_check[table_name-1]['avg_erpm'] * (list_trip_check[table_name-1]['count'] - 1) + erpm) / list_trip_check[table_name-1]['count']
        list_trip_check[table_name-1]['avg_engine_load'] = float(list_trip_check[table_name-1]['avg_engine_load'] * (list_trip_check[table_name-1]['count'] - 1) + engine_load) / list_trip_check[table_name-1]['count']
        list_trip_check[table_name-1]['avg_throttle_position'] = float(list_trip_check[table_name-1]['avg_throttle_position'] * (list_trip_check[table_name-1]['count'] - 1) + throttle_position) / list_trip_check[table_name-1]['count']
        list_trip_check[table_name-1]['last_runtime_crank'] = runtime_crank
        

        db_session.add(device)
        db_session.commit()
        clear_mappers();
        return ('added successfully')
  return ('Yooo')

