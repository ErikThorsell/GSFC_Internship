import os
import sys


###############################################################################

def parseLogTime(time):
    year  = int(time[:4])
    day   = int(time[5:8])
    hour  = int(time[9:11])
    min   = int(time[12:14])
    sec   = int(time[15:17])
    hun   = int(time[18:20])

    time = hun+100*(sec+60*(min+60*(hour+24*day)))

    return time/100

###############################################################################

def parseSkdTime(time):

    year  = int(time[:4])
    day  = int(time[2:5])
    hour = int(time[6:8])
    min  = int(time[8:10])
    sec  = int(time[10:12])
    hun  = 0

    time = hun+100*(sec+60*(min+60*(hour+24*day)))

    return time/100

###############################################################################

def parseSkd(skd_file, nstations, scheduled_stations, theo):
    station = ""
    nLines = 0

    for line in skd_file:
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
                    az = int(line[i:i+3])
                    el = int(line[i+4:i+6])
                    theo.append((station, date, source, az, el))

###############################################################################

def getLogData(path_to_logs, tups):
    nstations = 0
    sourcefound = False
    for subdir, dirs, files in os.walk(path_to_logs):
        for file in files:
            if file[-4:] == ".log":
                nstations = nstations + 1
                station = file[5:7].lower()
                log = open(os.path.join(subdir, file), 'r')
                sourcelines = log.readlines()
                log.close()

                for line in sourcelines:
                    if ("source=" in line) and (("ccw" in line) \
                                           or ("cw" in line) \
                                           or ("neutral" in line)):
                        sline = line.split(',')
                        source = sline[0]
                        ssource = source.split('=')
                        source = ssource[1]
                        direction = sline[len(sline)-1][:-1]
                        sourcefound = True
                        sourcedate = parseLogTime(line[:20])
                    if ("#trakl#Source acquired" in line and sourcefound):
                        sourcefound = False
                        trakldate = parseLogTime(line[:20])
                        if (trakldate > sourcedate):
                            tups.append((station, sourcedate, source, trakldate, direction, file))
                sourcefound = False
        return nstations

###############################################################################

def getSkdData(path_to_file, nstations, scheduled_stations, theo):

    skd = open(path_to_file, 'r')
    sourcelines = skd.readlines()
    skd.close()

    parseSkd(sourcelines, nstations, scheduled_stations, theo)

###############################################################################

def matchSkdLog(log, skd, matched):
    # log(station, sourcedate, source, trakldate, direction, filename)
    # skd(station, date, source, az, el)
    log = sorted(log)
    skd = sorted(skd)
    minrange = 0
    maxrange = 0
    d_az = 0

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

                        if station == "is":
                                az_b = az_b % 360
                                az_a = az_a % 360

                        d_az = abs(az_a - az_b)
                        d_el = abs(el_a - el_b)
                        matched.append((station, timediff, d_az, d_el))

###############################################################################

# time = (acc + (distance/(vel/60))
# sec  = sec  +  deg/((deg/min)/(sec/min))

def calcAz(spec, rotdata):

    az_slew = (spec[4] + rotdata[2]/(spec[2]/60))

    return az_slew


def calcEl(spec, rotdata):

    el_slew = (spec[4] + rotdata[3]/(spec[3]/60))

    return el_slew

