#Main application file. The routes are imported from views, data and record accordingly. 
from flask import Flask
app = Flask(__name__, static_folder='/static')
#Route methods are imported below
import myproject.views
import myproject.record
import myproject.data
import logging 
logging.basicConfig(filename='./error.log', level=logging.DEBUG)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
