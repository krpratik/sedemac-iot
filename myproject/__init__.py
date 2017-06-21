#Main application file. The routes are imported from views, data and record accordingly. 
from flask import Flask
app = Flask(__name__, static_folder='/static')
#Route methods are imported below
import myproject.views
import myproject.record
import myproject.data

if __name__ == "__main__":
<<<<<<< HEAD
    app.run(host='0.0.0.0',debug = True)

=======
    app.run(host='0.0.0.0')
>>>>>>> fc1918ef998dc1d132be65cb03be19ad3e1a18d8
