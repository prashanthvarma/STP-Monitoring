# STP_Monitoring
STP Route Monitoring


#***System Description***

Python 2.7.3 (default, Feb 27 2014, 20:00:17) 
[GCC 4.6.3] on linux2


#***Monitoring CLI***

Enter a command to monitor routes...

For the list of available commands, enter: Command = ¨list¨

At anytime, if you want to close this monitoring application, enter: command = ¨exit¨


Command: list


Here is the list of available commands for monitoring routes:

¨routes¨      -- For the list of destinations and their corresponding linksets
¨report¨      -- For the list of destinations (point codes) and linksets that are not reachable (CRITICAL and WARNING reporting)
¨destination¨ -- For filtering specific destination for its route monitoring and error reporting
¨linkset¨     -- For filtering specific linkset and its corresponding destination for its route monitoring and error reporting
¨clear¨       -- For clearing the  CLI at any time
¨exit¨        -- For closing this monitoring application at any time



#***Example log***

Logs/Routes


#***Example error report***

Monitoring routes...


***NOTE***

Destination (Point Code)  4176  is reachable only via a single connection in XUA routing table, its linkset(s) are unavailable


***WARNING***

Following linkset(s) in destination (Point Code)  4201  is/are unavailable but the destination is reachable: 
INAT-LS-BICS2


***CRITICAL***

Destination (Point Code)  4550  is not reachable
