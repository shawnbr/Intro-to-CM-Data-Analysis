from datetime import datetime
from datetime import timedelta

import math
import csv
import os
import matplotlib.pyplot as plt
DIR_PATH = os.getcwd() #Get currect directory
N = 1000
version = ""
UID = 0
TIM = 1
LAT = 2
LON = 3
LID = 4

#timedelta = 600 seconds, i.e. 10 minutes
timedelta = 600 
#distancedelta = 500 meters, i.e. 0.5 km
distancedelta = 0.5



#dictionary of connections: key=userid, val=friend id
connections = {}
#dictionary of checkins: key=userid, val=dictionary of times: key=time, val= locations[lat,lon]
checkins = {}
#dictionary of poplularity: key: userid, val=number of friends
popularity = {}
#dictionary of checkins with friends: key: userid, val=dictionary of number of friends: key=#of friends, val= frequency
checkinwfriends = {}


def plot(X,Y, title, xlabel, ylabel):
    #plt.figure()
    plt.plot(X, Y, 'ro')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
    #plt.savefig('CMC '+name+'.png')

#*****************************************************
#Gets the distance between 2 different locations 
#From Oliver
#*****************************************************
def get_distance(lat1, long1, lat2, long2):
   # Convert latitude and longitude to
   # spherical coordinates in radians.
   degrees_to_radians = math.pi/180.0

   # phi = 90 - latitude
   phi1 = (90.0 - lat1)*degrees_to_radians
   phi2 = (90.0 - lat2)*degrees_to_radians

   # theta = longitude
   theta1 = long1*degrees_to_radians
   theta2 = long2*degrees_to_radians

   # Compute spherical distance from spherical coordinates.

   # For two locations in spherical coordinates
   # (1, theta, phi) and (1, theta, phi)
   # cosine( arc length ) =
   #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
   # distance = rho * arc length

   cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
          math.cos(phi1)*math.cos(phi2))
   arc = math.acos( cos )

   # Remember to multiply arc by the radius of the earth
   # in your favorite set of units to get length.
   # MODIFIED TO return distance in miles
   return arc*6371.0


print "importing edges"
with open(DIR_PATH + os.sep + "data\Gowalla_edges"+version+".txt", 'r') as f:
    for line in f:
        uid = int(line.strip().split()[0])
        friendid = int(line.strip().split()[1])
        try:
            connections[uid].append(friendid)
        except:
            connections[uid] = [friendid]

        try:
            popularity[uid] += 1
        except:
            popularity[uid] = 1               


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
            
print "crunch time"
#for each user
for user in checkins.keys():
    checkinwfriends[user] = {}
    print "user "+ str(user)
    #for each checkin
    for time in checkins[user].keys():
        friendCount = 0

        #for each friend
        for friend in connections[user]:
            #for each friend's checkins
            try:
                for ftime in checkins[friend]:
                    #if they checked in at a similar time
                    if abs((time-ftime).total_seconds()) < timedelta and get_distance(checkins[user][time][0],checkins[user][time][1],
                    checkins[friend][ftime][0], checkins[friend][ftime][1]) < distancedelta:
                        friendCount += 1
            #if the friend never checked in
            except:
                #print get_distance(checkins[user][time][0],checkins[user][time][1],
                #    checkins[friend][ftime][0], checkins[friend][ftime][1])
                pass
        try:
            checkinwfriends[user][friendCount] += 1
        except:
            checkinwfriends[user][friendCount] = 1            


writer = csv.writer(open('dict.csv', 'wb'))
for key, value in checkinwfriends.items():
   writer.writerow([key, value])
   


 
print "time to graph"
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


#            
#maxVal = -1
#for value in popCheckIn.values():
#    if value[0] > maxVal:
#        maxVal = value[0]
#
#X = []
#Y = []
#temp = {}
#for key in popCheckIn.keys():
#    #if popCheckIn[key][0]/float(maxVal) < 0.05:
#    X.append(popCheckIn[key][0]/float(maxVal))
#    Y.append(popCheckIn[key][1])
#    try:
#        temp[popCheckIn[key][0]].append(popCheckIn[key][1])
#    except:
#        temp[popCheckIn[key][0]] = [popCheckIn[key][1]]
#
##Average 
#Xavg = []
#Yavg = []
#for key in temp.keys():
#    Xavg.append(key/float(maxVal))
#    Yavg.append(sum(temp[key])/float(len(temp[key])))
#plot(X,Y,"Checkins vs Popularity", "Popularity", "Checkins")

    
