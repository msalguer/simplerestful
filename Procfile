release: wget -O Chinook_Sqlite.sqlite https://github.com/lerocha/chinook-database/blob/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite?raw=true
release: chown dyno:dyno Chinook_Sqlite.sqlite
release: chmod 755 Chinook_Sqlite.sqlite
web: gunicorn -b 0.0.0.0:$PORT app:app
