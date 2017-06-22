from myproject import app
import logging 
logging.basicConfig(filename='./error.log', level=logging.DEBUG)

if __name__ == "__main__":
    app.run()