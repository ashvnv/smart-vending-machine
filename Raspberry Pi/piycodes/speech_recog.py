# Smart Vending Machine [github.com/ashvnv/smart-vending-machine]
# Raspberry Pi Voice Assistance and Face Recognition [Speech recognition script]
# Last updated: 16 May 2021
#
# This script recognizes voice and converts it into text using Google Speech-To-Text API
# This script defines various functions:

#             ListenAudio() <- No argments. Returns audio file which consits of voice recorded after this function is called. Using default microphone source. Using
#                              adjust_ambient_noise()
#             DecodeAudio() <- Accepts audio file as argument. Converts audio file to text using Google Speech-To-Text. Returns series of text string and prints the
#                              recognized speech on the console
#             NameFind() <- Accepts a string argument and a string array, string array is searched in the string argument and if any one of the array string is found
#                           in string argument, it returns that found string, else returns 0
#             CountFind() <- Accepts a string argument. This function defines a string array of number from 1 to 10 in words. This string array is searched in
#                              the passed string argument and if any one of the array string is found in string argument, it returns that found string, else returns 0
#                              This function also searches for numbers using isdigit() and returns it if found else return 0
#             switch_numlst() <- This function is called by CountFind() to convert number in words to number in digits


#--------------------------------------------
import tts # Text to speech script
import speech_recognition as sr
speechrecog_inst= sr.Recognizer() #create an instance of the recognizer class.
import os


#-----------------iftttlog.py file path--------------------
#log the data in google sheet
usr_dir = '/home/' + os.getlogin()
import sys
sys.path.append(usr_dir + '/smart-vending-machine')
import iftttlog
#----------------------------------------------------------



#-----------------------------------------------Voice recognition---------------------------------------
def ListenAudio():
    with sr.Microphone() as source:  #using device_index: default
               speechrecog_inst.adjust_for_ambient_noise(source) # suppress noice for better voice recognition {argument takes numerical values in seconds)
               
               iftttlog.logdata('speech_recog.py',"Waiting for voice input....") #log the data
               audio = speechrecog_inst.listen(source)
               iftttlog.logdata('speech_recog.py','recorded') #log the data
               
    return audio


def DecodeAudio(audio):
    text = {}
    try:
        text = speechrecog_inst.recognize_google(audio)
        iftttlog.logdata('speech_recog.py',"recognized: " + text) #log the data
        return text;
        

    #----------------Exceptions--------------------
    except sr.UnknownValueError:
        tts.TTS_call("Google Speech Recognition could not understand")
        
        iftttlog.logdata('speech_recog.py',"Google Speech Recognition could not understand") #log the data
        return 0

    except sr.RequestError as e:
        tts.TTS_call("Could not request results from Google")
        
        iftttlog.logdata('speech_recog.py',"Could not request results from Google") #log the data
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
            return int(i)
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

