import time

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def getStationNames(path_to_file):
    
    source = open(path_to_file, 'r')
    stationList = source.readlines()
    source.close()
    
    stationName = []
    first = True
    
    for line in stationList:
        if line[0:1] == " ":
            st = line[80:82].strip().lower()
            if isNumber(st[0:1]):
                st = "a" + st
            stationName.append(st)
            
    main = open("extract.py", "w")
    
    main.write( \
"###############################################################################\n"+\
"# This is the main program for the program extractor.py. extractor.py takes   #\n"+\
"# as arguments one sked file summary for an arbitrary session, and one folder #\n"+\
"# containing the log files for the same session.                              #\n"+\
"#                                                                             #\n"+\
"# $> python extract.py skdfile logdir                                         #\n"+\
"#                                                                             #\n"+\
"# extract.py is well suited to be run by the bash script calculate_slew.sh    #\n"+\
"# which runs extract.py for all sessions present in the directories           #\n"+\
"# specified in the script.                                                    #\n"+\
"#                                                                             #\n"+\
"#                                                                             #\n"+\
"# Written by the Swedish Interns (Erik, Simon and Lina) the summer of 2016.   #\n"+\
"###############################################################################\n\n"+\
                "import os\n" + \
                "import sys\n" + \
                "import azelslew_calc\n" + \
                "from station_specs import *\n" + \
                "\n" + \
                "if not len(sys.argv) > 2:\n" +\
                "   print \"Wrong usage:\"\n" +\
                "   print \"$> python extract.py outputdir sessiondir\"\n" +\
                "   print \"You must supply the program with a folder containing the log \" \\\n" +\
                "        +\"files for the session, as well as the skd file for the same \" \\\n" +\
                "        +\"session.\"\n" +\
                "   sys.exit()\n" +\
                "\n" +\
                "path_to_output = sys.argv[1]\n" +\
                "path_to_dir = sys.argv[2]\n" +\
                "\n" +\
                "#######################################################\n" +\
                "# Start of program \n" +\
                "\n" +\
                "filename = \"\"\n" +\
                "nstations = 0\n" +\
                "log_data = []\n" +\
                "skd_data = []\n" +\
                "scheduled_stations = []\n" +\
                "matched = []\n" +\
                "\n" +\
                "nstations = azelslew_calc.getLogData(path_to_dir, log_data)\n" +\
                "azelslew_calc.getSkdData(path_to_dir, nstations, scheduled_stations, skd_data)\n" +\
                "azelslew_calc.matchSkdLog(log_data, skd_data, matched)\n" +\
                "\n" +\
                "az_c = 1\n" +\
                "el_c = 1\n" +\
                "\n" +\
                "## List of files to be written. Two files per station (az and el. ##)\n"+\
                "## Each line in the file contains: Model time, Real time, Delta Az/El, Station, Sked Time, Source.\n"+\
                "\n" +\
                "for entry in matched:\n" )

    for name in stationName:
        if first:
            main.write( \
                "   if entry[0] == \"" + name + "\":\n" +\
                "       " + name + "_az = open(path_to_output + \"/data/" + name + "_az.dat\", \'a\')\n" + \
                "       " + name + "_el = open(path_to_output + \"/data/" + name + "_el.dat\",\'a\')\n" +\
                "       az_slew = azelslew_calc.calcAz(" + name + "_list, entry)\n"+\
                "       el_slew = azelslew_calc.calcEl(" + name + "_list, entry)\n"+\
                "       if az_slew > el_slew*az_c:\n" +\
                "           " + name + "_az.write(str(az_slew) + \",\" + str(entry[1]) + \",\" + str(entry[2]) + \",\" + entry[0] + \",\" + str(entry[4]) + \",\" + str(entry[5]) + \'\\n\')\n" +\
                "       elif az_slew*el_c < el_slew:\n" +\
                "           " + name + "_el.write(str(el_slew) + \",\" + str(entry[1]) + \",\" + str(entry[3]) + \",\" + entry[0] + \",\" + str(entry[4]) + \",\" + str(entry[5]) + \'\\n\')\n" +\
                "       else:\n" +\
                "           pass\n" +\
                "       " + name + "_az.close()\n" +\
                "       " + name + "_el.close()\n" +\
                "\n")
            first = False
        else:
            main.write( \
                "   elif entry[0] == \"" + name + "\":\n" +\
                "       " + name + "_az = open(path_to_output + \"/data/" + name + "_az.dat\", \'a\')\n" + \
                "       " + name + "_el = open(path_to_output + \"/data/" + name + "_el.dat\",\'a\')\n" +\
                "       az_slew = azelslew_calc.calcAz(" + name + "_list, entry)\n"+\
                "       el_slew = azelslew_calc.calcEl(" + name + "_list, entry)\n"+\
                "       if az_slew > el_slew*az_c:\n" +\
                "           " + name + "_az.write(str(az_slew) + \",\" + str(entry[1]) + \",\" + str(entry[2]) + \",\" + entry[0] + \",\" + str(entry[4]) + \",\" + str(entry[5]) + \'\\n\')\n" +\
                "       elif az_slew*el_c < el_slew:\n" +\
                "           " + name + "_el.write(str(el_slew) + \",\" + str(entry[1]) + \",\" + str(entry[3]) + \",\" + entry[0] + \",\" + str(entry[4]) + \",\" + str(entry[5]) + \'\\n\')\n" +\
                "       else:\n" +\
                "           pass\n" +\
                "       " + name + "_az.close()\n" +\
                "       " + name + "_el.close()\n" +\
                "\n")
             
    main.write(\
                "   else:\n" +\
                "       print \"No specs for this antenna: \" + entry[0]\n" )
        
    main.close()
###############################################################################

getStationNames("./antenna.cat") 
