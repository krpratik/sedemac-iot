#views.py contains API endpoints to serve the frontend pages for the website
#As the name itself suggests it delas with aesthetic part of the frontend
#The instance of app is imported from __init__.py
from myproject import app
from flask import Flask, flash, jsonify
from flask import render_template, request, send_from_directory, json

#API endpoint (route) for rendering the first page of the frontend website
@app.route("/")
def index():
    return render_template('index.html')

#API endpoint for individual tracking of a particular vehicle
@app.route("/track")
def track():
    return render_template('track.html')

#API endpoint to load charts
@app.route("/charts")
def charts():
    return render_template('charts.html')

#API endpoint to track a particular mentioned vehicle 
@app.route('/track/<int:device_id>')
def tracked(device_id):
  return render_template('tracked.html')

#API endpoint to serve static files located on server which are required for frontend
@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('static',path)
