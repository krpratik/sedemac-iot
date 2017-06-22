from myproject import app
import logging
logHandler = logging.FileHandler('./sedemac_iot_error.log')
logHandler.setLevel(logging.DEBUG)
app.logger.addHandler(logHandler)
app.logger.setLevel(logging.DEBUG)
if __name__ == "__main__":
    app.run()