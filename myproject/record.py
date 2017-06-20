#record.py records the raw data sent by the device on-board 
#The request is sent via POST request to the server
#API endpoint to store raw data from vehicles into respective database
from myproject import app
from flask import Flask, jsonify
# SQL related settings and paramneters are imported for SQL transactions
from flask import render_template, request, send_from_directory, json
from database import db_session, metadata
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import mapper, clear_mappers
from flask_sqlalchemy import SQLAlchemy
#Reuired variables are imported from variable store house ('data.py')
from myproject.data import Device, deviceNumbers, Device_derived, FMT, Cummulative_record
#Modules required for dealing with date and time type variables
from datetime import timedelta, datetime

##### FOR SAVING DATA FROM THE DEVICE #######
#Few basic variable initialization to be performed.
#Raw data is directly stored in the database. 
#For updating the seconday table when trips end, we keep taking running average of the curremt raw data.
#This running average is store in a a dictionary of python('trip_check_1' for device 1). 
#Each device has it's own dictionary trip_check_devicenumnber. list_trip_check is a list which contains all the dicts as list

# Initialization of dicts (trip_check) for two devices
trip_check_1 = {'table_name': 1, 'trip_update': False, 'last_runtime_crank': -1, 'last_trip_time': '00:00:00', 'last_trip_date':'0000-00-00', 'count':0, 'avg_speed':0, 'avg_erpm':0, 'avg_engine_load':0, 'avg_throttle_position':0, 'trip_start_time':0};
trip_check_2 = {'table_name': 2, 'trip_update': False, 'last_runtime_crank': -1, 'last_trip_time': '00:00:00', 'last_trip_date':'0000-00-00', 'count':0, 'avg_speed':0, 'avg_erpm':0, 'avg_engine_load':0, 'avg_throttle_position':0, 'trip_start_time':0};

#Intialization of list containing every dict for each device
list_trip_check=[trip_check_1,trip_check_2];

#POST request posts all the data in a string but with comma separated vallues
#We need to parse the string and assign parsed values to respective parameters
#list of parameters to be parsed from from the POST request
Form_list = ['table_name', 'new_data', 'data_date', 'data_time', 'latitude', 'longitude', 'engine_load', 'erpm', 'vehicle_speed', 'runtime_crank', 'throttle_position']

#A dictionary created from POST data with key as parameter's name for easier access of values
Request_form ={'table_name':'', 'data_date':'', 'data_time':'', 'latitude':'', 'longitude':'', 'engine_load':'', 'erpm':'', 'vehicle_speed':'', 'runtime_crank':'', 'throttle_position':''}

#API endpoint to process and store raw data from device installeld onto vehicle
@app.route('/new', methods = ['POST'])
def new():
    if request.method == 'POST' :
        request_form = Request_form
        form_list = Form_list
        #Storing the string posted via POST request method in variable
        data_string = request.form['d']
        #parsing the string as it contains ',' (comma) separated values and stroing it in a list
        data = data_string.split(',')
        #Iterating over the list and assigning values to respective key in request_form dictionary
        for i in range(0, len(data)) :
            request_form[form_list[i]] = data[i]
        #Determining whether the data represents the marking of a new trip or the same old trip.
        #new_data == 0 shows old trip and new_data == 1 shows new_trip
        new_data = 0
        if ('new_data' in request_form):
            new_data = int(request_form['new_data'])
        #checking whether the minimum required parameters are present in the received data
        if not(request_form['table_name'] and (request_form['data_date']) and (request_form['data_time'])) :
            #flash('Please enter all the fields', 'error')
            return ("Empty attempt")
        elif (not((int(request_form['table_name']) <= 0) or (int(request_form['table_name']) > deviceNumbers))) :
            data_time = request_form['data_time']
            data_time_str = str(data_time)
            ms = str(int(data_time_str[-2:])*10)
            ss = data_time_str[-4:-2]
            mm = data_time_str[-6:-4]
            hh = data_time_str[:-6]
            final_time = hh+':'+mm+':'+ss+'.'+ms
            data_date = request_form['data_date']
            table_name = int(request_form['table_name'])
            data_date_str = str(data_date)
            year = '20'+data_date_str[-2:]
            month = data_date_str[-4:-2]
            day = data_date_str[:-4]
            final_date = year+'-'+month+'-'+day
        else :
            return ('Device not registered to database')

        if (not new_data) :
            if not(request_form['erpm'] and request_form['runtime_crank'] and request_form['engine_load'] and request_form['table_name'] and (request_form['table_name']>0) ) :
                #flash('Please enter all the fields', 'error')
                return ("Empty attempt : Please send all the parameters")
            else :
                table_name = request_form['table_name']
                erpm = request_form['erpm']
                engine_load = request_form['engine_load']
                runtime_crank = request_form['runtime_crank']
                throttle_position = request_form['throttle_position']
                latitude = request_form['latitude']
                longitude = request_form['longitude']
                vehicle_speed = request_form['vehicle_speed']
                
                clear_mappers();
                devices = Table("device"+table_name, metadata,autoload= True
                )
                mapper(Device, devices)

                device = Device(erpm,engine_load,runtime_crank,throttle_position, latitude,longitude,vehicle_speed,final_date,final_time)
                db_session.add(device)
                db_session.commit()
                clear_mappers()
                
                table_name = int(table_name)
                runtime_crank = int(runtime_crank)
                erpm = int(erpm)
                engine_load = int(engine_load)
                throttle_position = int(throttle_position)
                vehicle_speed = int(vehicle_speed)

                # if old general data
                list_trip_check[table_name-1]['last_trip_time'] = hh+':'+mm+':'+ss
                list_trip_check[table_name-1]['last_trip_date'] = final_date
                list_trip_check[table_name-1]['count'] = list_trip_check[table_name-1]['count']+1
                list_trip_check[table_name-1]['avg_speed'] = float(list_trip_check[table_name-1]['avg_speed'] * (list_trip_check[table_name-1]['count'] - 1) + vehicle_speed) / list_trip_check[table_name-1]['count']
                list_trip_check[table_name-1]['avg_erpm'] = float(list_trip_check[table_name-1]['avg_erpm'] * (list_trip_check[table_name-1]['count'] - 1) + erpm) / list_trip_check[table_name-1]['count']
                list_trip_check[table_name-1]['avg_engine_load'] = float(list_trip_check[table_name-1]['avg_engine_load'] * (list_trip_check[table_name-1]['count'] - 1) + engine_load) / list_trip_check[table_name-1]['count']
                list_trip_check[table_name-1]['avg_throttle_position'] = float(list_trip_check[table_name-1]['avg_throttle_position'] * (list_trip_check[table_name-1]['count'] - 1) + throttle_position) / list_trip_check[table_name-1]['count']
                list_trip_check[table_name-1]['last_runtime_crank'] = runtime_crank

        else :

            if (list_trip_check[table_name-1]['trip_update'] and (list_trip_check[table_name-1]['last_runtime_crank'] != -1)) :
                clear_mappers()
                devices_derived = Table("device_derived"+str(table_name), metadata,autoload=True
                )
                mapper(Device_derived, devices_derived)
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

                cummulative_Record = Table("cummulative_record", metadata, autoload=True
                )
                mapper(Cummulative_record, cummulative_Record)
                data = Cummulative_record.query.filter(Cummulative_record.device_number == table_name).first()
                trips_number = data.trips_number+1
                trips_total_distance = data.trips_total_distance + int(trip_distance)

                last_total_time = datetime.strptime(str(data.trips_total_duration), FMT)
                last_timedelta = timedelta(hours=last_total_time.hour , minutes=last_total_time.minute , seconds=(last_total_time.second))
                updated_total_duration = last_timedelta + duration

                trips_total_duration = str(updated_total_duration)
                trips_avg_duration = str(timedelta(seconds = int(updated_total_duration.total_seconds()/trips_number)))
                trips_avg_distance = int(trips_total_distance/trips_number)
                trips_avg_engine_load = int((data.trips_avg_engine_load*(trips_number-1) + trip_avg_engine_load)/trips_number)
                trips_avg_erpm = int((data.trips_avg_erpm*(trips_number-1) + trip_avg_erpm)/trips_number)
                trips_avg_throttle_position = int((data.trips_avg_throttle_position*(trips_number-1) + trip_avg_throttle_position)/trips_number)
                trips_avg_speed = int((data.trips_avg_speed*(trips_number-1) + trip_avg_speed)/trips_number)
                
                # Coefficient for time weighed Average
                coeff_old = (last_timedelta.total_seconds()/updated_total_duration.total_seconds())
                avg_engine_load = int(data.avg_engine_load * coeff_old + (1-coeff_old)*trip_avg_engine_load)
                avg_erpm = int(data.avg_erpm * coeff_old + (1 - coeff_old)*trip_avg_erpm)
                avg_throttle_position = int(data.avg_throttle_position * coeff_old + (1 - coeff_old)* trip_avg_throttle_position)
                avg_speed = int(data.avg_speed * coeff_old + (1 - coeff_old)* trip_avg_speed)

                data.trips_number = trips_number
                data.trips_total_distance = trips_total_distance
                data.trips_total_duration = trips_total_duration
                data.trips_avg_duration = trips_avg_duration
                data.trips_avg_distance = trips_avg_distance
                data.trips_avg_engine_load = trips_avg_engine_load
                data.trips_avg_erpm = trips_avg_erpm
                data.trips_avg_throttle_position = trips_avg_throttle_position
                data.trips_avg_speed = trips_avg_speed
                data.avg_engine_load = avg_engine_load
                data.avg_erpm = avg_erpm
                data.avg_throttle_position = avg_throttle_position
                data.avg_speed = avg_speed
                db_session.commit()
                clear_mappers()
        
            list_trip_check[table_name-1]['trip_update'] = True
            list_trip_check[table_name-1]['trip_start_time'] = hh+':'+mm+':'+ss
            list_trip_check[table_name-1]['count'] = 0
            list_trip_check[table_name-1]['avg_speed'] = 0
            list_trip_check[table_name-1]['avg_erpm'] = 0
            list_trip_check[table_name-1]['avg_engine_load'] = 0
            list_trip_check[table_name-1]['avg_throttle_position'] = 0
            list_trip_check[table_name-1]['last_runtime_crank'] = -1
            # record starting time
            # restore count
        return ('added successfully')
    return('Yooo : Method is not POST')