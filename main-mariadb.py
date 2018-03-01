#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Copyright 2017 Pier Alberto <pieralbertopierini@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

# Built on OpenSuse Leap 42.3

from BeautifulSoup import BeautifulSoup
import urllib2
import mysql.connector as mariadb
import sys

# Reload sys and encoding to prevent errors
reload(sys)
sys.setdefaultencoding('utf-8')

db = mariadb.connect(host="localhost",      # your host 
                     user="username",       # username to access to mariadb
                     passwd="password",     # password
                     db="database_name")    # name of the database

# Create a Cursor object to execute queries.
cursor = db.cursor()

wiki = "http://en.wikipedia.org/wiki/List_of_districts_of_Costa_Rica"
header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error on Wikipedia
req = urllib2.Request(wiki,headers=header)
page = urllib2.urlopen(req)
soup = BeautifulSoup(page)
 
province = ""
canton = ""
district = ""

table = soup.find("table", { "class" : "wikitable sortable" })
 
for row in table.findAll("tr"):
    cells = row.findAll("td")
    #For each "tr", assign each "td" to a variable.
    if len(cells) == 4:
        try:
            # Insert Provincia
            province = cells[0].find(text=True)
            sql_province = "INSERT INTO Provincia (Provincia) SELECT * FROM (SELECT '%s') AS tmp WHERE NOT EXISTS (SELECT Provincia FROM Provincia WHERE Provincia = '%s') LIMIT 1" %(province, province)
            # Execute the SQL command
            cursor.execute(sql_province)
            # Insert Canton
            canton = cells[1].find(text=True)
            search_provincia_id = "SELECT id FROM Provincia WHERE Provincia = '%s'" %(province)
            cursor.execute(search_provincia_id)
            data_provincia_id = cursor.fetchone()
            provinciaid = data_provincia_id[0]
            sql_canton = "INSERT INTO Cantón (Cantón, ProvinciaID) SELECT * FROM (SELECT '%s', '%s') AS tmp WHERE NOT EXISTS (SELECT Cantón FROM Cantón WHERE Cantón = '%s') LIMIT 1" %(canton, provinciaid, canton)
            # Execute the sql command
            cursor.execute(sql_canton)
            # Insert District
            district = cells[2].find(text=True)
            search_canton_id = "SELECT id FROM Cantón WHERE Cantón = '%s'" %(canton)
            cantonid = cursor.execute(search_canton_id)
            data_canton_id = cursor.fetchone()
            cantonid = data_canton_id[0]
            sql_distrito = "INSERT INTO Distrito (Distrito, CantónID) VALUES ('%s', '%s')" %(district, cantonid)
            # Execute the sql Coammand
            cursor.execute(sql_distrito)
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
# disconect from server
db.close()
