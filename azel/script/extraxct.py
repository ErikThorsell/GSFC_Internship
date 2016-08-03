import os
import sys
import azelslew_calc
from station_specs import *

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

#logdir = "/home/lina/Programming/GSFC_Internship/azel/logs/r1729/"
#skddir = "/home/lina/Programming/GSFC_Internship/azel/skds/r1729.azel"

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

nstations = azelslew_calc.getLogData(logdir,tups)
azelslew_calc.getSkdData(skddir, nstations, scheduled_stations, theo)
azelslew_calc.matchSkdLog(tups, theo, matched)
#leastsq.plot_curve(distance, times, station, orienta

ft_az = open("data/ft_az.dat",'a')
ft_el = open("data/ft_el.dat",'a')
hb_az = open("data/hb_az.dat",'a')
hb_el = open("data/hb_el.dat",'a')
ht_az = open("data/ht_az.dat",'a')
ht_el = open("data/ht_el.dat",'a')
is_az = open("data/is_az.dat",'a')
is_el = open("data/is_el.dat",'a')
kb_az = open("data/kb_az.dat",'a')
kb_el = open("data/kb_el.dat",'a')
ke_az = open("data/ke_az.dat",'a')
ke_el = open("data/ke_el.dat",'a')
kk_az = open("data/kk_az.dat",'a')
kk_el = open("data/kk_el.dat",'a')
kv_az = open("data/kv_az.dat",'a')
kv_el = open("data/kv_el.dat",'a')
ma_az = open("data/ma_az.dat",'a')
ma_el = open("data/ma_el.dat",'a')
ny_az = open("data/ny_az.dat",'a')
ny_el = open("data/ny_el.dat",'a')
ts_az = open("data/ts_az.dat",'a')
ts_el = open("data/ts_el.dat",'a')
ww_az = open("data/ww_az.dat",'a')
ww_el = open("data/ww_el.dat",'a')
wn_az = open("data/wn_az.dat",'a')
wn_el = open("data/wn_el.dat",'a')
wz_az = open("data/wz_az.dat",'a')
wz_el = open("data/wz_el.dat",'a')
yg_az = open("data/yg_az.dat",'a')
yg_el = open("data/yg_el.dat",'a')

az_c = 1
el_c = 1

for entry in matched:
    if entry[0] == "ft":
        az_slew = azelslew_calc.calcAz(ft_list, entry)
        el_slew = azelslew_calc.calcEl(ft_list, entry)
#        ft_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew*az_c:
            ft_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        elif az_slew*el_c < el_slew:
            ft_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
        else:
            pass

    elif entry[0] == "hb":
        az_slew = azelslew_calc.calcAz(hb_list, entry)
        el_slew = azelslew_calc.calcEl(hb_list, entry)
#        hb_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew*az_c:
            hb_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        elif az_slew*el_c < el_slew:
            hb_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
        else:
            pass

    elif entry[0] == "ht":
        az_slew = azelslew_calc.calcAz(ht_list, entry)
        el_slew = azelslew_calc.calcEl(ht_list, entry)
#        ht_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew*az_c:
            ht_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        elif az_slew*el_c < el_slew:
            ht_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
        else:
            pass

    elif entry[0] == "is":
        az_slew = azelslew_calc.calcAz(is_list, entry)
        el_slew = azelslew_calc.calcEl(is_list, entry)
#        is_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew*az_c:
            is_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        elif az_slew*el_c < el_slew:
            is_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
        else:
            pass

    elif entry[0] == "kb":
        az_slew = azelslew_calc.calcAz(kb_list, entry)
        el_slew = azelslew_calc.calcEl(kb_list, entry)
#        kb_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew*az_c:
            kb_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        elif az_slew*el_c < el_slew:
            kb_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
        else:
            pass

    elif entry[0] == "ke":
        az_slew = azelslew_calc.calcAz(ke_list, entry)
        el_slew = azelslew_calc.calcEl(ke_list, entry)
#        ke_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew*az_c:
            ke_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        elif az_slew*el_c < el_slew:
            ke_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
        else:
            pass

    elif entry[0] == "kk":
        az_slew = azelslew_calc.calcAz(kk_list, entry)
        el_slew = azelslew_calc.calcEl(kk_list, entry)
#        kk_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew*az_c:
            kk_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        elif az_slew*el_c < el_slew:
            kk_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
        else:
            pass

    elif entry[0] == "kv":
        az_slew = azelslew_calc.calcAz(kv_list, entry)
        el_slew = azelslew_calc.calcEl(kv_list, entry)
#        kv_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew*az_c:
            kv_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        elif az_slew*el_c < el_slew:
            kv_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
        else:
            pass

    elif entry[0] == "ma":
        az_slew = azelslew_calc.calcAz(ma_list, entry)
        el_slew = azelslew_calc.calcEl(ma_list, entry)
#        ma_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew*az_c:
            ma_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        elif az_slew*el_c < el_slew:
            ma_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
        else:
            pass

    elif entry[0] == "ny":
        az_slew = azelslew_calc.calcAz(ny_list, entry)
        el_slew = azelslew_calc.calcEl(ny_list, entry)
#        ny_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew*az_c:
            ny_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        elif az_slew*el_c < el_slew:
            ny_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
        else:
            pass

    elif entry[0] == "ts":
        az_slew = azelslew_calc.calcAz(ts_list, entry)
        el_slew = azelslew_calc.calcEl(ts_list, entry)
#        ts_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew*az_c:
            ts_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        elif az_slew*el_c < el_slew:
            ts_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
        else:
            pass

    elif entry[0] == "ww":
        az_slew = azelslew_calc.calcAz(ww_list, entry)
        el_slew = azelslew_calc.calcEl(ww_list, entry)
#        ww_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew*az_c:
            ww_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        elif az_slew*el_c < el_slew:
            ww_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
        else:
            pass

    elif entry[0] == "wn":
        az_slew = azelslew_calc.calcAz(wn_list, entry)
        el_slew = azelslew_calc.calcEl(wn_list, entry)
#        wn_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew*az_c:
            wn_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        elif az_slew*el_c < el_slew:
            wn_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
        else:
            pass

    elif entry[0] == "wz":
        az_slew = azelslew_calc.calcAz(wz_list, entry)
        el_slew = azelslew_calc.calcEl(wz_list, entry)
#        wz_slew.append(az_slew - el_slew)
        ## I/O
        if az_slew > el_slew*az_c:
            wz_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
        elif az_slew*el_c < el_slew:
            wz_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
        else:
            pass

    elif entry[0] == "yg":
        az_slew = azelslew_calc.calcAz(yg_list, entry)
        el_slew = azelslew_calc.calcEl(yg_list, entry)
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

