#MIT License

#Copyright (c) 2021 ashvnv

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

# Smart Vending Machine [github.com/ashvnv/smart-vending-machine]
# Raspberry Pi Voice Assistance [IFTTT webhooks-googlesheets logging]
# Last updated: 16 May 2021
#

#----------------------------
#function <- logdata() ; accepts two string parameters, <filename> and <log>. Uses curl to make a POST request to webhooks and triggers the event. Function reads the config.txt file to get the
#                        IFTTT key and event name. Modify the config.txt file path from below. syntax of file:
                                                                                            #  <KEY>
                                                                                            #  <EVENTNAME>
#                        Refer https://ifttt.com/maker_webhooks documentation

#                        Function prints 0, indicating that the data was logged successfully
#                        Also prints the log serially using print

#----------------------------

import os

#---------------------config file path------------------------------------------
usr_dir = '/home/' + 'pi'
configfilepath = usr_dir + '/Desktop/config.txt'
#-------------------------------------------------------------------------------


def logdata(filename,log):
    print(log)

    #----------------------find KEY and EVENTNAME in the config.txt file-----------------------------------------------
    iftttlog = []                                # Declare an empty list.
    with open (configfilepath, 'rt') as myfile:# Open lorem.txt for reading text.
        for myline in myfile:                   # For each line in the file,
            iftttlog.append(myline.rstrip('\n')) # strip newline and add to list.
    #------------------------------------------------------------------------------------------------------------------



    #escape charaters so that curl can be called without errors
    escaped = log.translate(str.maketrans({"[":  r" ",    # [
                                           "]":  r" ",    # ]
                                           "'":  r" ",    # '
                                           "\"":  r" ",   # "
                                           ")": r" ",     # )
                                           "(": r" ",     # (
                                           "\\": r" "}))  # \
            

#---------------------------------------------------------------------------------------------------------------------------------------------
    webhooksurl = 'https://maker.ifttt.com/trigger/' + iftttlog[1] + '/with/key/' + iftttlog[0]
    json= """curl -X POST -H "Content-Type: application/json" -d '{"value1":\"""" + filename + """\","value2":\"""" + escaped + """\"}'"""
                                                                                                                      

    print(": " + str(os.system(json + " " + webhooksurl)))
    return

#test log
#print(logdata("iftttlog.py", "test"))
