
# SIMPLE RESTFUL -RESTFUL API by SoftwareSimple         
Developed by: Manuel Salguero Castell  

https://softwaresimple.es

https://msalguero.com.es

https://twitter.com/msalguer

https://github.com/msalguer/simplerestful


--------------------------------------------------------

MIT License                                 
Copyright 2021 - Manuel Salguero Castell

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

--------------------------------------------------------

At the moment, is a RESful API with SQLite databases. Built for developers, for testing frontend code.

Gets full Restful methods for all tables on selected SQLite database. Simple. Fast. Only for development purposes. Not includes security.

0.5 Beta version. Functional.

--------------------------------------

Install RESTFUL API by SoftwareSimple, on Ubuntu/ Debian server:

sudo apt install python3

sudo apt install curl

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

python3 get-pip.py

pip --version

pip install Flask

pip install wget

Get the simple RESTFul API application. Select before a folder to install:

wget https://github.com/msalguer/simplerestful/raw/main/app.py && wget https://raw.githubusercontent.com/msalguer/simplerestful/main/app.pyfile

Get SQLite test database.

wget -O Chinook_Sqlite.sqlite https://github.com/lerocha/chinook-database/blob/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite?raw=true

Is possible run with other SQLite database, if change source line that open database
In this case, review and/or change line: conn = sqlite3.connect('Chinook_Sqlite.sqlite')

Execute on localhost(On root app directory):

flask run

Execute on Production mode:

flask run -h 192.168.X.X -> Python Flask IP WebServer

Execute on Production mode with Gunicorn WGSI Server (4 instances) and receive petitions on all ips available on server:

pip install gunicorn
gunicorn -b 0.0.0.0:8000 -w 4 app:app

Open firewall port (if proceed)
http://localhost:8000/api OR IP server

Stop Gunicorn server or Flask server:
CTRL+C

---------
Tested with this versions:

Ubuntu 20.04.1 LTS

Python 3.8.5

Flask 1.1.2

Werkzeug 1.0.1

pip 20.3.3

--------

Trobleshotting:

If has any problem to run Gunicorn server, try:

pkill gunicorn

----------
DEPLOY

HEROKU
I modified code for get SQLite demo database on Python API. Is not necessary download first SQLite database. Now, you can deploy automatically on Heroku. You can test it here:

https://simplerestful.herokuapp.com/

The first request to the API could be slower, if the Heroku instance was asleep.

LOCAL DEPLOY:

Disable the wget line of app.py file, so as not to download the SQLite file for all executions because that file will be repeated on the file system.
