import os
import matplotlib.pyplot as plt
DIR_PATH = os.getcwd() #Get currect directory
N = 1000
#f = open(DIR_PATH + os.sep + "data\Gowalla_edges.txt")

LAT = 2
LON = 3
LID = 4

popCheckIn = {}
locations = {}

def plot(X,Y, title, xlabel, ylabel):
    #plt.figure()
    plt.plot(X, Y, '.')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    plt.show()
    
    #plt.savefig('CMC '+name+'.png')

with open(DIR_PATH + os.sep + "data\Gowalla_edges.txt", 'r') as f:
    #i = 0
    for line in f:
        #if i> N:
        #    break
        try:
            popCheckIn[int(line.strip().split()[0])][0] += 1
        except:
            popCheckIn[int(line.strip().split()[0])] = [1,0]               
        #i += 1



with open(DIR_PATH + os.sep + "data\Gowalla_totalCheckins.txt", 'r') as f:
    #i = 0
    for line in f:
        #if i > N:
            #break
        try:
            popCheckIn[int(line.strip().split()[0])][1] += 1
        except:
            popCheckIn[int(line.strip().split()[0])].append(1)
        #i += 1

maxVal = -1
for value in popCheckIn.values():
    if value[0] > maxVal:
        maxVal = value[0]

X = []
Y = []
temp = {}
for key in popCheckIn.keys():
    #if popCheckIn[key][0]/float(maxVal) < 0.05:
    X.append(popCheckIn[key][0]/float(maxVal))
    Y.append(popCheckIn[key][1])
    try:
        temp[popCheckIn[key][0]].append(popCheckIn[key][1])
    except:
        temp[popCheckIn[key][0]] = [popCheckIn[key][1]]

#Average 
Xavg = []
Yavg = []
for key in temp.keys():
    Xavg.append(key/float(maxVal))
    Yavg.append(sum(temp[key])/float(len(temp[key])))
plot(X,Y,"Checkins vs Popularity", "Popularity", "Checkins")

    
