from datetime import datetime
from datetime import timedelta

import os
import matplotlib.pyplot as plt
DIR_PATH = os.getcwd() #Get currect directory
N = 1000
#f = open(DIR_PATH + os.sep + "data\Gowalla_edges.txt")

UID = 0
TIM = 1
LAT = 2
LON = 3
LID = 4

delta = timedelta(minutes=10)
 
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
    plt.plot(X, Y, '.')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
    #plt.savefig('CMC '+name+'.png')

print "importing edges"
with open(DIR_PATH + os.sep + "data\Gowalla_edges.txt", 'r') as f:
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
with open(DIR_PATH + os.sep + "data\Gowalla_totalCheckins.txt", 'r') as f:
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
    #for each checkin
    for times in checkins[user].keys():
        friendCount = 0

        #for each friend
        for friend in connections[user]:
            #for each friend's checkins
            try:
                for ftimes in checkins[friend]:
                    #if they checked in at a similar time           
                    if times-ftimes < delta or ftimes-times < delta:
                        friendCount += 1
            #if the friend never checked in
            except:
                pass
        try:
            checkinwfriends[uid][friendCount] += 1
        except:
            counts = {}
            counts[friendCount] = 1
            checkinwfriends[uid] = counts


print "time to graph"
#Number of friends checked in with
X = []
#Frequencies of occurence
Y = []
                                        
#plotting
for uid in checkinwfriends.keys():
    totalCheckins = list.size(checkins[uid].keys())
    
    for friendCount in checkinwfriends.keys():
        X.append(friendCount)
        Y.append(checkinwfriends[friendCount]/totalCheckins)
plot(X,Y,"Frequency vs Friend Count", "# of Friends Checked in with", "Frequency")
                
                
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

    