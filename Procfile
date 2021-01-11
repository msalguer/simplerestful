release: wget -O Chinook_Sqlite.sqlite https://github.com/lerocha/chinook-database/blob/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite?raw=true
web: gunicorn -b 0.0.0.0:$PORT app:app
