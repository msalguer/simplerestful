#*****************************************************************
# SIMPLE RESTFUL - RESTFUL API by SoftwareSimple
# At the moment, is a RESful API with SQLite databases. Built for developers, for testing frontend code.
# 0.5 Beta version              
# Developed by: Manuel Salguero Castell
# https://softwaresimple.es
# https://msalguero.com.es
# https://twitter.com/msalguer
# https://github.com/msalguer/simplerestful      
# MIT License                                 
# Copyright 2021 - Manuel Salguero Castell
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#*****************************************************************

from flask import Flask, escape, request, jsonify, make_response
import sqlite3
import time
import datetime
import random
import os.path
import wget

app = Flask(__name__)

#For resolve Heroku SQLite problem
def firstconn():
    databasefile='Chinook_Sqlite.sqlite'
    wget.download('https://github.com/lerocha/chinook-database/blob/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite?raw=true')
    conn = sqlite3.connect(databasefile)
    dbmem = sqlite3.connect(':memory:',check_same_thread=False)
    conn.backup(dbmem)
    return dbmem
dbmem=firstconn()

#+++++++++++++++++++++++++++++++++ SQLite connection method +++++++++++++++++++++++++++++++++++
bbdd="SQLite"
def getconn(dbmem):
    #For resolve Heroku SQLite problem
    try:
        c = dbmem.cursor()
    except:
        dbmem=firstconn()
    conn=dbmem    
    #databasefile='Chinook_Sqlite.sqlite'
    #conn = sqlite3.connect(databasefile)
    return conn

#+++++++++++++++++++++++++++++++++++++++++ API METHOD ++++++++++++++++++++++++++++++++++++++++++
@app.route('/',methods=['GET'])
@app.route('/api',methods=['GET'])
def api():
    #Get DB cursor
    conn=getconn(dbmem)
    c = conn.cursor()

    #Get all tablenames 
    c.execute("SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';")
    datas=c.fetchall()
    tablenames=[]
    for data in datas:
        tablenames.append("".join(map(str,data)))

    print(tablenames)
    
    res='SIMPLE RESTFUL - RESTFUL API by SoftwareSimple<br>'+'<br>'
    res+="For development purposes."+'<br><br>'
    res+="Developed by: Manuel Salguero Castell"+'<br>'
    res+="MIT License" +'<br>'
    res+="Copyright 2021 - Manuel Salguero Castell"+'<br>'
    res+="_____________________________<br>"
    res+= '<br>'
    for tablename in tablenames:
        res+= tablename.upper()+'<br>'
        res+=''.ljust(len(tablename), '-')+'<br>'
        res+= "GET list method: "+request.url_root+tablename+'<br>'
        res+= "GET ID method: "+request.url_root+tablename+'/id''<br>'
        res+= "POST method (Insert): "+request.url_root+tablename+ ' => With JSON field-value data'+'<br>'
        res+= "PUT method (Update): "+request.url_root+tablename+'/id => With JSON field-value data'+'<br>'
        res+= "DELETE method: "+request.url_root+tablename+'/id'+'<br>'
        res+= '<br>'

    return res

#++++++++++++++++++++++++++++++++++++++++ FAVICON ROUTE (Ignore at the moment) ++++++++++++++++++++++++++
@app.route('/favicon.ico')
def favicon():
    return '' #send_from_directory(os.path.join(app.root_path, 'static'),
              #                 'favicon.ico', mimetype='image/vnd.microsoft.icon')

#+++++++++++++++++++++++++++++++++++++++++ GET LIST METHOD ++++++++++++++++++++++++++++++++++++++++++
@app.route('/<table>',methods=['GET'])
def getlist(table=None, id=None): 
    #Get DB cursor
    conn=getconn(dbmem)
    c = conn.cursor()

    #SELECT - GET ROW LIST
    c.execute(f'SELECT * FROM {escape(table)}')
    data=c.fetchall()
    print(data)
    
    #RESPONSE
    res = make_response(jsonify(data), 200)
    return res

#+++++++++++++++++++++++++++++++++++++++++ GET ROW METHOD ++++++++++++++++++++++++++++++++++++++++++
@app.route('/<table>/<id>',methods=['GET'])
def getid(table=None, id=None): 
    #Get DB cursor
    conn=getconn(dbmem)
    c = conn.cursor()

    #Get ID field name 
    c.execute(f'SELECT name FROM pragma_table_info(\'{escape(table)}\') LIMIT 1')
    data=c.fetchall()
    idfield="".join(map(str,data[0]))

    #SELECT - GET ROW
    c.execute(f'SELECT * FROM {escape(table)} WHERE {idfield}={escape(id)}')
    data = c.fetchall()
    print(data)

    res = make_response(jsonify(data), 200)
    return res

#+++++++++++++++++++++++++++++++++++++++++ POST METHOD ++++++++++++++++++++++++++++++++++++++++++
@app.route('/<table>', methods=['POST'])
def addrow(table=None):
    #Get DB cursor
    conn=getconn(dbmem)
    c = conn.cursor()

    #Only processed if receive POST with JSON format
    if request.is_json:
        req = request.get_json()
        vals=[]
        fids=[]
        values=''
        for key,value in req.items():
            fids.append(escape(key))
            vals.append(escape(value))

        #If BBDD is SQlite, ID autonumeric are computed (if proceed)
        idnext=0
        if (bbdd=='SQLite'):

            #Get ID field name on first column table
            c.execute(f'SELECT name FROM pragma_table_info(\'{escape(table)}\') LIMIT 1')
            data=c.fetchall()
            idfield="".join(map(str,data[0]))

            #Search ID field name in field names received
            try:
               index=fids.index(idfield)
            except:
                index=-1

            #Only if exists field name in JSON received, its replaced with computed
            if index!=-1:
                #Compute next ID
                c = conn.cursor()
                c.execute(f'SELECT MAX({idfield}) FROM {escape(table)}')
                data=c.fetchall()
                idnext=int("".join(map(str,data[0])))+1
                #Search index
                index=fids.index(idfield)
                #Replace value
                vals[index]=idnext

        #Convert list to comma separated text, with quotes in values
        values=''
        for val in vals:
            values=values+'"'+str(val)+'",'
        if len(val)>0:
            values=values[0:-1]

        #Convert list to comma separated text, without quotes in name fields
        fields= ','.join(map(str, fids))
        
        print(fields)
        print(values)

        #INSERT NEW ROW
        c.execute(f'INSERT INTO {escape(table)} ({fields}) VALUES ({values})')
        conn.commit()

        #Get last ID created (for check)
        c.execute(f'SELECT MAX({idfield}) FROM {escape(table)}')
        data=c.fetchall()
        id="".join(map(str,data[0]))

        #RESPONSE
        response_body = {
            "result": "OK",
            "message": f"Row created. {idfield}:{id}"
        }
        res = make_response(jsonify(response_body), 200)
        return res
    else:
        return make_response(jsonify({
            "result": "Error",
            "message": "Request body must be JSON"
        }), 400)

#+++++++++++++++++++++++++++++++++++++++++ PUT METHOD ++++++++++++++++++++++++++++++++++++++++++
@app.route('/<table>/<id>', methods=['PUT'])
def modifyrow(table=None, id=None): 
    #Get DB cursor
    conn=getconn(dbmem)
    c = conn.cursor()

    #Get ID fieldname (first field of table)
    c.execute(f'SELECT name FROM pragma_table_info(\'{escape(table)}\') LIMIT 1')
    data=c.fetchall()
    idfield="".join(map(str,data[0]))   
    
    #Check if row exists
    c.execute(f'SELECT * FROM {escape(table)} WHERE {idfield}={escape(id)}')
    data = c.fetchall()
    if not data:
    #RESPONSE AND EXIT
        response_body = {
            "result": "Error",
            "message": f"{idfield} not found: {escape(id)}"
        }
        res = make_response(jsonify(response_body), 200)
        return res
    
    #Only processed if receive PUT with JSON format
    if request.is_json:
        req = request.get_json()
        values=[]
        fields=[]
        for key,value in req.items():
            fields.append(escape(key))
            values.append(escape(value))
        
        # Build SET for update
        update=''
        i=0
        for field in fields:
            if update!='':
                update+=", "
            update+=field+"='"+str(values[i])+"'"
            i+=1
        print (update)

        #UPDATE ROW
        c.execute(f'UPDATE {escape(table)} SET {update} WHERE {idfield}={escape(id)}')
        conn.commit()

        #RESPONSE
        response_body = {
            "result": "OK",
            "message": f"Row modified. {idfield}:{escape(id)}"
        }
        res = make_response(jsonify(response_body), 200)
        return res
    else:
        return make_response(jsonify({
            "result": "Error",
            "message": "Request body must be JSON"
        }), 400)

#++++++++++++++++++++++++++++++++ DELETE METHOD ++++++++++++++++++++++++++++++++
@app.route('/<table>/<id>', methods=['DELETE'])
def deleterow(table=None, id=None): 
    #Get DB cursor
    conn=getconn(dbmem)
    c = conn.cursor()

    #Get ID fieldname (first field of table)
    c.execute(f'SELECT name FROM pragma_table_info(\'{escape(table)}\') LIMIT 1')
    data=c.fetchall()
    idfield="".join(map(str,data[0]))

    #Check if row exists
    c.execute(f'SELECT * FROM {escape(table)} WHERE {idfield}={escape(id)}')
    data = c.fetchall()
    if not data:
        #RESPONSE AND EXIT
        response_body = {
            "result": "Error",
            "message": f"{idfield} not found: {escape(id)}"
        }
        res = make_response(jsonify(response_body), 200)
        return res

    #DELETE
    c.execute(f'DELETE FROM {escape(table)} WHERE {idfield}={escape(id)}')
    conn.commit()

    #RESPONSE
    response_body = {
        "result": "OK",
        "message": f"Row deleted: {escape(id)}"
    }
    res = make_response(jsonify(response_body), 200)
    return res
