import os

###############################################################################

def timeDiff(sourcetime, trakltime):
    s_year  = int(sourcetime[:4])
    s_day   = int(sourcetime[5:8])
    s_hour  = int(sourcetime[9:11])
    s_min   = int(sourcetime[12:14])
    s_sec   = int(sourcetime[15:17])
    s_hun   = int(sourcetime[18:20])

    t_year  = int(trakltime[:4])
    t_day   = int(trakltime[5:8])
    t_hour  = int(trakltime[9:11])
    t_min   = int(trakltime[12:14])
    t_sec   = int(trakltime[15:17])
    t_hun   = int(trakltime[18:20])

    s_tot = s_hun+100*(s_sec+60*(s_min+60*(s_hour+24*s_day)))
    t_tot = t_hun+100*(t_sec+60*(t_min+60*(t_hour+24*t_day)))

    return t_tot - s_tot

###############################################################################

def parseSkd(skd_file):
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
                    station = scheduled_stations[index]
                    source = line[0:8]
                    date = line[9:21]
                    az = int(line[i:i+3])
                    el = int(line[i+4:i+6])
                    duri = (23+nstations*8)+index*4-1
                    dur = int(line[duri:duri+4])
                    theo.append((station, date, source, az, el, dur))

###############################################################################

def getLogData(path_to_logs):
    nstations = 0
    sourcefound = False

    for subdir, dirs, files in os.walk(path_to_logs):
        for file in files:
            if file[-4:] == ".log":
                nstations = nstations + 1
                station = file[5:7]
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
                        sourcefound = True
                        sourcedate = line[:20]
                    if ("#trakl#Source acquired" in line and sourcefound):
                        sourcefound = False
                        trakldate = line[:20]
                        if (trakldate > sourcedate):
                            tups.append((station, sourcedate, source, trakldate, file))
        return nstations

###############################################################################

def getSkdData(path_to_file):

    for subdir, dirs, files in os.walk(path_to_file):
        for file in files:
            if file[-5:] == ".azel":
                skdname = file
                skd = open(os.path.join(subdir, file), 'r')
                sourcelines = skd.readlines()
                skd.close()

                parseSkd(sourcelines)

###############################################################################

def matchSkdLog(log, skd):
    # log(station, sourcedate, source, trakldate, filename)
    # skd(station, date, source, az, el, dur)

    pass

###############################################################################

logdir = "/home/erik/Programming/git/GSFC_Internship/azel/logs/"
skddir = "/home/erik/Programming/git/GSFC_Internship/azel/skds/"

filename = ""
station = ""
nstations = 0
tups=[]
scheduled_stations=[]
theo=[]
ft_diffs=[]
hb_diffs=[]
ke_diffs=[]
kk_diffs=[]
ny_diffs=[]
ts_diffs=[]
ww_diffs=[]
wn_diffs=[]
wz_diffs=[]
yg_diffs=[]

nstations = getLogData(logdir)
ust = sorted(scheduled_stations)
getSkdData(skddir)

for t in tups:
    diff = timeDiff(t[1], t[3])
    station = t[0]
    if station == "ft":
        ft_diffs.append(diff)
    elif station == "hb":
        hb_diffs.append(diff)
    elif station == "ke":
        ke_diffs.append(diff)
    elif station == "kk":
        kk_diffs.append(diff)
    elif station == "ny":
        ny_diffs.append(diff)
    elif station == "ts":
        ts_diffs.append(diff)
    elif station == "ww":
        ww_diffs.append(diff)
    elif station == "wn":
        wn_diffs.append(diff)
    elif station == "wz":
        wz_diffs.append(diff)
    elif station == "yg":
        yg_diffs.append(diff)
    else:
        print "There is no array to store this data."

#for t in tups:
#    print "Tups:", t

#for station in theo:
#    print "Theo:", station

print theo[0]
print tups[0]

theo = sorted(theo)
tups = sorted(tups)

for i in range(0,5):
    print theo[i]
    print tups[i]

