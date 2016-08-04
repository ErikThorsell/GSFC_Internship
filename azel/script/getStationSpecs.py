import time

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def parseStationData(specs):
    id = ""
    name = ""
    axis = ""
    offset = ""
    az_speed = 0
    az_acc = 0
    az_min = 0
    az_max = 0
    el_speed = 0
    el_acc = 0
    el_min = 0
    el_max = 0
    diam = 0
    PO = ""
    EQ = ""
    MS = ""

    for line in specs:
        if line[0:1] == " ":
            id = line[1:2]
            name = line[3:7].strip()
            axis = line[12:16]
            offset = float(line[18:26])
            az_speed = float(line[27:32])
            az_acc = float(line[33:36])
            az_min = float(line[37:43])
            az_max = float(line[44:50])
            el_speed = float(line[51:57])
            el_acc = float(line[58:61])
            el_min = float(line[62:67])
            el_max = float(line[69:73])
            diam = float(line[74:79])
            PO = line[80:82].strip().lower()
            EQ = line[83:86].strip().lower()
            MS = line[87:89].strip().lower()
            if isNumber(PO[0:1]):
                PO = "a" + PO
            sp.write("# " + name + "\n" + \
                     "# Axis: " + axis + "\n" + \
                     "# Offset: " + str(offset) + "\n" + \
                     "# Diam: " + str(diam) + "\n" + \
                     PO + "_az = (" + str(az_min) + ", " + str(az_max) + ")\n" + \
                     PO + "_el = (" + str(el_min) + ", " + str(el_max) + ")\n" + \
                     PO + "_azspeed = " + str(az_speed) + "\n" + \
                     PO + "_elspeed = " + str(el_speed) + "\n" + \
                     PO + "_azspeed_acc = " + str(az_acc) + "\n" + \
                     PO + "_elspeed_acc = " + str(el_acc) + "\n" + \
                     PO + "_list = [" + PO + "_az, " + PO + "_el, " + \
                     PO + "_azspeed, " + PO + "_elspeed, " + \
                     PO + "_azspeed_acc, " + PO + "_elspeed_acc]" + \
                     "\n\n"
                     )

def getStationData(path_to_file):

    specs = open(path_to_file, 'r')
    sourcelines = specs.readlines()
    specs.close()

    parseStationData(sourcelines)

###############################################################################
sp = open("station_specs.py",'w')
sp.write( \
    "###############################################################################\n" + \
    "# This is an automatically generated spec file (created by the script         #\n" + \
    "# getStationSpecs.py). The data is taken from the file antenna.cat. It        #\n" + \
    "# should be fine, but use at own risk!                                        #\n" + \
    "#                                                                             #\n" + \
    "#                                                                             #\n" + \
    "# This version of the spec file was generated on: " + time.strftime("%Y-%m-%d") + \
    "                  #\n" + \
    "###############################################################################\n\n")

getStationData("./antenna.cat")

sp.close()
