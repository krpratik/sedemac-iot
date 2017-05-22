# sedemac-iot
### Follow these steps to install sedemac-iot on your ubuntu

* Move inside the cloned directory and type in your terminal "$ sudo pip install -e ." and press enter
* Then type in your terminal "$ postgres-shell" and press enter
* Then type in your terminal "$ myproject-shell"
* Then type in your terminal "$ export FLASK_APP=myproject"
* Then type in your terminal "$ export FLASK_DEBUG=true"
* Then type in your terminal "$ flask run" to start the server 

This will start your flask server without nginx or apache. It will by default create two tables for two devices named as device1 and device2
