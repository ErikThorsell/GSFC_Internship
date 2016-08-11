###############################################################################
# This is the main program for the program extractor.py. extractor.py takes   #
# as arguments one sked file summary for an arbitrary session, and one folder #
# containing the log files for the same session.                              #
#                                                                             #
# $> python extract.py skdfile logdir                                         #
#                                                                             #
# extract.py is well suited to be run by the bash script calculate_slew.sh    #
# which runs extract.py for all sessions present in the directories           #
# specified in the script.                                                    #
#                                                                             #
#                                                                             #
# Written by the Swedish Interns (Erik, Simon and Lina) the summer of 2016.   #
###############################################################################

import os
import sys
import azelslew_calc
from station_specs import *

if not len(sys.argv) > 1:
   print "Wrong usage:"
   print "$> python extract.py logdir skdfile"
   print "You must supple the program with a folder containing the log " \
           +"files for the session, as well as the skd file for the same " \
           +"session."
   sys.exit()

logdir = sys.argv[1]
skddir = sys.argv[2]

#######################################################
# Start of program 

filename = ""
station = ""
nstations = 0
tups = []
scheduled_stations = []
theo = []
matched = []

nstations = azelslew_calc.getLogData(logdir, tups)
azelslew_calc.getSkdData(skddir, nstations, scheduled_stations, theo)
azelslew_calc.matchSkdLog(tups, theo, matched)

az_c = 1
el_c = 1

## List of files to be written. Two files per station (az and el. ##)

for entry in matched:
   if entry[0] == "ag":
       ag_az = open("data/ag_az.dat", 'a')
       ag_el = open("data/ag_el.dat",'a')
       az_slew = azelslew_calc.calcAz(ag_list, entry)
       el_slew = azelslew_calc.calcEl(ag_list, entry)
       if az_slew > el_slew*az_c:
           ag_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           ag_el.write(str(el_slew) + "," +str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       ag_az.close()
       ag_el.close()

   elif entry[0] == "ai":
       ai_az = open("data/ai_az.dat", 'a')
       ai_el = open("data/ai_el.dat",'a')
       az_slew = azelslew_calc.calcAz(ai_list, entry)
       el_slew = azelslew_calc.calcEl(ai_list, entry)
       if az_slew > el_slew*az_c:
           ai_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           ai_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       ai_az.close()
       ai_el.close()

   elif entry[0] == "ap":
       ap_az = open("data/ap_az.dat", 'a')
       ap_el = open("data/ap_el.dat",'a')
       az_slew = azelslew_calc.calcAz(ap_list, entry)
       el_slew = azelslew_calc.calcEl(ap_list, entry)
       if az_slew > el_slew*az_c:
           ap_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           ap_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       ap_az.close()
       ap_el.close()

   elif entry[0] == "ar":
       ar_az = open("data/ar_az.dat", 'a')
       ar_el = open("data/ar_el.dat",'a')
       az_slew = azelslew_calc.calcAz(ar_list, entry)
       el_slew = azelslew_calc.calcEl(ar_list, entry)
       if az_slew > el_slew*az_c:
           ar_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           ar_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       ar_az.close()
       ar_el.close()

   elif entry[0] == "tl":
       tl_az = open("data/tl_az.dat", 'a')
       tl_el = open("data/tl_el.dat",'a')
       az_slew = azelslew_calc.calcAz(tl_list, entry)
       el_slew = azelslew_calc.calcEl(tl_list, entry)
       if az_slew > el_slew*az_c:
           tl_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           tl_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       tl_az.close()
       tl_el.close()

   elif entry[0] == "yk":
       yk_az = open("data/yk_az.dat", 'a')
       yk_el = open("data/yk_el.dat",'a')
       az_slew = azelslew_calc.calcAz(yk_list, entry)
       el_slew = azelslew_calc.calcEl(yk_list, entry)
       if az_slew > el_slew*az_c:
           yk_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           yk_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       yk_az.close()
       yk_el.close()

   elif entry[0] == "at":
       at_az = open("data/at_az.dat", 'a')
       at_el = open("data/at_el.dat",'a')
       az_slew = azelslew_calc.calcAz(at_list, entry)
       el_slew = azelslew_calc.calcEl(at_list, entry)
       if az_slew > el_slew*az_c:
           at_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           at_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       at_az.close()
       at_el.close()

   elif entry[0] == "bd":
       bd_az = open("data/bd_az.dat", 'a')
       bd_el = open("data/bd_el.dat",'a')
       az_slew = azelslew_calc.calcAz(bd_list, entry)
       el_slew = azelslew_calc.calcEl(bd_list, entry)
       if az_slew > el_slew*az_c:
           bd_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           bd_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       bd_az.close()
       bd_el.close()

   elif entry[0] == "br":
       br_az = open("data/br_az.dat", 'a')
       br_el = open("data/br_el.dat",'a')
       az_slew = azelslew_calc.calcAz(br_list, entry)
       el_slew = azelslew_calc.calcEl(br_list, entry)
       if az_slew > el_slew*az_c:
           br_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           br_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       br_az.close()
       br_el.close()

   elif entry[0] == "ce":
       ce_az = open("data/ce_az.dat", 'a')
       ce_el = open("data/ce_el.dat",'a')
       az_slew = azelslew_calc.calcAz(ce_list, entry)
       el_slew = azelslew_calc.calcEl(ce_list, entry)
       if az_slew > el_slew*az_c:
           ce_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           ce_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       ce_az.close()
       ce_el.close()

   elif entry[0] == "cd":
       cd_az = open("data/cd_az.dat", 'a')
       cd_el = open("data/cd_el.dat",'a')
       az_slew = azelslew_calc.calcAz(cd_list, entry)
       el_slew = azelslew_calc.calcEl(cd_list, entry)
       if az_slew > el_slew*az_c:
           cd_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           cd_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       cd_az.close()
       cd_el.close()

   elif entry[0] == "cc":
       cc_az = open("data/cc_az.dat", 'a')
       cc_el = open("data/cc_el.dat",'a')
       az_slew = azelslew_calc.calcAz(cc_list, entry)
       el_slew = azelslew_calc.calcEl(cc_list, entry)
       if az_slew > el_slew*az_c:
           cc_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           cc_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       cc_az.close()
       cc_el.close()

   elif entry[0] == "ch":
       ch_az = open("data/ch_az.dat", 'a')
       ch_el = open("data/ch_el.dat",'a')
       az_slew = azelslew_calc.calcAz(ch_list, entry)
       el_slew = azelslew_calc.calcEl(ch_list, entry)
       if az_slew > el_slew*az_c:
           ch_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           ch_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       ch_az.close()
       ch_el.close()

   elif entry[0] == "sm":
       sm_az = open("data/sm_az.dat", 'a')
       sm_el = open("data/sm_el.dat",'a')
       az_slew = azelslew_calc.calcAz(sm_list, entry)
       el_slew = azelslew_calc.calcEl(sm_list, entry)
       if az_slew > el_slew*az_c:
           sm_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           sm_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       sm_az.close()
       sm_el.close()

   elif entry[0] == "sb":
       sb_az = open("data/sb_az.dat", 'a')
       sb_el = open("data/sb_el.dat",'a')
       az_slew = azelslew_calc.calcAz(sb_list, entry)
       el_slew = azelslew_calc.calcEl(sb_list, entry)
       if az_slew > el_slew*az_c:
           sb_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           sb_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       sb_az.close()
       sb_el.close()

   elif entry[0] == "a13":
       a13_az = open("data/a13_az.dat", 'a')
       a13_el = open("data/a13_el.dat",'a')
       az_slew = azelslew_calc.calcAz(a13_list, entry)
       el_slew = azelslew_calc.calcEl(a13_list, entry)
       if az_slew > el_slew*az_c:
           a13_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           a13_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       a13_az.close()
       a13_el.close()

   elif entry[0] == "a15":
       a15_az = open("data/a15_az.dat", 'a')
       a15_el = open("data/a15_el.dat",'a')
       az_slew = azelslew_calc.calcAz(a15_list, entry)
       el_slew = azelslew_calc.calcEl(a15_list, entry)
       if az_slew > el_slew*az_c:
           a15_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           a15_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       a15_az.close()
       a15_el.close()

   elif entry[0] == "a45":
       a45_az = open("data/a45_az.dat", 'a')
       a45_el = open("data/a45_el.dat",'a')
       az_slew = azelslew_calc.calcAz(a45_list, entry)
       el_slew = azelslew_calc.calcEl(a45_list, entry)
       if az_slew > el_slew*az_c:
           a45_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           a45_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       a45_az.close()
       a45_el.close()

   elif entry[0] == "a6a":
       a6a_az = open("data/a6a_az.dat", 'a')
       a6a_el = open("data/a6a_el.dat",'a')
       az_slew = azelslew_calc.calcAz(a6a_list, entry)
       el_slew = azelslew_calc.calcEl(a6a_list, entry)
       if az_slew > el_slew*az_c:
           a6a_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           a6a_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       a6a_az.close()
       a6a_el.close()

   elif entry[0] == "eb":
       eb_az = open("data/eb_az.dat", 'a')
       eb_el = open("data/eb_el.dat",'a')
       az_slew = azelslew_calc.calcAz(eb_list, entry)
       el_slew = azelslew_calc.calcEl(eb_list, entry)
       if az_slew > el_slew*az_c:
           eb_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           eb_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       eb_az.close()
       eb_el.close()

   elif entry[0] == "fd":
       fd_az = open("data/fd_az.dat", 'a')
       fd_el = open("data/fd_el.dat",'a')
       az_slew = azelslew_calc.calcAz(fd_list, entry)
       el_slew = azelslew_calc.calcEl(fd_list, entry)
       if az_slew > el_slew*az_c:
           fd_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           fd_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       fd_az.close()
       fd_el.close()

   elif entry[0] == "ft":
       ft_az = open("data/ft_az.dat", 'a')
       ft_el = open("data/ft_el.dat",'a')
       az_slew = azelslew_calc.calcAz(ft_list, entry)
       el_slew = azelslew_calc.calcEl(ft_list, entry)
       if az_slew > el_slew*az_c:
           ft_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           ft_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       ft_az.close()
       ft_el.close()

   elif entry[0] == "gs":
       gs_az = open("data/gs_az.dat", 'a')
       gs_el = open("data/gs_el.dat",'a')
       az_slew = azelslew_calc.calcAz(gs_list, entry)
       el_slew = azelslew_calc.calcEl(gs_list, entry)
       if az_slew > el_slew*az_c:
           gs_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           gs_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       gs_az.close()
       gs_el.close()

   elif entry[0] == "gc":
       gc_az = open("data/gc_az.dat", 'a')
       gc_el = open("data/gc_el.dat",'a')
       az_slew = azelslew_calc.calcAz(gc_list, entry)
       el_slew = azelslew_calc.calcEl(gc_list, entry)
       if az_slew > el_slew*az_c:
           gc_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           gc_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       gc_az.close()
       gc_el.close()

   elif entry[0] == "a14":
       a14_az = open("data/a14_az.dat", 'a')
       a14_el = open("data/a14_el.dat",'a')
       az_slew = azelslew_calc.calcAz(a14_list, entry)
       el_slew = azelslew_calc.calcEl(a14_list, entry)
       if az_slew > el_slew*az_c:
           a14_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           a14_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       a14_az.close()
       a14_el.close()

   elif entry[0] == "gv":
       gv_az = open("data/gv_az.dat", 'a')
       gv_el = open("data/gv_el.dat",'a')
       az_slew = azelslew_calc.calcAz(gv_list, entry)
       el_slew = azelslew_calc.calcEl(gv_list, entry)
       if az_slew > el_slew*az_c:
           gv_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           gv_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       gv_az.close()
       gv_el.close()

   elif entry[0] == "hh":
       hh_az = open("data/hh_az.dat", 'a')
       hh_el = open("data/hh_el.dat",'a')
       az_slew = azelslew_calc.calcAz(hh_list, entry)
       el_slew = azelslew_calc.calcEl(hh_list, entry)
       if az_slew > el_slew*az_c:
           hh_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           hh_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       hh_az.close()
       hh_el.close()

   elif entry[0] == "ht":
       ht_az = open("data/ht_az.dat", 'a')
       ht_el = open("data/ht_el.dat",'a')
       az_slew = azelslew_calc.calcAz(ht_list, entry)
       el_slew = azelslew_calc.calcEl(ht_list, entry)
       if az_slew > el_slew*az_c:
           ht_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           ht_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       ht_az.close()
       ht_el.close()

   elif entry[0] == "hc":
       hc_az = open("data/hc_az.dat", 'a')
       hc_el = open("data/hc_el.dat",'a')
       az_slew = azelslew_calc.calcAz(hc_list, entry)
       el_slew = azelslew_calc.calcEl(hc_list, entry)
       if az_slew > el_slew*az_c:
           hc_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           hc_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       hc_az.close()
       hc_el.close()

   elif entry[0] == "hs":
       hs_az = open("data/hs_az.dat", 'a')
       hs_el = open("data/hs_el.dat",'a')
       az_slew = azelslew_calc.calcAz(hs_list, entry)
       el_slew = azelslew_calc.calcEl(hs_list, entry)
       if az_slew > el_slew*az_c:
           hs_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           hs_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       hs_az.close()
       hs_el.close()

   elif entry[0] == "hn":
       hn_az = open("data/hn_az.dat", 'a')
       hn_el = open("data/hn_el.dat",'a')
       az_slew = azelslew_calc.calcAz(hn_list, entry)
       el_slew = azelslew_calc.calcEl(hn_list, entry)
       if az_slew > el_slew*az_c:
           hn_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           hn_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       hn_az.close()
       hn_el.close()

   elif entry[0] == "hb":
       hb_az = open("data/hb_az.dat", 'a')
       hb_el = open("data/hb_el.dat",'a')
       az_slew = azelslew_calc.calcAz(hb_list, entry)
       el_slew = azelslew_calc.calcEl(hb_list, entry)
       if az_slew > el_slew*az_c:
           hb_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           hb_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       hb_az.close()
       hb_el.close()

   elif entry[0] == "ho":
       ho_az = open("data/ho_az.dat", 'a')
       ho_el = open("data/ho_el.dat",'a')
       az_slew = azelslew_calc.calcAz(ho_list, entry)
       el_slew = azelslew_calc.calcEl(ho_list, entry)
       if az_slew > el_slew*az_c:
           ho_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           ho_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       ho_az.close()
       ho_el.close()

   elif entry[0] == "is":
       is_az = open("data/is_az.dat", 'a')
       is_el = open("data/is_el.dat",'a')
       az_slew = azelslew_calc.calcAz(is_list, entry)
       el_slew = azelslew_calc.calcEl(is_list, entry)
       if az_slew > el_slew*az_c:
           is_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           is_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       is_az.close()
       is_el.close()

   elif entry[0] == "it":
       it_az = open("data/it_az.dat", 'a')
       it_el = open("data/it_el.dat",'a')
       az_slew = azelslew_calc.calcAz(it_list, entry)
       el_slew = azelslew_calc.calcEl(it_list, entry)
       if az_slew > el_slew*az_c:
           it_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           it_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       it_az.close()
       it_el.close()

   elif entry[0] == "jb":
       jb_az = open("data/jb_az.dat", 'a')
       jb_el = open("data/jb_el.dat",'a')
       az_slew = azelslew_calc.calcAz(jb_list, entry)
       el_slew = azelslew_calc.calcEl(jb_list, entry)
       if az_slew > el_slew*az_c:
           jb_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           jb_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       jb_az.close()
       jb_el.close()

   elif entry[0] == "kb":
       kb_az = open("data/kb_az.dat", 'a')
       kb_el = open("data/kb_el.dat",'a')
       az_slew = azelslew_calc.calcAz(kb_list, entry)
       el_slew = azelslew_calc.calcEl(kb_list, entry)
       if az_slew > el_slew*az_c:
           kb_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           kb_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       kb_az.close()
       kb_el.close()

   elif entry[0] == "k1":
       k1_az = open("data/k1_az.dat", 'a')
       k1_el = open("data/k1_el.dat",'a')
       az_slew = azelslew_calc.calcAz(k1_list, entry)
       el_slew = azelslew_calc.calcEl(k1_list, entry)
       if az_slew > el_slew*az_c:
           k1_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           k1_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       k1_az.close()
       k1_el.close()

   elif entry[0] == "ke":
       ke_az = open("data/ke_az.dat", 'a')
       ke_el = open("data/ke_el.dat",'a')
       az_slew = azelslew_calc.calcAz(ke_list, entry)
       el_slew = azelslew_calc.calcEl(ke_list, entry)
       if az_slew > el_slew*az_c:
           ke_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           ke_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       ke_az.close()
       ke_el.close()

   elif entry[0] == "ku":
       ku_az = open("data/ku_az.dat", 'a')
       ku_el = open("data/ku_el.dat",'a')
       az_slew = azelslew_calc.calcAz(ku_list, entry)
       el_slew = azelslew_calc.calcEl(ku_list, entry)
       if az_slew > el_slew*az_c:
           ku_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           ku_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       ku_az.close()
       ku_el.close()

   elif entry[0] == "kk":
       kk_az = open("data/kk_az.dat", 'a')
       kk_el = open("data/kk_el.dat",'a')
       az_slew = azelslew_calc.calcAz(kk_list, entry)
       el_slew = azelslew_calc.calcEl(kk_list, entry)
       if az_slew > el_slew*az_c:
           kk_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           kk_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       kk_az.close()
       kk_el.close()

   elif entry[0] == "k2":
       k2_az = open("data/k2_az.dat", 'a')
       k2_el = open("data/k2_el.dat",'a')
       az_slew = azelslew_calc.calcAz(k2_list, entry)
       el_slew = azelslew_calc.calcEl(k2_list, entry)
       if az_slew > el_slew*az_c:
           k2_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           k2_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       k2_az.close()
       k2_el.close()

   elif entry[0] == "kt":
       kt_az = open("data/kt_az.dat", 'a')
       kt_el = open("data/kt_el.dat",'a')
       az_slew = azelslew_calc.calcAz(kt_list, entry)
       el_slew = azelslew_calc.calcEl(kt_list, entry)
       if az_slew > el_slew*az_c:
           kt_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           kt_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       kt_az.close()
       kt_el.close()

   elif entry[0] == "km":
       km_az = open("data/km_az.dat", 'a')
       km_el = open("data/km_el.dat",'a')
       az_slew = azelslew_calc.calcAz(km_list, entry)
       el_slew = azelslew_calc.calcEl(km_list, entry)
       if az_slew > el_slew*az_c:
           km_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           km_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       km_az.close()
       km_el.close()

   elif entry[0] == "kp":
       kp_az = open("data/kp_az.dat", 'a')
       kp_el = open("data/kp_el.dat",'a')
       az_slew = azelslew_calc.calcAz(kp_list, entry)
       el_slew = azelslew_calc.calcEl(kp_list, entry)
       if az_slew > el_slew*az_c:
           kp_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           kp_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       kp_az.close()
       kp_el.close()

   elif entry[0] == "kg":
       kg_az = open("data/kg_az.dat", 'a')
       kg_el = open("data/kg_el.dat",'a')
       az_slew = azelslew_calc.calcAz(kg_list, entry)
       el_slew = azelslew_calc.calcEl(kg_list, entry)
       if az_slew > el_slew*az_c:
           kg_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           kg_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       kg_az.close()
       kg_el.close()

   elif entry[0] == "kw":
       kw_az = open("data/kw_az.dat", 'a')
       kw_el = open("data/kw_el.dat",'a')
       az_slew = azelslew_calc.calcAz(kw_list, entry)
       el_slew = azelslew_calc.calcEl(kw_list, entry)
       if az_slew > el_slew*az_c:
           kw_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           kw_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       kw_az.close()
       kw_el.close()

   elif entry[0] == "la":
       la_az = open("data/la_az.dat", 'a')
       la_el = open("data/la_el.dat",'a')
       az_slew = azelslew_calc.calcAz(la_list, entry)
       el_slew = azelslew_calc.calcEl(la_list, entry)
       if az_slew > el_slew*az_c:
           la_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           la_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       la_az.close()
       la_el.close()

   elif entry[0] == "ro":
       ro_az = open("data/ro_az.dat", 'a')
       ro_el = open("data/ro_el.dat",'a')
       az_slew = azelslew_calc.calcAz(ro_list, entry)
       el_slew = azelslew_calc.calcEl(ro_list, entry)
       if az_slew > el_slew*az_c:
           ro_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           ro_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       ro_az.close()
       ro_el.close()

   elif entry[0] == "mr":
       mr_az = open("data/mr_az.dat", 'a')
       mr_el = open("data/mr_el.dat",'a')
       az_slew = azelslew_calc.calcAz(mr_list, entry)
       el_slew = azelslew_calc.calcEl(mr_list, entry)
       if az_slew > el_slew*az_c:
           mr_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           mr_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       mr_az.close()
       mr_el.close()

   elif entry[0] == "md":
       md_az = open("data/md_az.dat", 'a')
       md_el = open("data/md_el.dat",'a')
       az_slew = azelslew_calc.calcAz(md_list, entry)
       el_slew = azelslew_calc.calcEl(md_list, entry)
       if az_slew > el_slew*az_c:
           md_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           md_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       md_az.close()
       md_el.close()

   elif entry[0] == "ma":
       ma_az = open("data/ma_az.dat", 'a')
       ma_el = open("data/ma_el.dat",'a')
       az_slew = azelslew_calc.calcAz(ma_list, entry)
       el_slew = azelslew_calc.calcEl(ma_list, entry)
       if az_slew > el_slew*az_c:
           ma_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           ma_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       ma_az.close()
       ma_el.close()

   elif entry[0] == "mc":
       mc_az = open("data/mc_az.dat", 'a')
       mc_el = open("data/mc_el.dat",'a')
       az_slew = azelslew_calc.calcAz(mc_list, entry)
       el_slew = azelslew_calc.calcEl(mc_list, entry)
       if az_slew > el_slew*az_c:
           mc_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           mc_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       mc_az.close()
       mc_el.close()

   elif entry[0] == "mh":
       mh_az = open("data/mh_az.dat", 'a')
       mh_el = open("data/mh_el.dat",'a')
       az_slew = azelslew_calc.calcAz(mh_list, entry)
       el_slew = azelslew_calc.calcEl(mh_list, entry)
       if az_slew > el_slew*az_c:
           mh_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           mh_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       mh_az.close()
       mh_el.close()

   elif entry[0] == "mi":
       mi_az = open("data/mi_az.dat", 'a')
       mi_el = open("data/mi_el.dat",'a')
       az_slew = azelslew_calc.calcAz(mi_list, entry)
       el_slew = azelslew_calc.calcEl(mi_list, entry)
       if az_slew > el_slew*az_c:
           mi_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           mi_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       mi_az.close()
       mi_el.close()

   elif entry[0] == "mu":
       mu_az = open("data/mu_az.dat", 'a')
       mu_el = open("data/mu_el.dat",'a')
       az_slew = azelslew_calc.calcAz(mu_list, entry)
       el_slew = azelslew_calc.calcEl(mu_list, entry)
       if az_slew > el_slew*az_c:
           mu_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           mu_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       mu_az.close()
       mu_el.close()

   elif entry[0] == "mz":
       mz_az = open("data/mz_az.dat", 'a')
       mz_el = open("data/mz_el.dat",'a')
       az_slew = azelslew_calc.calcAz(mz_list, entry)
       el_slew = azelslew_calc.calcEl(mz_list, entry)
       if az_slew > el_slew*az_c:
           mz_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           mz_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       mz_az.close()
       mz_el.close()

   elif entry[0] == "mn":
       mn_az = open("data/mn_az.dat", 'a')
       mn_el = open("data/mn_el.dat",'a')
       az_slew = azelslew_calc.calcAz(mn_list, entry)
       el_slew = azelslew_calc.calcEl(mn_list, entry)
       if az_slew > el_slew*az_c:
           mn_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           mn_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       mn_az.close()
       mn_el.close()

   elif entry[0] == "mk":
       mk_az = open("data/mk_az.dat", 'a')
       mk_el = open("data/mk_el.dat",'a')
       az_slew = azelslew_calc.calcAz(mk_list, entry)
       el_slew = azelslew_calc.calcEl(mk_list, entry)
       if az_slew > el_slew*az_c:
           mk_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           mk_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       mk_az.close()
       mk_el.close()

   elif entry[0] == "mo":
       mo_az = open("data/mo_az.dat", 'a')
       mo_el = open("data/mo_el.dat",'a')
       az_slew = azelslew_calc.calcAz(mo_list, entry)
       el_slew = azelslew_calc.calcEl(mo_list, entry)
       if az_slew > el_slew*az_c:
           mo_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           mo_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       mo_az.close()
       mo_el.close()

   elif entry[0] == "mp":
       mp_az = open("data/mp_az.dat", 'a')
       mp_el = open("data/mp_el.dat",'a')
       az_slew = azelslew_calc.calcAz(mp_list, entry)
       el_slew = azelslew_calc.calcEl(mp_list, entry)
       if az_slew > el_slew*az_c:
           mp_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           mp_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       mp_az.close()
       mp_el.close()

   elif entry[0] == "nl":
       nl_az = open("data/nl_az.dat", 'a')
       nl_el = open("data/nl_el.dat",'a')
       az_slew = azelslew_calc.calcAz(nl_list, entry)
       el_slew = azelslew_calc.calcEl(nl_list, entry)
       if az_slew > el_slew*az_c:
           nl_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           nl_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       nl_az.close()
       nl_el.close()

   elif entry[0] == "no":
       no_az = open("data/no_az.dat", 'a')
       no_el = open("data/no_el.dat",'a')
       az_slew = azelslew_calc.calcAz(no_list, entry)
       el_slew = azelslew_calc.calcEl(no_list, entry)
       if az_slew > el_slew*az_c:
           no_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           no_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       no_az.close()
       no_el.close()

   elif entry[0] == "nt":
       nt_az = open("data/nt_az.dat", 'a')
       nt_el = open("data/nt_el.dat",'a')
       az_slew = azelslew_calc.calcAz(nt_list, entry)
       el_slew = azelslew_calc.calcEl(nt_list, entry)
       if az_slew > el_slew*az_c:
           nt_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           nt_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       nt_az.close()
       nt_el.close()

   elif entry[0] == "g3":
       g3_az = open("data/g3_az.dat", 'a')
       g3_el = open("data/g3_el.dat",'a')
       az_slew = azelslew_calc.calcAz(g3_list, entry)
       el_slew = azelslew_calc.calcEl(g3_list, entry)
       if az_slew > el_slew*az_c:
           g3_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           g3_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       g3_az.close()
       g3_el.close()

   elif entry[0] == "gb":
       gb_az = open("data/gb_az.dat", 'a')
       gb_el = open("data/gb_el.dat",'a')
       az_slew = azelslew_calc.calcAz(gb_list, entry)
       el_slew = azelslew_calc.calcEl(gb_list, entry)
       if az_slew > el_slew*az_c:
           gb_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           gb_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       gb_az.close()
       gb_el.close()

   elif entry[0] == "gt":
       gt_az = open("data/gt_az.dat", 'a')
       gt_el = open("data/gt_el.dat",'a')
       az_slew = azelslew_calc.calcAz(gt_list, entry)
       el_slew = azelslew_calc.calcEl(gt_list, entry)
       if az_slew > el_slew*az_c:
           gt_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           gt_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       gt_az.close()
       gt_el.close()

   elif entry[0] == "gn":
       gn_az = open("data/gn_az.dat", 'a')
       gn_el = open("data/gn_el.dat",'a')
       az_slew = azelslew_calc.calcAz(gn_list, entry)
       el_slew = azelslew_calc.calcEl(gn_list, entry)
       if az_slew > el_slew*az_c:
           gn_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           gn_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       gn_az.close()
       gn_el.close()

   elif entry[0] == "ny":
       ny_az = open("data/ny_az.dat", 'a')
       ny_el = open("data/ny_el.dat",'a')
       az_slew = azelslew_calc.calcAz(ny_list, entry)
       el_slew = azelslew_calc.calcEl(ny_list, entry)
       if az_slew > el_slew*az_c:
           ny_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           ny_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       ny_az.close()
       ny_el.close()

   elif entry[0] == "oh":
       oh_az = open("data/oh_az.dat", 'a')
       oh_el = open("data/oh_el.dat",'a')
       az_slew = azelslew_calc.calcAz(oh_list, entry)
       el_slew = azelslew_calc.calcEl(oh_list, entry)
       if az_slew > el_slew*az_c:
           oh_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           oh_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       oh_az.close()
       oh_el.close()

   elif entry[0] == "on":
       on_az = open("data/on_az.dat", 'a')
       on_el = open("data/on_el.dat",'a')
       az_slew = azelslew_calc.calcAz(on_list, entry)
       el_slew = azelslew_calc.calcEl(on_list, entry)
       if az_slew > el_slew*az_c:
           on_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           on_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       on_az.close()
       on_el.close()

   elif entry[0] == "o8":
       o8_az = open("data/o8_az.dat", 'a')
       o8_el = open("data/o8_el.dat",'a')
       az_slew = azelslew_calc.calcAz(o8_list, entry)
       el_slew = azelslew_calc.calcEl(o8_list, entry)
       if az_slew > el_slew*az_c:
           o8_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           o8_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       o8_az.close()
       o8_el.close()

   elif entry[0] == "gg":
       gg_az = open("data/gg_az.dat", 'a')
       gg_el = open("data/gg_el.dat",'a')
       az_slew = azelslew_calc.calcAz(gg_list, entry)
       el_slew = azelslew_calc.calcEl(gg_list, entry)
       if az_slew > el_slew*az_c:
           gg_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           gg_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       gg_az.close()
       gg_el.close()

   elif entry[0] == "ov":
       ov_az = open("data/ov_az.dat", 'a')
       ov_el = open("data/ov_el.dat",'a')
       az_slew = azelslew_calc.calcAz(ov_list, entry)
       el_slew = azelslew_calc.calcEl(ov_list, entry)
       if az_slew > el_slew*az_c:
           ov_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           ov_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       ov_az.close()
       ov_el.close()

   elif entry[0] == "oo":
       oo_az = open("data/oo_az.dat", 'a')
       oo_el = open("data/oo_el.dat",'a')
       az_slew = azelslew_calc.calcAz(oo_list, entry)
       el_slew = azelslew_calc.calcEl(oo_list, entry)
       if az_slew > el_slew*az_c:
           oo_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           oo_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       oo_az.close()
       oo_el.close()

   elif entry[0] == "pa":
       pa_az = open("data/pa_az.dat", 'a')
       pa_el = open("data/pa_el.dat",'a')
       az_slew = azelslew_calc.calcAz(pa_list, entry)
       el_slew = azelslew_calc.calcEl(pa_list, entry)
       if az_slew > el_slew*az_c:
           pa_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           pa_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       pa_az.close()
       pa_el.close()

   elif entry[0] == "pe":
       pe_az = open("data/pe_az.dat", 'a')
       pe_el = open("data/pe_el.dat",'a')
       az_slew = azelslew_calc.calcAz(pe_list, entry)
       el_slew = azelslew_calc.calcEl(pe_list, entry)
       if az_slew > el_slew*az_c:
           pe_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           pe_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       pe_az.close()
       pe_el.close()

   elif entry[0] == "pt":
       pt_az = open("data/pt_az.dat", 'a')
       pt_el = open("data/pt_el.dat",'a')
       az_slew = azelslew_calc.calcAz(pt_list, entry)
       el_slew = azelslew_calc.calcEl(pt_list, entry)
       if az_slew > el_slew*az_c:
           pt_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           pt_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       pt_az.close()
       pt_el.close()

   elif entry[0] == "qb":
       qb_az = open("data/qb_az.dat", 'a')
       qb_el = open("data/qb_el.dat",'a')
       az_slew = azelslew_calc.calcAz(qb_list, entry)
       el_slew = azelslew_calc.calcEl(qb_list, entry)
       if az_slew > el_slew*az_c:
           qb_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           qb_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       qb_az.close()
       qb_el.close()

   elif entry[0] == "yj":
       yj_az = open("data/yj_az.dat", 'a')
       yj_el = open("data/yj_el.dat",'a')
       az_slew = azelslew_calc.calcAz(yj_list, entry)
       el_slew = azelslew_calc.calcEl(yj_list, entry)
       if az_slew > el_slew*az_c:
           yj_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           yj_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       yj_az.close()
       yj_el.close()

   elif entry[0] == "a61":
       a61_az = open("data/a61_az.dat", 'a')
       a61_el = open("data/a61_el.dat",'a')
       az_slew = azelslew_calc.calcAz(a61_list, entry)
       el_slew = azelslew_calc.calcEl(a61_list, entry)
       if az_slew > el_slew*az_c:
           a61_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           a61_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       a61_az.close()
       a61_el.close()

   elif entry[0] == "st":
       st_az = open("data/st_az.dat", 'a')
       st_el = open("data/st_el.dat",'a')
       az_slew = azelslew_calc.calcAz(st_list, entry)
       el_slew = azelslew_calc.calcEl(st_list, entry)
       if az_slew > el_slew*az_c:
           st_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           st_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       st_az.close()
       st_el.close()

   elif entry[0] == "sc":
       sc_az = open("data/sc_az.dat", 'a')
       sc_el = open("data/sc_el.dat",'a')
       az_slew = azelslew_calc.calcAz(sc_list, entry)
       el_slew = azelslew_calc.calcEl(sc_list, entry)
       if az_slew > el_slew*az_c:
           sc_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           sc_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       sc_az.close()
       sc_el.close()

   elif entry[0] == "s3":
       s3_az = open("data/s3_az.dat", 'a')
       s3_el = open("data/s3_el.dat",'a')
       az_slew = azelslew_calc.calcAz(s3_list, entry)
       el_slew = azelslew_calc.calcEl(s3_list, entry)
       if az_slew > el_slew*az_c:
           s3_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           s3_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       s3_az.close()
       s3_el.close()

   elif entry[0] == "kv":
       kv_az = open("data/kv_az.dat", 'a')
       kv_el = open("data/kv_el.dat",'a')
       az_slew = azelslew_calc.calcAz(kv_list, entry)
       el_slew = azelslew_calc.calcEl(kv_list, entry)
       if az_slew > el_slew*az_c:
           kv_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           kv_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       kv_az.close()
       kv_el.close()

   elif entry[0] == "sh":
       sh_az = open("data/sh_az.dat", 'a')
       sh_el = open("data/sh_el.dat",'a')
       az_slew = azelslew_calc.calcAz(sh_list, entry)
       el_slew = azelslew_calc.calcEl(sh_list, entry)
       if az_slew > el_slew*az_c:
           sh_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           sh_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       sh_az.close()
       sh_el.close()

   elif entry[0] == "se":
       se_az = open("data/se_az.dat", 'a')
       se_el = open("data/se_el.dat",'a')
       az_slew = azelslew_calc.calcAz(se_list, entry)
       el_slew = azelslew_calc.calcEl(se_list, entry)
       if az_slew > el_slew*az_c:
           se_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           se_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       se_az.close()
       se_el.close()

   elif entry[0] == "sy":
       sy_az = open("data/sy_az.dat", 'a')
       sy_el = open("data/sy_el.dat",'a')
       az_slew = azelslew_calc.calcAz(sy_list, entry)
       el_slew = azelslew_calc.calcEl(sy_list, entry)
       if az_slew > el_slew*az_c:
           sy_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           sy_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       sy_az.close()
       sy_el.close()

   elif entry[0] == "sv":
       sv_az = open("data/sv_az.dat", 'a')
       sv_el = open("data/sv_el.dat",'a')
       az_slew = azelslew_calc.calcAz(sv_list, entry)
       el_slew = azelslew_calc.calcEl(sv_list, entry)
       if az_slew > el_slew*az_c:
           sv_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           sv_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       sv_az.close()
       sv_el.close()

   elif entry[0] == "ta":
       ta_az = open("data/ta_az.dat", 'a')
       ta_el = open("data/ta_el.dat",'a')
       az_slew = azelslew_calc.calcAz(ta_list, entry)
       el_slew = azelslew_calc.calcEl(ta_list, entry)
       if az_slew > el_slew*az_c:
           ta_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           ta_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       ta_az.close()
       ta_el.close()

   elif entry[0] == "t6":
       t6_az = open("data/t6_az.dat", 'a')
       t6_el = open("data/t6_el.dat",'a')
       az_slew = azelslew_calc.calcAz(t6_list, entry)
       el_slew = azelslew_calc.calcEl(t6_list, entry)
       if az_slew > el_slew*az_c:
           t6_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           t6_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       t6_az.close()
       t6_el.close()

   elif entry[0] == "ti":
       ti_az = open("data/ti_az.dat", 'a')
       ti_el = open("data/ti_el.dat",'a')
       az_slew = azelslew_calc.calcAz(ti_list, entry)
       el_slew = azelslew_calc.calcEl(ti_list, entry)
       if az_slew > el_slew*az_c:
           ti_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           ti_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       ti_az.close()
       ti_el.close()

   elif entry[0] == "tc":
       tc_az = open("data/tc_az.dat", 'a')
       tc_el = open("data/tc_el.dat",'a')
       az_slew = azelslew_calc.calcAz(tc_list, entry)
       el_slew = azelslew_calc.calcEl(tc_list, entry)
       if az_slew > el_slew*az_c:
           tc_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           tc_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       tc_az.close()
       tc_el.close()

   elif entry[0] == "tr":
       tr_az = open("data/tr_az.dat", 'a')
       tr_el = open("data/tr_el.dat",'a')
       az_slew = azelslew_calc.calcAz(tr_list, entry)
       el_slew = azelslew_calc.calcEl(tr_list, entry)
       if az_slew > el_slew*az_c:
           tr_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           tr_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       tr_az.close()
       tr_el.close()

   elif entry[0] == "ts":
       ts_az = open("data/ts_az.dat", 'a')
       ts_el = open("data/ts_el.dat",'a')
       az_slew = azelslew_calc.calcAz(ts_list, entry)
       el_slew = azelslew_calc.calcEl(ts_list, entry)
       if az_slew > el_slew*az_c:
           ts_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           ts_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       ts_az.close()
       ts_el.close()

   elif entry[0] == "uc":
       uc_az = open("data/uc_az.dat", 'a')
       uc_el = open("data/uc_el.dat",'a')
       az_slew = azelslew_calc.calcAz(uc_list, entry)
       el_slew = azelslew_calc.calcEl(uc_list, entry)
       if az_slew > el_slew*az_c:
           uc_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           uc_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       uc_az.close()
       uc_el.close()

   elif entry[0] == "ur":
       ur_az = open("data/ur_az.dat", 'a')
       ur_el = open("data/ur_el.dat",'a')
       az_slew = azelslew_calc.calcAz(ur_list, entry)
       el_slew = azelslew_calc.calcEl(ur_list, entry)
       if az_slew > el_slew*az_c:
           ur_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           ur_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       ur_az.close()
       ur_el.close()

   elif entry[0] == "us":
       us_az = open("data/us_az.dat", 'a')
       us_el = open("data/us_el.dat",'a')
       az_slew = azelslew_calc.calcAz(us_list, entry)
       el_slew = azelslew_calc.calcEl(us_list, entry)
       if az_slew > el_slew*az_c:
           us_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           us_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       us_az.close()
       us_el.close()

   elif entry[0] == "vs":
       vs_az = open("data/vs_az.dat", 'a')
       vs_el = open("data/vs_el.dat",'a')
       az_slew = azelslew_calc.calcAz(vs_list, entry)
       el_slew = azelslew_calc.calcEl(vs_list, entry)
       if az_slew > el_slew*az_c:
           vs_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           vs_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       vs_az.close()
       vs_el.close()

   elif entry[0] == "vm":
       vm_az = open("data/vm_az.dat", 'a')
       vm_el = open("data/vm_el.dat",'a')
       az_slew = azelslew_calc.calcAz(vm_list, entry)
       el_slew = azelslew_calc.calcEl(vm_list, entry)
       if az_slew > el_slew*az_c:
           vm_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           vm_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       vm_az.close()
       vm_el.close()

   elif entry[0] == "y1":
       y1_az = open("data/y1_az.dat", 'a')
       y1_el = open("data/y1_el.dat",'a')
       az_slew = azelslew_calc.calcAz(y1_list, entry)
       el_slew = azelslew_calc.calcEl(y1_list, entry)
       if az_slew > el_slew*az_c:
           y1_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           y1_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       y1_az.close()
       y1_el.close()

   elif entry[0] == "ww":
       ww_az = open("data/ww_az.dat", 'a')
       ww_el = open("data/ww_el.dat",'a')
       az_slew = azelslew_calc.calcAz(ww_list, entry)
       el_slew = azelslew_calc.calcEl(ww_list, entry)
       if az_slew > el_slew*az_c:
           ww_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           ww_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       ww_az.close()
       ww_el.close()

   elif entry[0] == "wf":
       wf_az = open("data/wf_az.dat", 'a')
       wf_el = open("data/wf_el.dat",'a')
       az_slew = azelslew_calc.calcAz(wf_list, entry)
       el_slew = azelslew_calc.calcEl(wf_list, entry)
       if az_slew > el_slew*az_c:
           wf_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           wf_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       wf_az.close()
       wf_el.close()

   elif entry[0] == "wb":
       wb_az = open("data/wb_az.dat", 'a')
       wb_el = open("data/wb_el.dat",'a')
       az_slew = azelslew_calc.calcAz(wb_list, entry)
       el_slew = azelslew_calc.calcEl(wb_list, entry)
       if az_slew > el_slew*az_c:
           wb_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           wb_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       wb_az.close()
       wb_el.close()

   elif entry[0] == "wn":
       wn_az = open("data/wn_az.dat", 'a')
       wn_el = open("data/wn_el.dat",'a')
       az_slew = azelslew_calc.calcAz(wn_list, entry)
       el_slew = azelslew_calc.calcEl(wn_list, entry)
       if az_slew > el_slew*az_c:
           wn_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           wn_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       wn_az.close()
       wn_el.close()

   elif entry[0] == "ws":
       ws_az = open("data/ws_az.dat", 'a')
       ws_el = open("data/ws_el.dat",'a')
       az_slew = azelslew_calc.calcAz(ws_list, entry)
       el_slew = azelslew_calc.calcEl(ws_list, entry)
       if az_slew > el_slew*az_c:
           ws_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           ws_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       ws_az.close()
       ws_el.close()

   elif entry[0] == "wz":
       wz_az = open("data/wz_az.dat", 'a')
       wz_el = open("data/wz_el.dat",'a')
       az_slew = azelslew_calc.calcAz(wz_list, entry)
       el_slew = azelslew_calc.calcEl(wz_list, entry)
       if az_slew > el_slew*az_c:
           wz_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           wz_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       wz_az.close()
       wz_el.close()

   elif entry[0] == "yg":
       yg_az = open("data/yg_az.dat", 'a')
       yg_el = open("data/yg_el.dat",'a')
       az_slew = azelslew_calc.calcAz(yg_list, entry)
       el_slew = azelslew_calc.calcEl(yg_list, entry)
       if az_slew > el_slew*az_c:
           yg_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           yg_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       yg_az.close()
       yg_el.close()

   elif entry[0] == "ys":
       ys_az = open("data/ys_az.dat", 'a')
       ys_el = open("data/ys_el.dat",'a')
       az_slew = azelslew_calc.calcAz(ys_list, entry)
       el_slew = azelslew_calc.calcEl(ys_list, entry)
       if az_slew > el_slew*az_c:
           ys_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           ys_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       ys_az.close()
       ys_el.close()

   elif entry[0] == "zc":
       zc_az = open("data/zc_az.dat", 'a')
       zc_el = open("data/zc_el.dat",'a')
       az_slew = azelslew_calc.calcAz(zc_list, entry)
       el_slew = azelslew_calc.calcEl(zc_list, entry)
       if az_slew > el_slew*az_c:
           zc_az.write(str(az_slew) + "," + str(entry[1]) + "," + str(entry[2]) + '\n')
       elif az_slew*el_c < el_slew:
           zc_el.write(str(el_slew) + "," + str(entry[1]) + "," + str(entry[3]) + '\n')
       else:
           pass
       zc_az.close()
       zc_el.close()

   else:
       print "No specs for this antenna: " + entry[0]
