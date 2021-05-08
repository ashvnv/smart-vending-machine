## main.py

#### Flow of main section:
* Execute face recognition script (face_recog.py)
* Once face recognition script returns the recognized person's details, welcome message is executed by calling _tts.py_ 
* Execute speech_recog.py (_records the user's voice commands and returns the audio file_ and then _audio file is converted to text using google voice api function_) for getting voice to text message
* decodes the received text message to get product 1 and 2 counts
* takes confirmation message from the user for confirming the order
* call SwitchToggle() to send the order commands to Arduino
* giving thankyou voice message after Arduino completes processing the order (script continuously poles Arduino busystatus pin to know when Arduino finishes processing the order)
* _repeat_

### Python function called to send commands to Arduino:
> def SwitchToggle(pin, tglcount)
##### The function takes two parameters _pin number_ and _tglcount_. Both are integers values. Pin Number is the GPIO pin number the not the actual Raspberry Pi board pin number although this can be changed in the setup section of the Python Script as given below:
> GPIO.setmode(GPIO.BCM)  //_Use GPIO number instead of actual board pin number_
##### tglcount is how many times the pin should be made ___LOW-HIGH___

---

## tts.py

This script calls the Text-To-Speech using Terminal. Currently configured to use espeak
script imports _call_ from _subprocess_ for executing espeak
Functions defined: 
> TTS_call() <- Accepts string as argument. This string is passed to espeak

espeak commands:

* -f <text file> speaks a text file.
* --stdin takes the text input from stdin.
* -a <integer> sets amplitude (volume) in a range of 0 to 200. The default is 100.
* -p <integer> adjusts the pitch in a range of 0 to 99. The default is 50.
* -s <integer> sets the speed in words-per-minute (approximate values for the default English voice, others may differ slightly). The default value is 170. Range 80 to 390.
* -g <integer> inserts a pause between words. The value is the length of the pause, in units of 10 mS (at the default speed of 170 wpm).
* -l <integer> inserts a line-break length, default value 0. If set, then lines which are shorter than this are treated as separate clauses and spoken separately with a break between them. This can be useful for some text files, but bad for others.
* -w <wave file> writes the speech output to a file in WAV format, rather than speaking it.
* -z removes the end-of-sentence pause which normally occurs at the end of the text.
* --stdout writes the speech output to stdout as it is produced, rather than speaking it. The data starts with a WAV file header which indicates the sample rate and format of the data. The length field is set to zero because the length of the data is unknown when the header is produced.

---

## speech_recog.py

This script recognizes voice and converts it into text using Google Speech-To-Text API
This script defines various functions:
> ListenAudio() <- No argments. Returns audio file which consits of voice recorded after this function is called. Using default microphone source. Using adjust_ambient_noise()
 
> DecodeAudio() <- Accepts audio file as argument. Converts audio file to text using Google Speech-To-Text. Returns series of text string and prints the recognized speech on the console

> NameFind() <- Accepts a string argument and a string array, string array is searched in the string argument and if any one of the array string is found in string argument, it returns that found string, else returns 0

> CountFind()() <- Accepts a string argument. This function defines a string array of number from 1 to 10 in words. This string array is searched in the passed string argument and if any one of the array string is found in string argument, it returns that found string, else returns 0. This function also searches for numbers using isdigit() and returns it if found else return 0

> switch_numlst() <- This function is called by CountFind() to convert number in words to number in digits
