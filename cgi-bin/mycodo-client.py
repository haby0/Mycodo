#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#  mycodo-client.py - Client for mycodo.py. Communicates with daemonized mycodo.py to
#                     execute commands and receive status. This allows only one
#                     program to run, preventing possible "double-editing" of files
#                     and other risky behavior.
#
#  Kyle Gabriel (2012 - 2015)
#

import rpyc
import time
import sys
import getopt
import datetime

c = rpyc.connect("localhost", 18812)

def usage():
    print 'mycodo-client.py: Client for mycodo.py (must be running in daemon mode -d).\n'
    print 'Usage:  mycodo-client.py [OPTION]...\n'
    print 'Options:'
    print '        --modrelaynames [Name1] [Name2] [Name3] [Name4] [Name5] [Name6] [Name7] [Name8]'
    print '           Modify relay names (Restrict to a maximum of 12 characters each)'
    print '        --modrelaypins [Pin1] [Pin2] [Pin3] [Pin4] [Pin5] [Pin6] [Pin7] [Pin8]'
    print '           Modify relay pins (Using BCM numbering)'
    print '        --modrelaytrigger [Trig1] [Trig2] [Trig3] [Trig4] [Trig5] [Trig6] [Trig7] [Trig8]'
    print '           Modify the trigger state of relays'
    print '        --modsensornames [Name1] [Name2] [Name3] [Name4] [Name5] [Name6] [Name7] [Name8]'
    print '           Modify sensor names (Restrict to a maximum of 12 characters each)'
    print '        --modsensordevices [Device1] [Device2] [Device3] [Device4] [Device5] [Device6] [Device7] [Device8]'
    print '           Modify sensor names (Restrict to a maximum of 12 characters each)'
    print '        --modsensorpins [Pin1] [Pin2] [Pin3] [Pin4] [Pin5] [Pin6] [Pin7] [Pin8]'
    print '           Modify sensor pins (Using BCM numbering)'
    print '        --modsensorperiods [Per1] [Per2] [Per3] [Per4] [Per5] [Per6] [Per7] [Per8]'
    print '           Modify the period between sensor reads'
    print '        --modtimer [Timer Number] [State] [Relay Number] [Duration On] [Duration Off]'
    print '           Modify custom timers, State: 0=off 1=on, durations in seconds'
    print '        --modvar [Var1Name] [Var1Value] [Var2Name] [Var2Value]...'
    print '           Modify any configuration variable or variables (multiple allowed, must be paired input)'
    print "    -r, --relay [Relay Number] [0/1/X]"
    print "           Change the state of a relay"
    print "           0=OFF, 1=ON, or X number of seconds On"
    print '    -t, --terminate'
    print '           Terminate the communication service and daemon'
    print '    -w, --writelog'
    print '           Read sensor and append log file\n'    

def menu():
    try:
        opts, args = getopt.getopt(
            sys.argv[1:], 'o:p:r:s:tw', 
            ["modrelaynames=", "modrelaypins=", "modrelaytrigger=",
            "modsensornames", "modsensordevices", "modsensorpins", "modsensorperiods",
            "modtimer=", "modvar=", "pid=", "relay=", "terminate", "writelog"])
    except getopt.GetoptError as err:
        print(err) # will print "option -a not recognized"
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == "--modvar":
            print "%s [Remote command] Mod Vars: %s" % (
                Timestamp(), sys.argv[1:])
            print "%s [Remote command] Server returned:" % (
                Timestamp()),
            if c.root.Modify_Variables(*sys.argv[1:]) == 1:
                print "Success"
            else:
                print "Fail"
            sys.exit(0)
        elif opt == "--changetempor":
            print "%s [Remote command] Change TempOR to %s: Server returned:" % (
                Timestamp(), sys.argv[2]),
            if c.root.ChangeTempOR(int(float(sys.argv[2]))) == 1:
                print "Success"
            else:
                print "Fail"
            sys.exit(0)
        elif opt == "--changehumor":
            print "%s [Remote command] Change HumOR to %s: Server returned:" % (
                Timestamp(), sys.argv[2]),
            if c.root.ChangeHumOR(int(float(sys.argv[2]))) == 1:
                print "Success"
            else:
                print "Fail"
            sys.exit(0)
        elif opt == "--modsensornames":
            print "%s [Remote command] Set Sensor Names: %s %s %s %s %s %s %s %s: Server returned:" % (
                Timestamp(), 
                sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], 
                sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9]),
            if c.root.ChangeSensorNames(
                sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], 
                sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9]) == 1:
                print "Success"
            else:
                print "Fail"
            sys.exit(0)
        elif opt == "--modsensordevices":
            print "%s [Remote command] Set Sensor Devicess: %s %s %s %s %s %s %s %s: Server returned:" % (
                Timestamp(), int(sys.argv[2]), int(sys.argv[3]), 
                int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), 
                int(sys.argv[7]), int(sys.argv[8]), int(sys.argv[9])),
            if c.root.ChangeSensorDevices(
                int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), 
                int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]), 
                int(sys.argv[8]), int(sys.argv[9])) == 1: 
                print "Success"
            else: 
                print "Fail"
            sys.exit(0)
        elif opt == "--modsensorpins":
            print "%s [Remote command] Set Sensor Pins: %s %s %s %s %s %s %s %s: Server returned:" % (
                Timestamp(), int(sys.argv[2]), int(sys.argv[3]), 
                int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), 
                int(sys.argv[7]), int(sys.argv[8]), int(sys.argv[9])),
            if c.root.ChangeSensorPins(
                int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), 
                int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]), 
                int(sys.argv[8]), int(sys.argv[9])) == 1: 
                print "Success"
            else: 
                print "Fail"
            sys.exit(0)
        elif opt == "--modsensorperiods":
            print "%s [Remote command] Set Sensor Periods: %s %s %s %s %s %s %s %s: Server returned:" % (
                Timestamp(), int(sys.argv[2]), int(sys.argv[3]), 
                int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), 
                int(sys.argv[7]), int(sys.argv[8]), int(sys.argv[9])),
            if c.root.ChangeSensorPeriods(
                int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), 
                int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]), 
                int(sys.argv[8]), int(sys.argv[9])) == 1: 
                print "Success"
            else: 
                print "Fail"
            sys.exit(0)
        elif opt == "--modrelaynames":
            print "%s [Remote command] Set Relay Names: %s %s %s %s %s %s %s %s: Server returned:" % (
                Timestamp(), 
                sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], 
                sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9]),
            if c.root.ChangeRelayNames(
                sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], 
                sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9]) == 1:
                print "Success"
            else:
                print "Fail"
            sys.exit(0)
        elif opt == "--modrelaypins":
            print "%s [Remote command] Set Relay Pins: %s %s %s %s %s %s %s %s: Server returned:" % (
                Timestamp(), int(sys.argv[2]), int(sys.argv[3]), 
                int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), 
                int(sys.argv[7]), int(sys.argv[8]), int(sys.argv[9])),
            if c.root.ChangeRelayPins(
                int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), 
                int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]), 
                int(sys.argv[8]), int(sys.argv[9])) == 1: 
                print "Success"
            else: 
                print "Fail"
            sys.exit(0)
        elif opt == "--modtimer":
            print "%s [Remote command] Set Timer %s: State: %s Relay: %s DurOn: %s DurOff: %s: Server returned:" % (
                Timestamp(), int(sys.argv[2]), int(sys.argv[3]), 
                int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])),
            if c.root.ChangeTimer(
                int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), 
                int(sys.argv[5]), int(sys.argv[6])) == 1: 
                print "Success"
            else: 
                print "Fail"
            sys.exit(0)
        elif opt == "--modrelaytrigger":
            print "%s [Remote command] Set Relay Triggers: %s %s %s %s %s %s %s %s: Server returned:" % (
                Timestamp(), int(sys.argv[2]), int(sys.argv[3]), 
                int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), 
                int(sys.argv[7]), int(sys.argv[8]), int(sys.argv[9])),
            if c.root.ChangeRelayTriggers(
                int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), 
                int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]), 
                int(sys.argv[8]), int(sys.argv[9])) == 1: 
                print "Success"
            else: 
                print "Fail"
            sys.exit(0)
        elif opt in ("-r", "--relay"):
            if RepresentsInt(sys.argv[2]) and \
                int(float(sys.argv[2])) > 0:
                if (sys.argv[3] == '0' or sys.argv[3] == '1'):
                    print "%s [Remote command] Set relay %s to %s: Server returned:" % (
                        Timestamp(), int(float(sys.argv[2])), int(float(sys.argv[3]))),
                    if c.root.ChangeRelay(int(float(sys.argv[2])), 
                            int(float(sys.argv[3]))) == 1:
                        print 'success'
                    else:
                        print 'fail'
                    sys.exit(0)
                if (sys.argv[2] > 1):
                    print '%s [Remote command] Relay %s ON for %s seconds: Server returned:' % (
                        Timestamp(), int(float(sys.argv[2])), int(float(sys.argv[3]))),
                    if c.root.ChangeRelay(int(float(sys.argv[2])),
                            int(float(sys.argv[3]))) == 1:
                        print "Success"
                    else:
                        print "Fail"
                    sys.exit(0)
            else:
                print 'Error: second input must be an integer greater than 0'
                sys.exit(1)
        elif opt in ("-t", "--terminate"):
            print "%s [Remote command] Terminate all threads and daemon: Server returned:" % (
                Timestamp()),
            if c.root.Terminate(1) == 1: print "Success"
            else: print "Fail"
            sys.exit(0)
        elif opt in ("-w", "--logwrite"):
            print "%s [Remote Command] Append sensor log: Server returned:" % (
                Timestamp()), 
            if c.root.WriteSensorLog() == 1: print "Success"
            else: print "Fail"
            sys.exit(0)
        else:
            assert False, "Fail"

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def Timestamp():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y %m %d %H %M %S')

if len(sys.argv) == 1: # No arguments given
    usage()
    sys.exit(1)

menu()
usage()
sys.exit(0)