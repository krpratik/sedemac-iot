#to run pgadmin use python lib/python2.7/site-packages/pgadmin4/pgAdmin4.py
#python code to create tables in database in required format

from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgresql:///xyzdb', convert_unicode=True)
metadata = MetaData(bind=engine)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=True,
                                         bind=engine))
deviceNumbers = 2;

if __name__=="__main__":

  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///xyzdb'
  db = SQLAlchemy(app)

  class Last_data(db.Model) :
    __tablename__="last_data"
    id = db.Column(db.Integer, primary_key = True)
    device_number = db.Column(db.Integer)
    trip_update= db.Column(db.Integer)
    last_runtime_crank= db.Column(db.Integer)
    last_trip_time= db.Column(db.Time)
    last_trip_date= db.Column(db.Date)
    count= db.Column(db.Integer)
    avg_speed= db.Column(db.Float)
    avg_erpm= db.Column(db.Float)
    avg_engine_load= db.Column(db.Float)
    avg_throttle_position= db.Column(db.Float)
    trip_start_time=db.Column(db.Time)
    trip_latitude = db.Column(db.Float)
    trip_longitude = db.Column(db.Float)
    trip_altitude = db.Column(db.Float)

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

  class cummulative_record(db.Model) :
    __tablename__="cummulative_record"
    id = db.Column(db.Integer, primary_key = True)
    device_number = db.Column(db.Integer)
    device_name = db.Column(db.String(50))
    trips_number = db.Column(db.Integer)
    trips_avg_duration = db.Column(db.Time)
    trips_avg_distance = db.Column(db.Integer)
    trips_avg_engine_load = db.Column(db.Integer)
    trips_avg_erpm = db.Column(db.Integer)
    trips_avg_throttle_position = db.Column(db.Integer)
    trips_avg_speed = db.Column(db.Integer)
    avg_engine_load = db.Column(db.Integer)
    avg_erpm = db.Column(db.Integer)
    avg_throttle_position = db.Column(db.Integer)
    avg_speed = db.Column(db.Integer)
    trips_total_distance = db.Column(db.Integer)
    trips_total_duration = db.Column(db.Time)

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


  for device in range(1,deviceNumbers+1) :
    Cummulative_record = cummulative_record(device, "device_"+str(device), 0,'00:00:00', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,'00:00:00')
    db_session.add(Cummulative_record)
    last_Data = Last_data(device, 0, -1, '00:00:00', '2000-01-01', 0, 0, 0, 0, 0, '00:00:00',0 , 0, 0)
    db_session.add(last_Data)
    class Device(db.Model):
      __tablename__= "device"+str(device)
      id = db.Column(db.Integer, primary_key = True)
      erpm = db.Column(db.Integer)
      engine_load = db.Column(db.Integer)
      runtime_crank = db.Column(db.Integer)
      throttle_position = db.Column(db.Integer)
      latitude = db.Column(db.Numeric)
      longitude = db.Column(db.Numeric)
      altitude = db.Column(db.Numeric)
      vehicle_speed = db.Column(db.Integer)
      data_date = db.Column(db.Date)
      data_time = db.Column(db.Time)

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
      trip_start_time = db.Column(db.Time)
      trip_latitude = db.Column(db.Float)
      trip_longitude = db.Column(db.Float)
      trip_altitude = db.Column(db.Float)


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

  db.create_all();
  db_session.commit();


