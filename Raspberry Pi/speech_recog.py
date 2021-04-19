# Smart Vending Machine [github.com/ashvnv/smart-vending-machine]
# Raspberry Pi Voice Assistance Python code
#
# Prerequisite packages for speech recognition (for debian based distros):
#               sudo apt-get install espeak
#               sudo pip3 install SpeechRecognition
#               sudo pip3 install PyAudio
#
# GPIO PINS USED:
# GPIO_PIN 4 (Board pin 7) Check Arduino busy status
# GPIO_PIN 18 (Board pin 12) Product confirm signal to Arduino
# GPIO_PIN 27 (Board pin 13) Product 1 signal to Arduino
# GPIO_PIN 22 (Board pin 15) Product 2 signal to Arduino
#
# 
#


from subprocess import call
import speech_recognition as sr
#import serial
#import RPi.GPIO as GPIO
import os, time

speechrecog_inst= sr.Recognizer() #create an instance of the recognizer class.
#GPIO.setwarnings(False) #Suppress warnings
#GPIO.setmode(GPIO.BCM) # Use GPIO number instead of actual board pin number

#-----------PINS declared--------------
BUSYSTAT_BTN = 4
CONFIRM_BTN = 18
PROD1_BTN = 27
PROD2_BTN = 22

#----------PINS configured-------------
#GPIO.setup(busystat, GPIO.IN)
#GPIO.setup(confirm_btn, GPIO.OUT)
#GPIO.setup(prod1, GPIO.OUT)
#GPIO.setup(prod2, GPIO.OUT)



#-----------------------------------------------Voice recognition---------------------------------------
def ListenAudio():
    with sr.Microphone() as source:  #using device_index: default
               speechrecog_inst.adjust_for_ambient_noise(source) # suppress noice for better voice recognition {argument takes numerical values in seconds)
               
               print("Waiting for voice input....");
               audio = speechrecog_inst.listen(source)
               print("recorded");
    return audio


def DecodeAudio(audio):
    text = {}
    try:
        text = speechrecog_inst.recognize_google(audio)
        #call('espeak '+text, shell=True)
        print ("recognized: " + text);
        return text;
        

    #----------------Exceptions--------------------
    except sr.UnknownValueError:
        call(["espeak", "-s140  -ven+18 -z" , "Google Speech Recognition could not understand"])
        print("Google Speech Recognition could not understand")
        return 0

    except sr.RequestError as e:
        print("Could not request results from Google")
        return 0


#----------------------------------------------------------------------------------------------------
def NameFind(recognized_text, textlst):
#regex can improve this function
    
    for txt in textlst:
        if txt in recognized_text:
            return txt
    return "null"

    
def CountFind(recognized_text):
    numlst = ["one","two","three","four","five","six","seven","eight","nine","ten"]
#finds numbers in both words and figures
    
    for i in recognized_text.split():
        if i.isdigit():
            return i
        temp = switch_numlst(i) #call switch function to find the count in figure
        if (temp != 0):
            return temp
        
    return 0


#---------------------Switch function----------------------------
def switch_numlst(arg):
    switcher = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
    }
    return switcher.get(arg,0) #returns 0 for invalid arguments



#-------------------------------Send order to Arduino via toggling pins------------------------------
def SwitchToggle(pin, tglcount):
    while i in range(tglcount):
        
        #GPIO.output(pin, GPIO.LOW) #pin made low
        print("Pin " + pin + " made LOW")
        time.sleep(0.2) #wait for arduino debounce delay
        
        #GPIO.output(pin, GPIO.HIGH) #pin made high
        print("Pin " + pin + " made HIGH")
        time.sleep(0.2) #wait for arduino debounce delay

    

#----------------------------------Script starts execution from here----------------------------------------
#-----------------------------------------------------------------------------------------------------------
while(1):

    # while(1): {} ### FACE RECOGNITION SCRIPT WILL BE CALLED FROM HERE
    

    #----------------------------------Welcome msg------------------------------------
    call(["espeak", "-s140  -ven+18 -z" , "Hy there! What would you like to order?"])
    #---------------------------------------------------------------------------------

    #----------------------calling recognition functions---------------------------
    recognized_text = 0
    while (recognized_text == 0):
        recorded_audio = ListenAudio() 
        recognized_text = DecodeAudio(recorded_audio);
    #------------------------------------------------------------------------------



    #-------------------------------------------Message decoder-----------------------------------------------------
        
    prod1_name = NameFind(recognized_text, ["Toblerone","toblerone"]) # also send a list of words to compare with recognized text
    if (prod1_name != "null"): # skip count check is product 1 not found
        prod1_count = CountFind(recognized_text)
    else:
        prod1_count = 0


    prod2_name = NameFind((recognized_text), ["KitKat","Kit Kat","kitkat","kit kat"]) # also send a list of words to compare with recognized text
    if (prod2_name != "null"): # skip count check is product 2 not found
        prod2_count = CountFind(" ".join(reversed(recognized_text.split())))
        #string had to be reversed because a user may simultaneously give order for both the product (eg. 3 product1 and 1 product2). CountFind() loops through the string to find a particular number. reversing the string is necessary
        #as CountFind() uses isdigit() to find a number in the string. Looking for product2 count from lhs of string will result in function returning product1 count. 
    else:
        prod2_count = 0
    #--------------------------------------------------------------------------------------------------------------



    #-------------------------------------check if valid inputs are recognized-------------------------------------
    if ((prod1_name != "null" and prod1_count != 0) or (prod2_count != "null" and prod2_count != 0)): 
        call(["espeak", "-s140  -ven+18 -z" , "You have ordered "])
        
        if (prod1_name != "null"):
            msg = str(prod1_count) + " " + prod1_name
            call(["espeak", "-s140  -ven+18 -z" , msg])
            print(msg)
            
        if (prod2_name != "null"):
            msg = str(prod2_count) + " " + prod2_name
            call(["espeak", "-s140  -ven+18 -z" , msg])
            print(msg)
    #--------------------------------------------------------------------------------------------------------------
            

        call(["espeak", "-s140  -ven+18 -z" , "Would you like to confirm the order?"])


        conf_resp = "null"
        rej_resp = "null"
        while(conf_resp == "null" and rej_resp == "null"):
            
            #----------------------calling recognition functions---------------------------
            recognized_text = 0
            while (recognized_text == 0):
                recorded_audio = ListenAudio()
                recognized_text = DecodeAudio(recorded_audio);
            #------------------------------------------------------------------------------

            conf_resp = NameFind(recognized_text, ["yes","Yes"])
            rej_resp = NameFind(recognized_text, ["no", "No"])

            if (conf_resp != "null"):
                call(["espeak", "-s140  -ven+18 -z" , "Order confirmed. Please wait while I prepare your order"])
            
            #-------------------------------------Arduino switch toggle------------------------------------------------
                if (prod1_name != "null"):
                    print("Processing Product 1, Count: " + prod1_count)
                    #SwitchToggle(PROD1_BTN, prod1_count) #Toggle arduino product 1 pin
            
                if (prod2_name != "null"):
                    print("Processing Product 2, Count: " + prod2_count)
                    #SwitchToggle(PROD2_BTN, prod2_count) #toggle arduino product 2 pin

                #SwitchToggle(CONFIRM_BTN, 1) #send confirm pulse to arduino
            #-----------------------------------------------------------------------------------------------------------

                #while(1) check busy status here
                call(["espeak", "-s140  -ven+18 -z" , "Your order is prepared. Please collect it from the collection window. See you soon."])


            elif(rej_resp != "null"):
                call(["espeak", "-s140  -ven+18 -z" , "Order cancelled"])
            else:
                call(["espeak", "-s140  -ven+18 -z" , "Invalid input... Please try again"])
        
    else:
        call(["espeak", "-s140  -ven+18 -z" , "Invalid inputs... Please try again"])
            
            
            
        

    
