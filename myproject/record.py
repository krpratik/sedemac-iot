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
from myproject.data import Device, deviceNumbers, Device_derived, FMT, Cummulative_record, Last_data
#Modules required for dealing with date and time type variables
from datetime import timedelta, datetime

##### FOR SAVING DATA FROM THE DEVICE #######
#Few basic variable initialization to be performed.
#Raw data is directly stored in the database. 
#For updating the seconday table when trips end, we keep taking running average of the curremt raw data.
#This running average is store in a a dictionary of python('trip_check_1' for device 1). 
#Each device has it's own dictionary trip_check_devicenumnber. list_trip_check is a list which contains all the dicts as list

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
        request_form = {'table_name':'', 'data_date':'', 'data_time':'', 'latitude':'', 'longitude':'', 'altitude':'', 'engine_load':'', 'erpm':'', 'vehicle_speed':'', 'runtime_crank':'', 'throttle_position':''}
        trip_check = {'trip_update': False, 'last_runtime_crank': -1, 'last_trip_time': '00:00:00', 'last_trip_date':'0000-00-00', 'count':0, 'avg_speed':0, 'avg_erpm':0, 'avg_engine_load':0, 'avg_throttle_position':0, 'trip_start_time':0, 'trip_latitude':0, 'trip_longitude':0, 'trip_altitude':0};
        form_list = ['table_name', 'new_data', 'data_date', 'data_time', 'latitude', 'longitude', 'altitude', 'engine_load', 'erpm', 'vehicle_speed', 'runtime_crank', 'throttle_position']
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
        if not(request_form['table_name'] and (request_form['data_date']) and (request_form['data_time']) and (request_form['latitude']) and (request_form['longitude'])) :
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
            latitude = float(request_form['latitude'])/1000000.0
            longitude = float(request_form['longitude'])/1000000.0
            clear_mappers()
            last_data = Table("last_data", metadata, autoload= True
            )
            mapper(Last_data, last_data)
            data_last = Last_data.query.filter(Last_data.device_number == table_name).first()
            trip_check['trip_update']=data_last.trip_update
            trip_check['last_runtime_crank']=data_last.last_runtime_crank
            trip_check['last_trip_time']=data_last.last_trip_time
            trip_check['last_trip_date']=data_last.last_trip_date
            trip_check['count']=data_last.count
            trip_check['avg_speed']=data_last.avg_speed
            trip_check['avg_erpm']=data_last.avg_erpm
            trip_check['avg_engine_load']=data_last.avg_engine_load
            trip_check['avg_throttle_position']=data_last.avg_throttle_position
            trip_check['trip_start_time'] = data_last.trip_start_time
            trip_check['trip_latitude']= data_last.trip_latitude
            trip_check['trip_longitude']=data_last.trip_longitude
            trip_check['trip_altitude']= data_last.trip_altitude
        else :
            return ('Device not registered to database')

        if (not new_data) :
            if not(request_form['altitude'] and request_form['erpm'] and request_form['vehicle_speed'] and request_form['throttle_position'] and request_form['runtime_crank'] and request_form['engine_load'] and request_form['table_name'] and (request_form['table_name']>0) ) :
                #flash('Please enter all the fields', 'error')
                return ("Empty attempt : Please send all the parameters")
            else :
                altitude = request_form['altitude']
                table_name = request_form['table_name']
                erpm = request_form['erpm']
                engine_load = request_form['engine_load']
                runtime_crank = request_form['runtime_crank']
                throttle_position = request_form['throttle_position']
                vehicle_speed = request_form['vehicle_speed']
                #clear_mappers();
                devices = Table("device"+table_name, metadata,autoload= True
                )
                mapper(Device, devices)

                device = Device(erpm,engine_load,runtime_crank,throttle_position, latitude, longitude, altitude, vehicle_speed,final_date,final_time)
                db_session.add(device)

                table_name = int(table_name)
                runtime_crank = int(runtime_crank)
                erpm = int(erpm)
                engine_load = int(engine_load)
                throttle_position = int(throttle_position)
                vehicle_speed = int(vehicle_speed)

                if (trip_check['trip_latitude'] == 0) :
                    trip_check['trip_latitude'] = float(latitude)
                    data_last.trip_latitude  = float(latitude)

                if (trip_check['trip_longitude'] == 0):
                    trip_check['trip_longitude'] = float(longitude)
                    data_last.trip_longitude = float(longitude)

                if (trip_check['last_trip_date'] == '1111-11-11') :
                    trip_check['last_trip_date'] = final_date
                    data_last.last_trip_date = final_date

                if (trip_check['trip_altitude'] == 0):
                    trip_check['trip_altitude'] = float(altitude)
                    data_last.trip_altitude = float(altitude)

                # if old general data
                data_last.last_trip_time = hh+':'+mm+':'+ss
                data_last.count = trip_check['count']+1
                data_last.avg_speed = float(trip_check['avg_speed'] * (trip_check['count']) + vehicle_speed) / (trip_check['count'] + 1)
                data_last.avg_erpm = float(trip_check['avg_erpm'] * (trip_check['count']) + erpm) / (trip_check['count'] + 1)
                data_last.avg_engine_load = float(trip_check['avg_engine_load'] * (trip_check['count']) + engine_load) / (trip_check['count'] + 1)
                data_last.avg_throttle_position = float(trip_check['avg_throttle_position'] * (trip_check['count']) + throttle_position) / (trip_check['count'] + 1)
                data_last.last_runtime_crank = runtime_crank

                db_session.commit()
                clear_mappers()
        else :
            if (trip_check['trip_update'] and (trip_check['last_runtime_crank'] != -1)) :
                #clear_mappers()
                devices_derived = Table("device_derived"+str(table_name), metadata,autoload=True
                )
                mapper(Device_derived, devices_derived)
                #duration = datetime.strptime(trip_check['trip_start_time'], FMT) - datetime.strptime(trip_check['last_trip_time'], FMT)
                duration = timedelta(seconds = trip_check['last_runtime_crank'])
                trip_duration = str(duration)
                trip_distance = trip_check['avg_speed'] * duration.total_seconds() / 3600
                trip_avg_speed =trip_check['avg_speed']
                trip_avg_erpm = trip_check['avg_erpm']
                trip_avg_engine_load = trip_check['avg_engine_load']
                trip_avg_throttle_position = trip_check['avg_throttle_position']
                trip_date = trip_check['last_trip_date']
                trip_end_time = trip_check['last_trip_time']
                trip_latitude = trip_check['trip_latitude']
                trip_longitude = trip_check['trip_longitude']
                trip_altitude = trip_check['trip_altitude']
                trip_start_time = trip_check['trip_start_time']

                device_derived = Device_derived(trip_duration, trip_distance, trip_avg_speed, trip_avg_erpm, trip_avg_engine_load, trip_avg_throttle_position, trip_date, trip_end_time, trip_start_time, trip_latitude, trip_longitude, trip_altitude)
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

            data_last.trip_update = int(True)
            data_last.trip_start_time = hh+':'+mm+':'+ss
            data_last.trip_latitude = latitude
            data_last.trip_longitude = longitude
            data_last.trip_altitude = 0
            data_last.last_trip_date = final_date
            data_last.count = 0
            data_last.avg_speed = 0
            data_last.avg_erpm = 0
            data_last.avg_engine_load = 0
            data_last.avg_throttle_position = 0
            data_last.last_runtime_crank = -1
            db_session.commit()
            clear_mappers()
            # record starting time
            # restore count
        return ('added successfully')
    return('Yooo : Method is not POST')