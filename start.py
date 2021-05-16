# Smart Vending Machine [github.com/ashvnv/smart-vending-machine]
# Raspberry Pi Voice Assistance and Face Recognition [start script]
# Last updated: 16 May 2021
#
# This is the python script which Raspberry Pi runs on startup.
# Script flow:
# 1) Check Internet connection
# 2) Update the cloned github repository (smart-vending-machine); this script should remain inside smart-vending-machine repository, git pull doesnot work from other paths
# 3) Call the main.py script <- restart raspberry pi if error encountered (commented)

import os


#-----------------iftttlog.py file path--------------------
#log the data in google sheet
my_dir = os.path.expanduser('~/')
import sys
sys.path.append(my_dir + '/smart-vending-machine')
import iftttlog
#----------------------------------------------------------


#--------------------------------------------------Connection check------------------------------------------------------------
#-------------------
WAIT_PERIOD = 5 #If the ping failed, time to wait before the next ping check is done (time in seconds)
PING_URL = 'http://google.com'
#-------------------


import urllib.request
import time

#---------------------------------------------------------------

def check_conn():
    try:
        urllib.request.urlopen(PING_URL)
        return True
    except:
        return False

while(check_conn() == False):
    print("Not connected")
    time.sleep(WAIT_PERIOD)

iftttlog.logdata('start.py','Connected to Internet') #log the data




#----------------------------------------------repository update------------------------------------------------------------------
import subprocess

subprocess.run(["git","reset","--hard"], capture_output=True) #discard local changes completely:
subprocess.run(["git","clean","-fd"], capture_output=True) #remove untracked / new files

tempstr = subprocess.run(["git","pull"], capture_output=True) #pull
iftttlog.logdata('start.py', str(tempstr)) #log the data




#-----------------------------------------------call main.py---------------------------------------------------------------------

# main.py path
MAIN_PATH = "~/smart-vending-machine/Raspberry\ Pi/piycodes/main.py"

if (os.system("python3 " + MAIN_PATH) != 0):
    iftttlog.logdata('start.py','Fatal error, check logs') #log the data
    
    #restart the system if error occurs
    # os.system("reboot")
