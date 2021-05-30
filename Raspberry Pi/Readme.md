#### Code tested on Raspberry Pi 2 B 1GB RAM

##### ___Which features works as of now___:
* Script can convert voice message to text using Google Speech Recognition
* Script can recognize 2 products _names_ and their respective _counts_ (eg. saying "I want 2 Toblerones and 3 KitKats", the script knows that the quantity of Toblerone is 2 and quantity of KitKat is 3). As long as the _count_ of the product preceeds the _product name_ the script works
* Script also works when single product order is given (eg. "I want 1 KitKat", this voice command also works)
* Assistant's voice greeting messages are already added and can be modified as required.
* Once the order is given confirmation is asked by the assistant whether to accept the order
* In case of invalid voice inputs, the script gives an 'invalid input' voice feedback and loops back again to re-record the voice command from the user
* Send Product count signal and confirm signal to Arduino (By toggling button state)
* Check Arduino busy status line before accepting the next order

##### ___What improvements can be made:___
* Regex can be used to improve decoding the product _name_ and _count_ from the text obtained after conversion of voice using speech recognition
* Text to speech synthesis can be improved using MBROLA
##### ___Yet to implement:___
* Calling Face recognition Python script before giving the greeting voice message

---
#### engines used:
##### Speech-To-Text > SpeechRecognition https://pypi.org/project/SpeechRecognition/
##### Text-To-Speech > espeak http://espeak.sourceforge.net/
---

### Pre-requisite packages installation on Raspberry Pi
* sudo pip3 install SpeechRecognition
* sudo pip3 install PyAudio
* sudo apt-get install flac

I ran into issues while using espeak directly from the apt repository. Sentences were not completely spoken and had to run the same espeak command twice to get the proper speech output. I recommend installing espeak from the repository using _sudo apt-get install espeak_ and check if espeak is working properly. I got around this issue by building espeak from source. Even though sometimes words were not spoken, I got a better result.

### Building espeak from source:
* Download the espeak package from sourceforge (I downloaded 1.48.04)
* Open the Makefile inside src folder and comment (adding #) _AUDIO = portaudio_, uncomment (removing #) _AUDIO = pulseaudio_. Add _.asoundrc_ file in your home directory (~) and add the following code:

> pcm.pulse { type pulse } <br/>
> ctl.pulse { type pulse }  <br/>
> pcm.!default { type pulse }  <br/>
> ctl.!default { type pulse }  <br/>

Now to build espeak, install these packages: <br/>
sudo apt-get update <br/>
sudo apt-get install make autoconf automake libtool pkg-config <br/>
sudo apt-get install  portaudio19-dev <br/>
sudo apt-get install  libasound2-dev <br/>
sudo apt-get install  libportaudio2 <br/>
sudo apt-get install  libportaudiocpp0 <br/>
sudo apt-get install libwxgtk2.8-dev <br/>
sudo apt-get install  libpulse-dev <br/>
sudo apt-get install  libportaudio-dev <br/>
sudo apt-get install speech-dispatcher <br/>

Open the terminal from src folder and type:
> make

> sudo make-install

Try running espeak from terminal:
> espeak "Hello World" <br/>

You should hear "Hello World"

### Why we had to go through all these steps?
Somehow pulseaudio works better in raspbian while using espeak. To know more about this you may refer: https://www.emacspeak.org/VCCS-archive//2010/msg00068.html and building espeak from souce you may refer: https://learn.linksprite.com/pcduino/how-to-compile-espeak-text-to-speech-engine-from-source-on-pcduino3/

---
### Raspberry Pi GPIO pins used for interfacing with Arduino: ###
* GPIO_PIN 4 (Board pin 7) ___Check Arduino busy status___
* GPIO_PIN 18 (Board pin 12) ___Product confirm signal to Arduino___
* GPIO_PIN 27 (Board pin 13) ___Product 1 signal to Arduino___
* GPIO_PIN 22 (Board pin 15) ___Product 2 signal to Arduino___
---

### I went with modular coding approach here. There are 3 python scripts:
* main.py
* tts.py
* speech_recog,py

This approach makes debugging and modifying the code easier.

### Script functions:
* main.py <- As the name suggest, this is the main script which is run in raspberry pi.
* tts.py <- For executing espeak on terminal. Script calling tts.py defined function sends a string argument and this string argument is passed on to the terminal along with the predefined espeak configurations (like speech rate, volume, voice etc which can be edited in this script file).
* speech_recog.py <- Here the voice is recorded and voice to speech recognition is done.

### For more detailed information about these script files, refer the Readme inside ___piycodes___ folder
