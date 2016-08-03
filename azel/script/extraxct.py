import os
import sys

if not len(sys.argv) > 1:
    print "Wrong usage."
    print "$> python extraxct.py logdir skdfile"
    print "You must supply the program with a folder containing the log " \
         +"files for the session, as well as the skdfile for the same " \
         +"session."
    sys.exit()

logdir = sys.argv[1]
skddir = sys.argv[2]

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
                    theo.append((station, date, source, az, el))

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
                sourcefound = False
        return nstations

###############################################################################

def getSkdData(path_to_file):

    skd = open(path_to_file, 'r')
    sourcelines = skd.readlines()
    skd.close()

    parseSkd(sourcelines)

###############################################################################

def matchSkdLog(log, skd):
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
                        d_az = abs(skd[j+1][3] - skd[j][3])
                        #if station == "is":
                            #print "Station: " + station + ", dAZ: " + str(d_az) + ", timediff: " + \
                            #str(timediff) + ", Sourcedate: " + str(log[i][1]) + \
                            #", Trakldate: " + str(log[i][3]) + ",  Dir: " + log[i][4]
                        d_el = abs(skd[j+1][4] - skd[j][4])
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

###############################################################################

#logdir = "/home/erik/Programming/git/GSFC_Internship/azel/logs/r1729/"
#skddir = "/home/erik/Programming/git/GSFC_Internship/azel/skds/r1729.azel"

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

# Hart
ht_az = (-185.0, 275.0)
ht_el = (2.0, 88.0)
ht_azspeed = 300.0
ht_elspeed = 60.0
ht_azspeed_acc = 3.0
ht_elspeed_acc = 3.0
ht_list = [ht_az, ht_el, ht_azspeed, ht_elspeed, ht_azspeed_acc, ht_elspeed_acc]

# Ishioka
is_az = (-75.0, 430.0)
is_el = (5.0, 89.0)
is_azspeed = 720.0
is_elspeed = 360.0
is_azspeed_acc = 10.0
is_elspeed_acc = 10.0
is_list = [is_az, is_el, is_azspeed, is_elspeed, is_azspeed_acc, is_elspeed_acc]

# Kashim
kb_az = (90.0, 630.0)
kb_el = (7.0, 88.0)
kb_azspeed = 45.0
kb_elspeed = 40.0
kb_azspeed_acc = 0.0
kb_elspeed_acc = 0.0
kb_list = [kb_az, kb_el, kb_azspeed, kb_elspeed, kb_azspeed_acc, kb_elspeed_acc]

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

# Sejong
kv_az = (10.0, 710.0)
kv_el = (5.0, 89.0)
kv_azspeed = 300.0
kv_elspeed = 300.0
kv_azspeed_acc = 0.0
kv_elspeed_acc = 0.0
kv_list = [kv_az, kv_el, kv_azspeed, kv_elspeed, kv_azspeed_acc, kv_elspeed_acc]

# Matera
ma_az = (277.0, 803.0)
ma_el = (4.0, 88.0)
ma_azspeed = 90.0
ma_elspeed = 100.0
ma_azspeed_acc = 20.0
ma_elspeed_acc = 20.0
ma_list = [ma_az, ma_el, ma_azspeed, ma_elspeed, ma_azspeed_acc, ma_elspeed_acc]

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
#ft_slew=[]
#hb_slew=[]
#ht_slew=[]
#is_slew=[]
#kb_slew=[]
#ke_slew=[]
#kk_slew=[]
#kv_slew=[]
#ny_slew=[]
#ts_slew=[]
#ww_slew=[]
#wn_slew=[]
#wz_slew=[]
#yg_slew=[]

nstations = getLogData(logdir)
getSkdData(skddir)
matchSkdLog(tups, theo)

ft_az = open("ft_az.dat",'w')
ft_el = open("ft_el.dat",'w')
hb_az = open("hb_az.dat",'w')
hb_el = open("hb_el.dat",'w')
ht_az = open("ht_az.dat",'w')
ht_el = open("ht_el.dat",'w')
is_az = open("is_az.dat",'w')
is_el = open("is_el.dat",'w')
kb_az = open("kb_az.dat",'w')
kb_el = open("kb_el.dat",'w')
ke_az = open("ke_az.dat",'w')
ke_el = open("ke_el.dat",'w')
kk_az = open("kk_az.dat",'w')
kk_el = open("kk_el.dat",'w')
kv_az = open("kv_az.dat",'w')
kv_el = open("kv_el.dat",'w')
ma_az = open("ma_az.dat",'w')
ma_el = open("ma_el.dat",'w')
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

az_c = 1
el_c = 1

for entry in matched:
    if entry[0] == "ft":
        az_slew = calcAz(ft_list, entry)
        el_slew = calcEl(ft_list, entry)
#        ft_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew*az_c:
            ft_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        elif az_slew*el_c < el_slew:
            ft_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
        else:
            pass

    elif entry[0] == "hb":
        az_slew = calcAz(hb_list, entry)
        el_slew = calcEl(hb_list, entry)
#        hb_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew*az_c:
            hb_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        elif az_slew*el_c < el_slew:
            hb_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
        else:
            pass

    elif entry[0] == "ht":
        az_slew = calcAz(ht_list, entry)
        el_slew = calcEl(ht_list, entry)
#        ht_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew*az_c:
            ht_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        elif az_slew*el_c < el_slew:
            ht_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
        else:
            pass

    elif entry[0] == "is":
        az_slew = calcAz(is_list, entry)
        el_slew = calcEl(is_list, entry)
#        is_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew*az_c:
            is_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        elif az_slew*el_c < el_slew:
            is_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
        else:
            pass

    elif entry[0] == "kb":
        az_slew = calcAz(kb_list, entry)
        el_slew = calcEl(kb_list, entry)
#        kb_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew*az_c:
            kb_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        elif az_slew*el_c < el_slew:
            kb_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
        else:
            pass

    elif entry[0] == "ke":
        az_slew = calcAz(ke_list, entry)
        el_slew = calcEl(ke_list, entry)
#        ke_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew*az_c:
            ke_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        elif az_slew*el_c < el_slew:
            ke_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
        else:
            pass

    elif entry[0] == "kk":
        az_slew = calcAz(kk_list, entry)
        el_slew = calcEl(kk_list, entry)
#        kk_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew*az_c:
            kk_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        elif az_slew*el_c < el_slew:
            kk_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
        else:
            pass

    elif entry[0] == "kv":
        az_slew = calcAz(kv_list, entry)
        el_slew = calcEl(kv_list, entry)
#        kv_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew*az_c:
            kv_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        elif az_slew*el_c < el_slew:
            kv_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
        else:
            pass

    elif entry[0] == "ma":
        az_slew = calcAz(ma_list, entry)
        el_slew = calcEl(ma_list, entry)
#        ma_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew*az_c:
            ma_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        elif az_slew*el_c < el_slew:
            ma_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
        else:
            pass

    elif entry[0] == "ny":
        az_slew = calcAz(ny_list, entry)
        el_slew = calcEl(ny_list, entry)
#        ny_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew*az_c:
            ny_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        elif az_slew*el_c < el_slew:
            ny_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
        else:
            pass

    elif entry[0] == "ts":
        az_slew = calcAz(ts_list, entry)
        el_slew = calcEl(ts_list, entry)
#        ts_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew*az_c:
            ts_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        elif az_slew*el_c < el_slew:
            ts_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
        else:
            pass

    elif entry[0] == "ww":
        az_slew = calcAz(ww_list, entry)
        el_slew = calcEl(ww_list, entry)
#        ww_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew*az_c:
            ww_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        elif az_slew*el_c < el_slew:
            ww_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
        else:
            pass

    elif entry[0] == "wn":
        az_slew = calcAz(wn_list, entry)
        el_slew = calcEl(wn_list, entry)
#        wn_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew*az_c:
            wn_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        elif az_slew*el_c < el_slew:
            wn_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
        else:
            pass

    elif entry[0] == "wz":
        az_slew = calcAz(wz_list, entry)
        el_slew = calcEl(wz_list, entry)
#        wz_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew*az_c:
            wz_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        elif az_slew*el_c < el_slew:
            wz_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
        else:
            pass

    elif entry[0] == "yg":
        az_slew = calcAz(yg_list, entry)
        el_slew = calcEl(yg_list, entry)
#        yg_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew*az_c:
            yg_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        elif az_slew*el_c < el_slew:
            yg_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
        else:
            pass
    else:
        print "No specs for this antenna: " + entry[0]

