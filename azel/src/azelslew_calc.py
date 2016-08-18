##############################################################################
# These are the functions used by extract.py.                                #
##############################################################################
import os
import sys


###############################################################################

def parseLogTime(time):
    year  = float(time[:4])
    day   = float(time[5:8])
    hour  = float(time[9:11])
    min   = float(time[12:14])
    sec   = float(time[15:17])
    hun   = float(time[18:20])

    time = hun+100*(sec+60*(min+60*(hour+24*day)))

    return time/100

###############################################################################

def parseSkdTime(time):

    year = float(time[:4])
    day  = float(time[2:5])
    hour = float(time[6:8])
    min  = float(time[8:10])
    sec  = float(time[10:12])
    hun  = 0.0

    time = hun+100*(sec+60*(min+60*(hour+24*day)))

    return time/100

###############################################################################

def getLogData(path_to_logs, tups):
    nstations = 0
    sourceacquired = False
    station = ""

    for subdir, dirs, files in os.walk(path_to_logs):
        for file in files:
            if file[-4:] == ".log":
                sourcefound = False
                sourceacquired = False
                nstations = nstations + 1
                station = file[-6:-4].lower()
                log = open(os.path.join(subdir, file), 'r')
                sourcelines = log.readlines()
                log.close()

                for line in sourcelines:
                    if ("source=" in line) and (("ccw" in line) \
                                           or ("cw" in line) \
                                           or ("neutral" in line)):
                        sourcefound = True
                        sline = line.split(',')
                        source = sline[0]
                        ssource = source.split('=')
                        source = ssource[1]
                        direction = sline[len(sline)-1][:-1]
                        sourcedate = parseLogTime(line[:20])

                    if ((("#trakl#Source acquired" in line) or \
                        ("#trakl# Source acquired" in line) or \
                        ('#flagr#flagr/antenna,acquired' in line)) and sourcefound):
                        sourceacquired = True
                        trakldate = parseLogTime(line[:20])
                        if (trakldate > sourcedate):
                            tups.append((station, sourcedate, source, trakldate, direction, file))
                if not sourceacquired:
                    print "# WARNING #"
                    print "Trakl or Flagr is not turned on for station " + station \
                        + " in session " + file[:-6] + '\n'

        return nstations

###############################################################################

def getSkdData(path_to_dir, nstations, scheduled_stations, theo):
    azelfound = False
    station = ""
    nLines = 0

    for subdir, dirs, files in os.walk(path_to_dir):
        for file in files:
            if file[-5:] == ".azel":
                azelfound = True
                skd = open(os.path.join(subdir, file), 'r')
                sourcelines = skd.readlines()
                skd.close()

                for line in sourcelines:
                    nLines = nLines + 1
                    if line[0:4] == "name":
                        for i in range(22,(22+nstations*8),8):
                            scheduled_stations.append(line[i+4:i+6])
            
                    if nLines > 3 and (not (line[0:3]=="End")):
                        for i in range(23, (23+nstations*8),8):
                            if (not (line[i:i+3].isspace())):
                                index = ((i-23)/8)
                                station = scheduled_stations[index].lower()
                                source = line[0:8]
                                date = parseSkdTime(line[9:21])
                                az = float(line[i:i+3])
                                el = float(line[i+4:i+6])
                                theo.append((station, date, source, az, el))
            
                if not azelfound:
                    print "Unable to locate .azel file in " + path_to_dir
                    print "Make sure there is a .azel file before you proceed. See the " + \
                           "README.md for info on how to generate one."
            
###############################################################################

def matchSkdLog(log, skd, matched):
    # log(station, sourcedate, source, trakldate, direction, filename)
    # skd(station, date, source, az, el)
    log = sorted(log)
    skd = sorted(skd)
    minrange = 0.0
    maxrange = 0.0
    d_az = 0.0

    for i in range(len(log)):
        for j in range(len(skd)):
            if log[i][0] == skd[j][0]:
                if skd[j][1] < log[i][1] < skd[j+1][1]:
                    if log[i][2] == skd[j+1][2]:
                        station = log[i][0]
                        timediff = log[i][3] - log[i][1]
                        az_b = skd[j][3]
                        az_a = skd[j+1][3]
                        el_b = skd[j][4]
                        el_a = skd[j+1][4]
                        skdtime = skd[j][1]
                        source = skd[j][2]
                        d_az = abs(az_a - az_b)
                        d_el = abs(el_a - el_b)
                        matched.append((station, timediff, d_az, d_el, skdtime, source))

###############################################################################

# time = (acc + (distance/(vel/60))
# sec  = sec  +  deg/((deg/min)/(sec/min))

def calcAz(spec, rotdata):

    az_slew = (spec[4] + rotdata[2]/(spec[2]/60))

    return az_slew


def calcEl(spec, rotdata):

    el_slew = (spec[4] + rotdata[3]/(spec[3]/60))

    return el_slew

