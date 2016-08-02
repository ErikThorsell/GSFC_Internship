import os

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
                    station = scheduled_stations[index].lower()
                    source = line[0:8]
                    date = parseSkdTime(line[9:21])
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
    # log(station, sourcedate, source, trakldate, direction, filename)
    # skd(station, date, source, az, el, dur)
    log = sorted(log)
    skd = sorted(skd)
    minrange = 0
    maxrange = 0

    for i in range(len(log)):
        for j in range(len(skd)):
            if log[i][0] == skd[j][0]:
                if skd[j][1] < log[i][1] < skd[j+1][1]:
                    if log[i][2] == skd[j+1][2]:
                        station = log[i][0]
                        timediff = log[i][3] - log[i][1]
                        d_az = abs(skd[j][3]-skd[j+1][3])
                        if log[i][0] == "ft":
                            minrange = ft_az[0]
                            maxrange = ft_az[1]
                        elif log[i][0] == "hb":
                            minrange = hb_az[0]
                            maxrange = hb_az[1]
                        elif log[i][0] == "ke":
                            minrange = ke_az[0]
                            maxrange = ke_az[1]
                        elif log[i][0] == "kk":
                            minrange = kk_az[0]
                            maxrange = kk_az[1]
                        elif log[i][0] == "ny":
                            minrange = ny_az[0]
                            maxrange = ny_az[1]
                        elif log[i][0] == "ts":
                            minrange = ts_az[0]
                            maxrange = ts_az[1]
                        elif log[i][0] == "ww":
                            minrange = ww_az[0]
                            maxrange = ww_az[1]
                        elif log[i][0] == "wn":
                            minrange = wn_az[0]
                            maxrange = wn_az[1]
                        elif log[i][0] == "wz":
                            minrange = wz_az[0]
                            maxrange = wz_az[1]
                        elif log[i][0] == "yg":
                            minrange = yg_az[0]
                            maxrange = yg_az[1]
                        else:
                            print "No array for said station."

                        if (skd[j][3] + d_az > maxrange) or (skd[j][3] - d_az < minrange):
                            d_az = 360 - d_az

                        d_el = abs(skd[j][4]-skd[j+1][4])
                        matched.append((station, timediff, d_az, d_el))

###############################################################################

# time = (acc + (distance/vel) * 60)
# sec  = sec  +  deg/(deg/min) * (sec/min)

def calcAz(spec, rotdata):

    az_slew = (spec[4] + rotdata[2]/spec[2]*60)

    return az_slew


def calcEl(spec, rotdata):

    el_slew = (spec[4] + rotdata[3]/spec[2]*60)

    return el_slew

###############################################################################


logdir = "/home/erik/Programming/git/GSFC_Internship/azel/logs/"
skddir = "/home/erik/Programming/git/GSFC_Internship/azel/skds/"

#####################################
# Static Variables for the antennas #
# In the skd-file these are read as:
#    n/a  az-slew  az-acc  az-ran-  az-ran+  el-slew  el-acc  el-ran-  el-ran+
#

# Fortaleza
ft_az = (171.0, 709.0)
ft_el = (5.0, 88.0)
ft_azspeed = 40.0
ft_elspeed = 20.0
ft_azspeed_acc = 0.0
ft_elspeed_acc = 0.0
ft_list = [ft_az, ft_el, ft_azspeed, ft_elspeed, ft_azspeed_acc, ft_elspeed_acc]

# Hobart
hb_az = (90.0, 630.0)
hb_el = (5.0, 88.0)
hb_azspeed = 300.0
hb_elspeed = 75.0
hb_azspeed_acc = 3.0
hb_elspeed_acc = 3.0
hb_list = [hb_az, hb_el, hb_azspeed, hb_elspeed, hb_azspeed_acc, hb_elspeed_acc]

# Kath
ke_az = (90.0, 630.0)
ke_el = (5.0, 88.0)
ke_azspeed = 300.0
ke_elspeed = 75.0
ke_azspeed_acc = 3.0
ke_elspeed_acc = 3.0
ke_list = [ke_az, ke_el, ke_azspeed, ke_elspeed, ke_azspeed_acc, ke_elspeed_acc]

# Kokee
kk_az = (270.0, 810.0)
kk_el = (0.0, 89.7)
kk_azspeed = 117.0
kk_elspeed = 117.0
kk_azspeed_acc = 15.0
kk_elspeed_acc = 15.0
kk_list = [kk_az, kk_el, kk_azspeed, kk_elspeed, kk_azspeed_acc, kk_elspeed_acc]

# Nyales
ny_az = (271.0, 809.0)
ny_el = (0.0, 89.7)
ny_azspeed = 120.0
ny_elspeed = 120.0
ny_azspeed_acc = 9.0
ny_elspeed_acc = 9.0
ny_list = [ny_az, ny_el, ny_azspeed, ny_elspeed, ny_azspeed_acc, ny_elspeed_acc]

# Tsukub
ts_az = (10.0, 710.0)
ts_el = (5.0, 88.0)
ts_azspeed = 180.0
ts_elspeed = 180.0
ts_azspeed_acc = 14.0
ts_elspeed_acc = 14.0
ts_list = [ts_az, ts_el, ts_azspeed, ts_elspeed, ts_azspeed_acc, ts_elspeed_acc]

# Yarra
yg_az = (90.0, 630.0)
yg_el = (5.0, 88.0)
yg_azspeed = 300.0
yg_elspeed = 75.0
yg_azspeed_acc = 3.0
yg_elspeed_acc = 3.0
yg_list = [yg_az, yg_el, yg_azspeed, yg_elspeed, yg_azspeed_acc, yg_elspeed_acc]

######################
#ww_az =
#ww_el =
#ww_azspeed =
#ww_elspeed =
#ww_azspeed_acc =
#ww_elspeed_acc =
#wn_az =
#wn_el =
#wn_azspeed =
#wn_elspeed =
#wn_azspeed_acc =
#wn_elspeed_acc =
#wz_az =
#wz_el =
#wz_azspeed =
#wz_elspeed =
#wz_azspeed_acc =
#wz_elspeed_acc =
#                                  #
####################################

filename = ""
station = ""
nstations = 0
tups=[]
scheduled_stations=[]
theo=[]
matched=[]
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
ft_slew=[]
hb_slew=[]
ke_slew=[]
kk_slew=[]
ny_slew=[]
ts_slew=[]
ww_slew=[]
wn_slew=[]
wz_slew=[]
yg_slew=[]

nstations = getLogData(logdir)
getSkdData(skddir)
matchSkdLog(tups, theo)


ft_az = open("ft_az.dat",'w')
ft_el = open("ft_el.dat",'w')
hb_az = open("hb_az.dat",'w')
hb_el = open("hb_el.dat",'w')
ke_az = open("ke_az.dat",'w')
ke_el = open("ke_el.dat",'w')
kk_az = open("kk_az.dat",'w')
kk_el = open("kk_el.dat",'w')
ny_az = open("ny_az.dat",'w')
ny_el = open("ny_el.dat",'w')
ts_az = open("ts_az.dat",'w')
ts_el = open("ts_el.dat",'w')
ww_az = open("ww_az.dat",'w')
ww_el = open("ww_el.dat",'w')
wn_az = open("wn_az.dat",'w')
wn_el = open("wn_el.dat",'w')
wz_az = open("wz_az.dat",'w')
wz_el = open("wz_el.dat",'w')
yg_az = open("yg_az.dat",'w')
yg_el = open("yg_el.dat",'w')

for entry in matched:
    if entry[0] == "ft":
        az_slew = calcAz(ft_list, entry)
        el_slew = calcEl(ft_list, entry)
        ft_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew:
            ft_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        else:
            ft_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')

    elif entry[0] == "hb":
        az_slew = calcAz(hb_list, entry)
        el_slew = calcEl(hb_list, entry)
        hb_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew:
            hb_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        else:
            hb_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
    elif entry[0] == "ke":
        az_slew = calcAz(ke_list, entry)
        el_slew = calcEl(ke_list, entry)
        ke_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew:
            ke_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        else:
            ke_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
    elif entry[0] == "kk":
        az_slew = calcAz(kk_list, entry)
        el_slew = calcEl(kk_list, entry)
        kk_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew:
            kk_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        else:
            kk_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
    elif entry[0] == "ny":
        az_slew = calcAz(ny_list, entry)
        el_slew = calcEl(ny_list, entry)
        ny_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew:
            ny_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        else:
            ny_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
    elif entry[0] == "ts":
        az_slew = calcAz(ts_list, entry)
        el_slew = calcEl(ts_list, entry)
        ts_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew:
            ts_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        else:
            ts_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
    elif entry[0] == "ww":
        az_slew = calcAz(ww_list, entry)
        el_slew = calcEl(ww_list, entry)
        ww_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew:
            ww_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        else:
            ww_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
    elif entry[0] == "wn":
        az_slew = calcAz(wn_list, entry)
        el_slew = calcEl(wn_list, entry)
        wn_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew:
            wn_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        else:
            wn_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
    elif entry[0] == "wz":
        az_slew = calcAz(wz_list, entry)
        el_slew = calcEl(wz_list, entry)
        wz_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew:
            wz_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        else:
            wz_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
    elif entry[0] == "yg":
        az_slew = calcAz(yg_list, entry)
        el_slew = calcEl(yg_list, entry)
        yg_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew:
            yg_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        else:
            yg_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
    else:
        print "No specs for this antenna!"

for t in tups:
    diff = t[3]-t[1]
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

#for i in range(len(tups)):
#    print theo[i]
#    print tups[i]

