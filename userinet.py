#!/usr/bin/python3


import os
import optparse
import re
from pprint import pprint
from wifi_user import wifi_user

usage = "usage: %prog [options] arg"
parser = optparse.OptionParser()
parser.add_option("-u", "--userid", dest="userid",
                  help="user id", metavar="USER_ID")                
parser.add_option("-a", "--action", dest="action",
                  help="enable or disable user", metavar="ACTION")


(options, args) = parser.parse_args()

print("userid %s" % (options.userid))
print("action %s" % (options.action))


users = {
    '4c:49:e3:b6:ef:a7': 'Adel',
    '64:cc:2e:6e:ee:89': 'Lori',
    'b4:9d:0b:6d:59:b8': 'Kris',
    '5c:51:88:3a:af:9c': 'Vera',
    '9c:b6:d0:e2:09:d1': 'xps13',
    '18:3d:a2:08:4f:98': 'x201',
    'irulu': 'Adam',
    '60:67:20:ed:42:8c': 't430s',
    '58:94:6b:17:41:7c': 'e4310',
    }    
  

wifi_user = wifi_user(users, options.userid)


if(options.action == 'enable'):
    wifi_user.traffic_enable()
if(options.action == 'disable'):
    wifi_user.traffic_disable()
    
