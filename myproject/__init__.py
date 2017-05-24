from flask import Flask
app = Flask(__name__, static_folder='/static')

import myproject.views
import myproject.record
import myproject.data


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug = True)
