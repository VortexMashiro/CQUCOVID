#This will run the server with following configuration. 
#To boot the server with default configuration, use `flask run`.
from cqu_covid import app

app.run(debug=True)