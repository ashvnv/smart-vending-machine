## Caution!
#### Raspberry Pi python script is incomplete.

##### ___What works for now___:
* Script can convert voice message to text using Google Speech Recognition
* Script can recognize 2 products _names_ and their respective _counts_ (eg. saying "I want 2 Toblerones and 3 KitKats", the script knows that the quantity of Toblerone is 2 and quantity of KitKat is 3). As long as the _count_ of the product preceeds the _product name_ the script works
* Script also works when single product order is given (eg. "I want 1 KitKat", this voice command also works)
* Assistant's voice greeting messages are already added and can be modified as required.
* Once the order is given confirmation is asked by the assistant whether to accept the order
* In case of invalid voice inputs, the script gives an 'invalid input' voice feedback and loops back again to re-record the voice command from the user

##### ___What improvements can be made:___
* Regex can be used to improve decoding the product _name_ and _count_ from the text obtained after conversion of voice using speech recognition
##### ___Yet to implement:___
* Calling Face recognition Python script before giving the greeting voice message
* Arduino busy-status pin check after giving the product _counts_ and order _confirm_ commands to Arduino
---

## Caution!
#### The Raspberry Pi Python script was tested on a laptop running Linux Mint 20.1 (based on Ubuntu 20.04 LTS). Due to covid-19 lockdown and lack of resources, getting a Raspberry Pi was not possible. Before executing the script on the laptop, many program lines had to be commented-out as they require a Raspberry Pi to work. The commented lines script is available in this repository as of now. For testing the Python script on Raspberry Pi these comments can be removed and python script should work as expected but there is no guarantee about the same.
---
### For Debian based distros (including Raspbian OS) prequisite packages to be installed before making the voice assistant python script work:
* sudo pip3 install espeak
* sudo pip3 install SpeechRecognition
* sudo pip3 install PyAudio
---
### Raspberry Pi GPIO pins used for interfacing with Arduino: ###
* GPIO_PIN 4 (Board pin 7) ___Check Arduino busy status___
* GPIO_PIN 18 (Board pin 12) ___Product confirm signal to Arduino___
* GPIO_PIN 27 (Board pin 13) ___Product 1 signal to Arduino___
* GPIO_PIN 22 (Board pin 15) ___Product 2 signal to Arduino___
---
## Voice Assistant script
> The script is bifurcated using '-' comment lines for easier understanding and debugging. Some codes in the script is commented-out as the script has not been tested yet on Raspberry Pi.
#### Libraries imported:
* import speech_recognition as sr //___called from the installed SpeechRecognition package___
* import serial //___for Raspberry Pi___
* import RPi.GPIO as GPIO //___for Raspberry Pi___
* import os, time //__for calling delay()___


### Script starts execution from the bottom-most section inside a while(1) loop
##### Flow of main section:
* Execute face recognition script
* welcome message is executed using _espeak_ once face recognition script returns the recognized person's details
* calls ListenAudio() (_records the user's voice commands and returns the audio file_) and DecodeAudio() (_audio file is converted to text using google voice api function_) for getting voice to text message
* decodes the received text message to get product 1 and 2 counts
* takes confirmation message from the user for confirming the order
* call SwitchToggle() to send the order commands to Arduino
* giving thankyou voice message after Arduino completes processing the order (script continuously poles Arduino busystatus pin to know when Arduino finishes processing the order)
* _repeat_ the loop

### Python function called to send commands to Arduino:
> def SwitchToggle(pin, tglcount)
##### The function takes two parameters _pin number_ and _tglcount_. Both are integers values. Pin Number is the GPIO pin number the not the actual Raspberry Pi board pin number although this can be changed in the setup section of the Python Script as given below:
> GPIO.setmode(GPIO.BCM)  //_Use GPIO number instead of actual board pin number_
##### tglcount is how many times the pin should be made ___LOW-HIGH___
---
