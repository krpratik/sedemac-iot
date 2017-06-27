# sedemac-iot
### Follow these steps to install sedemac-iot on your ubuntu

* Move inside the cloned directory and type in your terminal "$ sudo pip install -e ." and press enter
* Then type in your terminal "$ postgres-shell" and press enter
* Then type in your terminal "$ myproject-shell"
* Then type in your terminal "$ export FLASK_APP=myproject"
* Then type in your terminal "$ export FLASK_DEBUG=true"
* Then type in your terminal "$ flask run" to start the server 

This will start your flask server without nginx or apache. It will by default create two tables for four devices named as device1 ,device2 and so on. 
You will have to export these variables (FLASK_APP and FLASK_DEBUG) everytime before you run the server. 
If you want to export these variables permanently then type in your terminal "$ nano /etc/environment" .
And add lines "export FLASK_APP=myproject" and "export FLASK_DEBUG=true" in /etc/environment file.
Then Refresh your environment variables by typing "$ source /etc/environment" in your terminal. Now you can run your server without exporting variables everytime.  
