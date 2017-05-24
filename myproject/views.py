from myproject import app
from flask import Flask, flash, jsonify
from flask import render_template, request, send_from_directory, json

# Here n is the number of devices

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
def tracked(device_id):
  return render_template('tracked.html')

@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('static',path)
