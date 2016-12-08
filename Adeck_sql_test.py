
# coding: utf-8

# ### SQL database Examples ###
# 
# We'll use some basic python to learn about SQL queries, creation and general hygeine.
# 
# First up load basic python libraries we'll use to play with SQL

# In[ ]:

import sqlite3 as sql
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
#get_ipython().magic(u'matplotlib inline')

# import numpy as np
# from datetime import datetime
# import pandas as pd


# There'll be a warning above about a font cache.  Ignore it, it doesn't matter. 

# In[ ]:

def plot_points(lat, lon):
    width = 15
    height = 15
    fig = plt.figure(figsize=(width, height));
    themap = Basemap(projection='gall',
              llcrnrlon = min(lon)-10,              # lower-left corner longitude
              llcrnrlat = min(lat)-5,               # lower-left corner latitude
              urcrnrlon = max(lon)+10,               # upper-right corner longitude
              urcrnrlat = max(lat)+5,               # upper-right corner latitude
              resolution = 'l',
              area_thresh = 500.0,
              );
    themap.drawcoastlines();
    themap.drawcountries();
    themap.fillcontinents(color = 'gainsboro',lake_color='lightskyblue');
    themap.drawmapboundary(fill_color='steelblue');

    x, y = themap(lon,lat);

    themap.plot(x, y, 
            'o',                    # marker shape
            c='indigo',         # marker colour
            markersize=8            # marker size
            );                    
    plt.show();


# Next we need to connect to the database file.  
# Then we make a cursor for some reason? Don't question it just remember to do it.   
# or go [here](http://stackoverflow.com/questions/6318126/why-do-you-need-to-create-a-cursor-when-querying-a-sqlite-database)

# In[ ]:

#C1
conn = sql.connect('test')
c    = conn.cursor()


# ok, so boring pre-amble over.   
# Lets see whats in the database.  
# We can execute queries pretty much like from the command line or sqlite3.  

# In[ ]:

#C2
c.execute("CREATE TABLE Person(firstname text, familyname text, age integer);");


# Simple way to create a table named Person with 3 columns in it
# This contains their name and age. To add people we can insert some or all the data

# In[ ]:

#C3
# Most basic way to insert data
c.execute("INSERT INTO Person VALUES('Alan','Brammer',27)");
# By specifying the column names we won't make a mistake though.
c.execute("INSERT INTO Person(firstname, familyname, age) VALUES('Alan','Brammer',27)");
# The order of the column names also doesn't need to matter. 
c.execute("INSERT INTO Person(familyname,firstname, age) VALUES('Brammer','Alan',27)");
# We also don't have to include all the information. 
c.execute("INSERT INTO Person(familyname,firstname) VALUES('Brammer','Alan')");


data = c.execute("SELECT * FROM Person");
for datum in data:
    print datum


# Because we inserted the same data multiple times we now have table of repeated and redundant info.
# We obviously don't want that, so we can create a table that doesn't allow it.  
# 
# - - -
# 
# First lets drop this table and start again and make a better version.

# In[ ]:

#C4
c.execute("DROP TABLE Person");
c.execute("CREATE TABLE Person(firstname text, familyname text, age integer, PRIMARY KEY(firstname, familyname)) ;");


# Now we have a "Primary Key" in the table.  This has to be unique throughout the whole table, but can be a combination of columns. 

# In[ ]:

#C5
c.execute("INSERT INTO Person(firstname, familyname, age) VALUES('Alan','Brammer',27)")
data = c.execute("SELECT * FROM Person")
for datum in data:
    print datum


# If we run the above code twice we now get an error stating why.  This is good, but also we didn't get any output because of the error.  SQL can helpfully ignore these erorrs though.

# In[ ]:

#C5
c.execute("INSERT OR IGNORE INTO Person(firstname, familyname, age) VALUES('Alan','Brammer',28)")
data = c.execute("SELECT * FROM Person")
for datum in data:
    print datum


# Here we tried to update the age but it was "ignored" because the primary key already exists.  
# We can replace instead of ignoring though.  More complicated methods also exist for this. 

# In[ ]:

#C6
c.execute("INSERT OR REPLACE INTO Person(firstname, familyname, age) VALUES('Alan','Brammer',28)")
c.execute("INSERT OR REPLACE INTO Person(firstname, familyname, age) VALUES('Brandon','Stark',9)")
data = c.execute("SELECT * FROM Person")
for datum in data:
    print datum
    


# Ok, So that was a very basic table lets drop it and look at some more complicating structures. 
# 
# - - -
# 
# We have a new database call adecks, so lets connect to that and put the cursor in it. 

# In[ ]:

#C7
c.execute("DROP TABLE IF EXISTS Person");

conn = sql.connect('adecks')
c    = conn.cursor()


# In[ ]:

#C8
pragma= c.execute("PRAGMA table_info(atl)");
for header in pragma.fetchall():
    print header[:3]

    
db_length = c.execute("SELECT Count(*)  FROM atl").fetchone()[0]
print "No of Lines in the table:",db_length;


# You can think of this in a way like a massive excel spreadsheet (with 755k lines) and 8 columns.  
# Creating a database is pretty easy, you just need to plan ahead and think about it first. 
# 
# So to create this table, we use similar line as before but with more columns.  Our primary key will now encompass 4 columns as well. 

# In[ ]:

#C9
c.execute('CREATE TABLE IF NOT EXISTS atl_new(id TEXT, date DATETIME, tech TEXT, fhr INT, lat REAL, lon REAL, vmax INT, mslp INT, type TEXT, PRIMARY KEY(id,date,tech,fhr));')

pragma= c.execute("PRAGMA table_info(atl_new)");
for header in pragma.fetchall():
    print header[:3]

 


# We can now start querying a large database.  First lets see when and what the most recent data entry was. 

# In[ ]:

#C10
recent_time = c.execute('SELECT MAX(date) FROM atl').fetchone()[0]
if recent_time is None:
    recent_time = 0
print recent_time


# In[ ]:

#C11
data = c.execute('SELECT date, id, lat, lon, fhr, mslp,tech FROM atl WHERE date='+str(recent_time)).fetchall()

idNo=[]; lat = []; lon = [];mslp=[];fhr=[]; tech=[];
for datum in data:
  idNo.append(datum[1])
  lat.append(datum[2])
  lon.append(datum[3])
  fhr.append(datum[4])
  mslp.append(datum[5])
  tech.append(datum[6])
  print datum[1],datum[6],datum[4], datum[2], datum[3]  


# In[ ]:

#C12
plot_points(lat,lon)


# In[ ]:

#C13
id_string='"aal09"';
data = c.execute('SELECT date, id, lat, lon, fhr, mslp FROM atl WHERE id='+id_string+' AND date>=2016010100 AND tech="CARQ" AND fhr=0').fetchall()

lat = []; lon = [];mslp=[];
for datum in data:
  lat.append(datum[2])
  lon.append(datum[3])
  mslp.append(datum[5])


# In[ ]:

#C14
for l in range(10):
    print lon[l], lat[l]


# In[ ]:

#C15
plot_points(lat,lon)


# In[ ]:

#C16
data = c.execute('SELECT date, id, lat, lon, fhr, mslp FROM atl WHERE mslp=(SELECT MIN(mslp) from atl where mslp >850 AND id!="aal51");').fetchall()

idNo=[]; date=[];lat = []; lon = [];mslp=[];
for datum in data:
    lat.append(datum[2])
    lon.append(datum[3])
    mslp.append(datum[5])
    date.append(datum[0])
    idNo.append(datum[1])

    
   
for d,i in zip(date,idNo):
      data = c.execute('SELECT date, id, lat, lon, fhr, mslp FROM atl WHERE date>=2016010100 AND id="'+str(i)+'" and tech like "AP%"').fetchall();
      lat = []; lon = [];mslp=[];
      print str(i)
      for datum in data:
        lat.append(datum[2])
        lon.append(datum[3])
        mslp.append(datum[5])
      plot_points(lat,lon)


# In[ ]:




# In[ ]:



