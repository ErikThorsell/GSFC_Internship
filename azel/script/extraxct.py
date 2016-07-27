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

#    print sourcetime
#    print trakltime
#    print s_tot
#    print t_tot
    return t_tot - s_tot

###############################################################################

def getLogData(path_to_logs):

    sourcefound = False

    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            station = file[5:7]
            log = open(os.path.join(subdir, file), 'r')
            sourcelines = log.readlines()
            log.close()

            for line in sourcelines:
                if ("source=" in line) and (("ccw" in line) \
                                       or ("cw" in line) \
                                       or ("neutral" in line)):
                    sourcefound = True
                    sourcedate = line[:20]
                if ("#trakl#Source acquired" in line and sourcefound):
                    sourcefound = False
                    trakldate = line[:20]
                    if (trakldate > sourcedate):
                        tups.append((station, sourcedate, trakldate))

###############################################################################

rootdir = "/home/erik/Programming/git/GSFC_Internship/azel/logs/"
station = ""
tups=[]
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

getLogData(rootdir)

for t in tups:
    diff = timeDiff(t[1], t[2])
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

print "Ft: " + str(len(ft_diffs))
print "Hb: " + str(len(hb_diffs))
print "Ke: " + str(len(ke_diffs))
print "Kk: " + str(len(kk_diffs))
print "Ny: " + str(len(ny_diffs))
print "Ts: " + str(len(ts_diffs))
print "Ww: " + str(len(ww_diffs))
print "Wn: " + str(len(wn_diffs))
print "Wz: " + str(len(wz_diffs))
print "Yg: " + str(len(yg_diffs))
