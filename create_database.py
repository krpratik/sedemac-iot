#to run pgadmin use python lib/python2.7/site-packages/pgadmin4/pgAdmin4.py

from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

deviceNumbers = 2;

if __name__=="__main__":

  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///xyzdb'
  db = SQLAlchemy(app)

  for device in range(1,deviceNumbers+1) :
    class Device(db.Model):
      __tablename__= "device"+str(device)
      id = db.Column(db.Integer, primary_key = True)
      erpm = db.Column(db.Integer)
      engine_load = db.Column(db.Integer)
      runtime_crank = db.Column(db.Integer)
      throttle_position = db.Column(db.Integer)
      latitude = db.Column(db.Numeric)
      longitude = db.Column(db.Numeric)
      vehicle_speed = db.Column(db.Integer)
      data_date = db.Column(db.Date)
      data_time = db.Column(db.Time)

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

    class Device_derived(db.Model) :
      __tablename__ = "device_derived"+str(device)
      id = db.Column(db.Integer, primary_key = True)
      trip_duration = db.Column(db.Time)
      trip_distance = db.Column(db.Numeric)
      trip_avg_speed = db.Column(db.Numeric)
      trip_avg_erpm = db.Column(db.Numeric)
      trip_avg_engine_load = db.Column(db.Numeric)
      trip_avg_throttle_position = db.Column(db.Numeric)
      trip_date = db.Column(db.Date)
      trip_end_time = db.Column(db.Time)

      def __init__(self, trip_duration, trip_distance, trip_avg_speed, trip_avg_erpm, trip_avg_engine_load, trip_avg_throttle_position, trip_date, trip_end_time):
        self.trip_duration = trip_duration
        self.trip_distance = trip_distance
        self.trip_avg_speed = trip_avg_speed
        self.trip_avg_erpm = trip_avg_erpm
        self.trip_avg_engine_load = trip_avg_engine_load
        self.trip_avg_throttle_position = trip_avg_throttle_position
        self.trip_date = trip_date
        self.trip_end_time = trip_end_time

  db.create_all();


