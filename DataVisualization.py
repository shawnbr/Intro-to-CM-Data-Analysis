import json
import os
from datetime import datetime
from datetime import timedelta
import cPickle as pickle

import matplotlib.pyplot as plt
DIR_PATH = os.getcwd() #Get currect directory

version = ""
UID = 0
TIM = 1
LAT = 2
LON = 3
LID = 4

locationdata = "datawlocation.json"
checkinwfriends = "checkinwfriends.json"

def plot(X,Y, title, xlabel, ylabel):
    #plt.figure()
    plt.plot(X, Y, 'ro')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
    #plt.savefig('CMC '+name+'.png')


checkins = {}
print "importing checkins"
with open(DIR_PATH + os.sep + "data\Gowalla_totalCheckins"+version+".txt", 'r') as f:
    for line in f:
        line = line.strip().split()
        
        uid = int(line[UID])
        time = datetime.strptime(line[1], '%Y-%m-%dT%H:%M:%SZ')
        lat = float(line[LAT])
        lon = float(line[LON])

        try:
            checkins[uid][time] = [lat,lon]
        except:
            times = {}
            times[time] = [lat,lon]
            checkins[uid] = times
            

with open('checkinwfriends.p', 'rb') as fp:
    checkinwfriends = pickle.load(fp)

with open('datawlocation.p', 'rb') as fp:
    locationdata = pickle.load(fp)

diff = {}
for uid in checkinwfriends.keys():
    diff[uid] = {}
    for friendCount in checkinwfriends[uid].keys():
        try:
            diff[uid][friendCount] = checkinwfriends[uid][friendCount] - locationdata[uid][friendCount]
        except:
            diff[uid][friendCount] = checkinwfriends[uid][friendCount]
            

######WITHOUT LOCATION ######

#Number of friends checked in with
X = []
#Frequencies of occurence
Y = []
temp = {}                              
#plotting
for uid in checkinwfriends.keys():
    totalCheckins = len(checkins[uid].keys())
    
    for friendCount in checkinwfriends[uid].keys():
        try:
            Y.append(checkinwfriends[uid][friendCount]/float(totalCheckins))
            X.append(friendCount)
        except:
            pass
        try:
            temp[friendCount].append(checkinwfriends[uid][friendCount]/float(totalCheckins))
        except:
            temp[friendCount] = [checkinwfriends[uid][friendCount]/float(totalCheckins)]
        
plot(X,Y,"Frequency vs Friend Count", "# of Friends Checked in with", "Frequency")

#Average 
Xavg = []
Yavg = []
for key in temp.keys():
    Xavg.append(key)
    Yavg.append(sum(temp[key])/float(len(temp[key])))
plot(Xavg,Yavg,"Frequency vs Friend Count", "# of Friends Checked in with", "Frequency (avg)")

######LOCATION ######

#Number of friends checked in with
Xloc = []
#Frequencies of occurence
Yloc = []
temploc = {}                              
#plotting
for uid in locationdata.keys():
    totalCheckins = len(checkins[uid].keys())
    
    for friendCount in locationdata[uid].keys():
        try:
            Yloc.append(locationdata[uid][friendCount]/float(totalCheckins))
            Xloc.append(friendCount)
        except:
            pass
        try:
            temploc[friendCount].append(locationdata[uid][friendCount]/float(totalCheckins))
        except:
            temploc[friendCount] = [locationdata[uid][friendCount]/float(totalCheckins)]


#Average 
Xavgloc = []
Yavgloc = []
for key in temp.keys():
    Xavgloc.append(key)
    Yavgloc.append(sum(temploc[key])/float(len(temploc[key])))
plot(Xavgloc,Yavgloc,"Frequency vs Friend Count", "# of Friends Checked in with", "Frequency (avg)")


##### DIFFERENCE #######

#Number of friends checked in with
Xdiff = []
#Frequencies of occurence
Ydiff = []
temp = {}                              
#plotting
for uid in diff.keys():
    totalCheckins = len(checkins[uid].keys())
    
    for friendCount in diff[uid].keys():
        try:
            Ydiff.append(diff[uid][friendCount]/float(totalCheckins))
            Xdiff.append(friendCount)
        except:
            pass
        try:
            temp[friendCount].append(diff[uid][friendCount]/float(totalCheckins))
        except:
            temp[friendCount] = [diff[uid][friendCount]/float(totalCheckins)]
        
plot(X,Y,"Frequency vs Friend Count", "# of Friends Checked in with", "Frequency")

#Average 
Xavgdiff = []
Yavgdiff = []
for key in temp.keys():
    Xavgdiff.append(key)
    Yavgdiff.append(sum(temp[key])/float(len(temp[key])))
plot(Xavgdiff,Yavgdiff,"Frequency vs Friend Count (number of checkins not in the same location)", "# of Friends Checked in with", "Frequency (avg)")


