##############################################################################
# These are the functions used by extract.py.                                #
##############################################################################
import os
import sys


###############################################################################
# Converts the date and time given in the log file to number of seconds since
# the start of the year
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
# Converts the date and time given in the skd file to number of seconds since
# the start of the year

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
# Read in data from a log file (.log file)
# Find when the antenna is given the command to go to a new source, what source
# that is, what cablewrap it is on (cw, ccw, neutral) 
# Find if trakl or flagr is being used, and if so find the time when a source
# was acquired. 
# Also, store information about which session (which log file) the information
# comes from.

def getLogData(path_to_logs, log_data):
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
                        sourcetime = parseLogTime(line[:20])

                    if ((("#trakl#Source acquired" in line) or \
                        ("#trakl# Source acquired" in line) or \
                        ('#flagr#flagr/antenna,acquired' in line)) and sourcefound):
                        sourceacquired = True
                        trakltime = parseLogTime(line[:20])
                        if (trakltime > sourcetime):
                            log_data.append((station, sourcetime, source, trakltime, direction, file))
                if not sourceacquired:
                    print "# WARNING #"
                    print "Trakl or Flagr is not turned on for station " + station \
                        + " in session " + file[:-6] + '\n'

        return nstations

###############################################################################
# Read in data from a skd file (.azel file) 
# Find scheduled sources and their respective positions in az and el, and what
# time they are supposed to be observed for all the stations in the session.

def getSkdData(path_to_dir, nstations, scheduled_stations, skd_data):
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
                                timestamp = parseSkdTime(line[9:21])
                                az = float(line[i:i+3])
                                el = float(line[i+4:i+6])
                                skd_data.append((station, timestamp, source, az, el))
            
            if not azelfound:
                print "Unable to locate .azel file in " + path_to_dir
                print "Make sure there is a .azel file before you proceed. See the " + \
                        "README.md for info on how to generate one."
            
###############################################################################
# Matches data from skd and log files. 
# For matched points, save: (station, slewingtime, d_az, d_el, timestamp, source)
            
def matchSkdLog(log, skd, matched):
    # log(station, sourcetime, source, trakltime, direction, filename)
    # skd(station, timestamp, source, az, el)
    log = sorted(log)
    skd = sorted(skd)
    minrange = 0.0
    maxrange = 0.0
    d_az = 0.0

    for i in range(len(log)):
        for j in range(len(skd)):
            if log[i][0] == skd[j][0]:                      #Are we on the same station?
                if skd[j][1] < log[i][1] < skd[j+1][1]:     #Are we between two contigous measurements in the skd file?
                    if log[i][2] == skd[j+1][2]:            #Are we on the same source?
                        station = log[i][0]                 #Save station name
                        slewingtime = log[i][3] - log[i][1]    #Save the actual time the antenna slewed
                        az_before = skd[j][3]                    
                        az_after = skd[j+1][3]
                        el_before = skd[j][4]
                        el_after = skd[j+1][4]
                        d_az = abs(az_after - az_before)    #Save Delta_Azimuth
                        d_el = abs(el_after - el_before)    #Save Delta_Elevation
                        timestamp = skd[j][1]               #Save timestamp from skd file
                        source = skd[j][2]                  #Save source name
                        matched.append((station, slewingtime, d_az, d_el, timestamp, source))

###############################################################################
# Calculates theoretical azimuth slewing time

def calcAz(antenna_spec, rotdata):
    az_offset = antenna_spec[4]
    d_az = rotdata[2]
    az_speed = antenna_spec[2]

    az_slewtime = (az_offset + d_az/(az_speed/60))  #Divide by 60 to get sec to min conversion right

    return az_slewtime

###############################################################################
# Calculates theoretical elevation slewing time

def calcEl(antenna_spec, rotdata):
    el_offset = antenna_spec[5]
    d_el = rotdata[3]
    el_speed = antenna_spec[3]

    el_slewtime = (el_offset + d_el/(el_speed/60))  #Divide by 60 to get sec to min conversion right

    return el_slewtime

