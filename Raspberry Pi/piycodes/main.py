# Smart Vending Machine [github.com/ashvnv/smart-vending-machine]
# Raspberry Pi Voice Assistance and Face Recognition [Main script]
# Last updated: 16 May 2021
#
# Prerequisite packages for speech recognition (for debian based distros):
#               sudo apt-get install espeak
#               sudo pip3 install SpeechRecognition
#               sudo pip3 install PyAudio
#               sudo apt-get install flac  
#
# GPIO PINS USED:
# GPIO_PIN 4 (Board pin 7) Check Arduino busy status
# GPIO_PIN 18 (Board pin 12) Product confirm signal to Arduino
# GPIO_PIN 27 (Board pin 13) Product 1 signal to Arduino
# GPIO_PIN 22 (Board pin 15) Product 2 signal to Arduino
#
# 
#



import serial
import RPi.GPIO as GPIO
import os, time


#-------------Import other scripts-------------
import speech_recog as srpy
import tts # Text to speech script
#----------------------------------------------



#-----------------iftttlog.py file path--------------------
#log the data in google sheet
my_dir = os.path.expanduser('~/')
import sys
sys.path.append(my_dir + '/smart-vending-machine')
import iftttlog
#----------------------------------------------------------



GPIO.setwarnings(False) #Suppress warnings
GPIO.setmode(GPIO.BCM) # Use GPIO number instead of actual board pin number

#-----------PINS declared--------------
BUSYSTAT_BTN = 4
CONFIRM_BTN = 18
PROD1_BTN = 27
PROD2_BTN = 22

#----------PINS configured-------------
GPIO.setup(BUSYSTAT_BTN, GPIO.IN)
GPIO.setup(CONFIRM_BTN, GPIO.OUT)
GPIO.setup(PROD1_BTN, GPIO.OUT)
GPIO.setup(PROD2_BTN, GPIO.OUT)




#-------------------------------Send order to Arduino by toggling pins------------------------------
def SwitchToggle(pin, tglcount):
    for i in range(0,tglcount):
        
        GPIO.output(pin, GPIO.LOW) #pin made low
        iftttlog.logdata('main.py',"Pin " + str(pin) + " made LOW") #log the data
        time.sleep(0.2) #wait for arduino debounce delay
        
        GPIO.output(pin, GPIO.HIGH) #pin made high
        iftttlog.logdata('main.py',"Pin " + str(pin) + " made HIGH") #log the data
        time.sleep(0.2) #wait for arduino debounce delay




#----------------------------------Script starts execution from here----------------------------------------
#-----------------------------------------------------------------------------------------------------------
while(1):

    # while(1): {} ### FACE RECOGNITION SCRIPT WILL BE CALLED FROM HERE
    

    #----------------------------------Welcome msg------------------------------------
    tts.TTS_call("Hy there! What would you like to order?")
    #---------------------------------------------------------------------------------

    #----------------------calling recognition functions---------------------------
    recognized_text = 0
    while (recognized_text == 0):
        recorded_audio = srpy.ListenAudio() 
        recognized_text = srpy.DecodeAudio(recorded_audio);
    #------------------------------------------------------------------------------



    #-------------------------------------------Message decoder-----------------------------------------------------
        
    prod1_name = srpy.NameFind(recognized_text, ["Toblerone","toblerone"]) # also send a list of words to compare with recognized text
    if (prod1_name != "null"): # skip count check is product 1 not found
        prod1_count = srpy.CountFind(recognized_text)
    else:
        prod1_count = 0


    prod2_name = srpy.NameFind((recognized_text), ["KitKat","Kit Kat","kitkat","kit kat"]) # also send a list of words to compare with recognized text
    if (prod2_name != "null"): # skip count check is product 2 not found
        prod2_count = srpy.CountFind(" ".join(reversed(recognized_text.split())))
        #string had to be reversed because a user may simultaneously give order for both the product (eg. 3 product1 and 1 product2). CountFind() loops through the string to find a particular number. reversing the string is necessary
        #as CountFind() uses isdigit() to find a number in the string. Looking for product2 count from lhs of string will result in function returning product1 count. 
    else:
        prod2_count = 0
    #--------------------------------------------------------------------------------------------------------------



    #-------------------------------------check if valid inputs are recognized-------------------------------------
    if ((prod1_name != "null" and prod1_count != 0) or (prod2_count != "null" and prod2_count != 0)): 
        tts.TTS_call("You have ordered")
        
        if (prod1_name != "null"):
            msg = str(prod1_count) + " " + prod1_name
            tts.TTS_call(msg)
            iftttlog.logdata('main.py',msg) #log the data
            
        if (prod2_name != "null"):
            msg = str(prod2_count) + " " + prod2_name
            tts.TTS_call(msg)
            iftttlog.logdata('main.py',msg) #log the data
    #--------------------------------------------------------------------------------------------------------------
            

        tts.TTS_call("Would you like to confirm the order?")


        conf_resp = "null"
        rej_resp = "null"
        while(conf_resp == "null" and rej_resp == "null"):
            
            #----------------------calling recognition functions---------------------------
            recognized_text = 0
            while (recognized_text == 0):
                recorded_audio = srpy.ListenAudio()
                recognized_text = srpy.DecodeAudio(recorded_audio);
            #------------------------------------------------------------------------------

            conf_resp = srpy.NameFind(recognized_text, ["yes","Yes"])
            rej_resp = srpy.NameFind(recognized_text, ["no", "No"])

            if (conf_resp != "null"):
                tts.TTS_call("Order confirmed. Please wait while I prepare your order")
            
            #-------------------------------------Arduino switch toggle------------------------------------------------
                if (prod1_name != "null"):
                    iftttlog.logdata('main.py',"Processing Product 1, Count: " + str(prod1_count)) #log the data
                    SwitchToggle(PROD1_BTN, prod1_count) #Toggle arduino product 1 pin
            
                if (prod2_name != "null"):
                    iftttlog.logdata('main.py',"Processing Product 2, Count: " + str(prod2_count)) #log the data
                    SwitchToggle(PROD2_BTN, prod2_count) #toggle arduino product 2 pin
                    
                iftttlog.logdata('main.py',"Confirm btn") #log the data
                SwitchToggle(CONFIRM_BTN, 1) #send confirm pulse to arduino
            #-----------------------------------------------------------------------------------------------------------

                while GPIO.input(BUSYSTAT_BTN) == GPIO.LOW:
                    #check busy status here
                    time.sleep(0.5)
                iftttlog.logdata('main.py',"Processed") #log the data
                tts.TTS_call("Your order is prepared. Please collect it from the collection window. See you soon.")


            elif(rej_resp != "null"):
                tts.TTS_call("Order cancelled")
            else:
                tts.TTS_call("Invalid input... Please try again")
        
    else:
        tts.TTS_call("Invalid input... Please try again")
            
            
            
        

    
