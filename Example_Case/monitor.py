#!/usr/bin/env python
# -*- coding: utf-8 -*-

# STP Monitoring Application

# Importing Python modules

import re # Python module for parsing strings
import sys # Python module for system (interpreter) specific parameters and functions
import os # Python module for operating system dependent functionality


class read_file():

    # Reading routes from log file and returning them upon function call (both system and XUA routes)
    
    def routes(self):
        lines = [line.strip() for line in open('Logs/Routes')]
        l = len(lines)
        for line in lines:
            if line == 'Routing table = system Destinations = 5 Routes = 13':
                s = lines.index(line)
                s = s+4
            if line == 'Routing table = XUA':
                e = lines.index(line)
                e = e-1
        system = lines[s:e]
        xua = lines[e+5:l]
        sys_routes = {}
        for sys in system:
            route = sys.split()
            rl = len(route)
            if rl == 6:
                route_dic = {}
                pc = route[0].split('/')
                pc = pc[0]
                l = 1
                route_dic[l] = route[2:rl]
                l = l+1
                sys_routes[pc] = route_dic
            else:
                route_dic[l] = route
                l = l+1
        xua_routes = {}
        for xu in xua:
            route = xu.split()
            rl = len(route)
            pc = route[0].split('/')
            pc = pc[0]
            xua_routes[pc] = route[rl-1]
        return {'system' : sys_routes, 'XUA' : xua_routes}


class routes_list():

    # Printing the list of destinations and their corresponding linksets

    def show_routes(self, sys_routes, xua_routes):
        print '\nList of destinations and their corresponding linksets: '
        print '\n=>System Routing Table: \n'
        for sys in sys_routes:
            print 'Destination (Point Code):', sys
            print 'Linksets:'
            for route in sys_routes[sys]:
                print sys_routes[sys][route][1]
        print '\n=>XUA Routing Table: \n'
        for xu in xua_routes:
            print 'Destination (Point Code):', xu
            print '(Single connection)'
    

class report():


    # Reports errors such as CRITICAL and WARNING

    def error_report(self, sys_routes, xua_routes, destination, linkset):
        print '\n\nMonitoring routes...'
        if (destination == '' and linkset == ''):
            for sys in sys_routes:
                c = 0
                l = len(sys_routes[sys].keys())
                for route in sys_routes[sys]:
                    if sys_routes[sys][route][2] == 'avail':
                        c = c+1
                if c == 0:
                    if sys not in xua_routes.keys():
                        print '\n\n***CRITICAL***\n'
                        print 'Destination (Point Code) ', sys, ' is not reachable\n\n'
                    else:
                        print '\n\n***NOTE***\n'
                        print 'Destination (Point Code) ', sys, ' is reachable only via a single connection in XUA routing table, its linkset(s) are unavailable\n'
                elif (c>0 and c<l):
                    print '\n\n***WARNING***\n'
                    print 'Following linkset(s) in destination (Point Code) ', sys, ' is/are unavailable but the destination is reachable: '
                    for route in sys_routes[sys]:
                        if sys_routes[sys][route][2] == 'unavail':
                            print sys_routes[sys][route][1]
        elif (destination != '' or linkset != ''):
            if destination not in sys_routes.keys():
                    if destination not in xua_routes.keys():
                        print '\nThis destination (Point Code) does not exist in the routing tables, re-enter'
                    else:
                        print '\n\n***NOTE***\n'
                        print 'Destination (Point Code) ', destination, ' is reachable only via a single connection in XUA routing table, its linkset(s) are unavailable\n'            
            else:
                print '\nDestination (Point Code):', destination
                c = 0
                l = len(sys_routes[destination].keys())
                for route in sys_routes[destination]:
                    if sys_routes[destination][route][2] == 'avail':
                        c = c+1
                if c == 0:
                    if destination not in xua_routes.keys():
                        print '\n\n***CRITICAL***\n'
                        print 'Destination (Point Code) ', destination, ' is not reachable\n\n'
                    else:
                        print '\n\n***NOTE***\n'
                        print 'Destination (Point Code) ', destination, ' is reachable only via a single connection in XUA routing table, its linkset(s) are unavailable\n'
                elif (c>0 and c<l):
                    if linkset != '':
                        k = 0
                        for route in sys_routes[destination]:
                            if (sys_routes[destination][route][1] == linkset):
                                k = k+1
                                ind = route
                        if k != 0:
                            if (sys_routes[destination][ind][2] == 'unavail'):
                                print 'un'
                                print '\n\n***WARNING***\n'
                                print 'linkset', linkset, 'of destination (Point Code) ', destination, ' is unavailable but the destination is reachable: '
                            else:
                                print 'av'
                                print '\nlinkset', linkset, 'of destination (Point Code) ', destination, ' is available'
                        else:
                            print'This linkset does not exist for this destination (Point Code), re-enter'          
                    else:
                        print '\n\n***WARNING***\n'
                        print 'Following linkset(s) in destination (Point Code) ', destination, ' is/are unavailable but the destination is reachable: '
                        for route in sys_routes[destination]:
                            if sys_routes[destination][route][2] == 'unavail':
                                print sys_routes[destination][route][1]
                else:
                    print '\nDestination (Point Code)', destination, 'is reachable through all its linksets'


class monitor_cli():


    # Accepting user commands to monitor routes on CLI

    def cli(self):
        print '\n\nEnter a command to monitor routes...\n'
        print 'For the list of available commands, enter: Command = ¨list¨\n'
        print 'At anytime, if you want to close this monitoring application, enter: command = ¨exit¨\n'
        while True:
            routes = read_file().routes()
            sys_routes = routes['system']
            xua_routes = routes['XUA']
            try:
                print '\n\n'
                cmd = raw_input('Command: ')
                cmd = cmd.lower()
                if (cmd.strip() == 'exit' or cmd.strip() == 'close'):
                    print '\nYou are now exiting the monitoring application...\n'
                    break
                elif (cmd == 'clear'):
                    os.system('clear')
                elif (cmd == 'list'):
                    print '\n\nHere is the list of available commands for monitoring routes:\n'
                    print '¨routes¨      -- For the list of destinations and their corresponding linksets'
                    print '¨report¨      -- For the list of destinations (point codes) and linksets that are not reachable (CRITICAL and WARNING reporting)'
                    print '¨destination¨ -- For filtering specific destination for its route monitoring and error reporting'
                    print '¨linkset¨     -- For filtering specific linkset and its corresponding destination for its route monitoring and error reporting'
                    print '¨clear¨       -- For clearing the  CLI at any time'
                    print '¨exit¨        -- For closing this monitoring application at any time'
                elif cmd == 'routes':
                    routes_list().show_routes(sys_routes, xua_routes)
                elif cmd == 'report':
                    report().error_report(sys_routes, xua_routes, '', '')
                elif cmd == 'destination':
                    print '\n'
                    destination = raw_input('Enter the destination (Point Code) for filtering: ')
                    report().error_report(sys_routes, xua_routes, destination, '')
                elif cmd == 'linkset':
                    print'\n'
                    destination = raw_input('Enter the destination point code for filtering: ')
                    linkset = raw_input('Enter the destination linkset for filtering: ')
                    report().error_report(sys_routes, xua_routes, destination, linkset)
                else:
                    print '\n\nWrong entry'
                    print '\nFor the list of available commands, enter: Command = ¨list¨\n'
            except KeyboardInterrupt:
                print '\nYou are now exiting the monitoring application...\n'
                sys.exit(0)
            except:
                print '\nYou are now exiting the monitoring application...\n'
                sys.exit(0)



# Initializing the STP monitoring application

print '\n\nStarting the STP Monitoring Application...\n'
print '\n\nYou are now entering the STP Monitoring Application...\n\n'


# Reading routes from log file and returning them upon function call (both system and XUA routes)

routes = read_file().routes()
sys_routes = routes['system']
xua_routes = routes['XUA']


# Printing the list of destinations and their corresponding linksets

routes_list().show_routes(sys_routes, xua_routes)


# Reporting errors such as CRITICAL and WARNING

report().error_report(sys_routes, xua_routes, '', '')


# Initializing monitoring application CLI

monitor_cli().cli()


