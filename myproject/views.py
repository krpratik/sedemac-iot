from myproject import app
from flask import Flask, flash, jsonify
from flask import render_template, request, send_from_directory, json

# Here n is the number of devices
deviceNumbers = 2 ;

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/track")
def track():
    return render_template('track.html')

@app.route("/charts")
def charts():
    return render_template('charts.html')

@app.route('/track/<int:device_id>')
<<<<<<< HEAD
def tracked(device_id):
  return render_template('tracked.html')
=======
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

>>>>>>> bf6a41ae345cbfdd00213312fa5ee2b16c6529b7

@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('static',path)
