import os
import matplotlib.pyplot as plt
DIR_PATH = os.getcwd() #Get currect directory
N = 1000
#f = open(DIR_PATH + os.sep + "data\Gowalla_edges.txt")

LAT = 2
LON = 3
LID = 4

locations = {}


with open(DIR_PATH + os.sep + "data\Gowalla_totalCheckins.txt", 'r') as f:
    for line in f:

        line = line.strip().split()
        lid = int(line[LID])
        try:
            lat = float(line[LAT])
            lon = float(line[LON])
        except:
            print line[LAT], line[LON]
        
        try:
            if locations[str(lat)+str(lon)] !=  lid:
                print lat,lon, lid, locations[str(lat)+str(lon)]
        except:
            locations[str(lat)+str(lon)] =  lid
