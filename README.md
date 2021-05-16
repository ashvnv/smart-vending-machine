# Smart Vending Machine [Under development]
>Cautious! This project is still under development. Directories and files of this repo may change constantly.
### Boards used:
* Raspberry Pi for voice assistance and face recognition
* Arduino UNO for managing vending machine control functions required to move the product to the *product collect window* of the machine

### Preview
- Raspberry Pi provides voice assistance, so the order can be made completely using voice. Face recognition helps in providing personalized voice assistance. The assistant will suggest orders to the person based on their order history.
- After confirming the order, Raspberry Pi sends the information to Arduino UNO. Arduino executes it's predefined functions which moves the selected products to the product collection window of the vending machine.

### Block Diagram
![BD](https://raw.githubusercontent.com/ashvnv/smart-vending-machine/main/temp/BD2.png)

### Vending machine model ###
For now a small model of vending machine will be used to simulate the working of the project. There will only be two products in the vending machine. The products will be placed on a spiral (spring) which will be rotated by a motor. Arduino will be controlling this motor's rotation. An IR sensor will be used to count how many products moved into the *product collect window*. Arduino stops the motor when all the required number of products are dispatched successfully.\
Initially the model will be tested without Raspberry Pi\
There will be 3 switches:
* Switch 1 <= Selecting Product 1
* Switch 2 <= Selecting Product 2
* Switch 3 <= Confirm the order

Each time Switch 1 or 2 is pressed, the quantity of that product increments by 1. Everything is displayed on a LCD. Switch 3 is used to confirm the order.
> Later on Raspberry Pi will replace these switches

### Switch logic ###
> All the pinouts are mentioned in the Arduino code and the Readme file inside the Arduino folder of this repository
- Switch 1 and 2 are connected to pins 2 and 3 respectively for interrupting the Arduino. Switches are pulled_high internally by Arduino. Pressing the switch will make the respective Arduino pin LOW. ***Interrupt is initialized during the falling edge of the pulse.***
- Switch 3 is pulled_high externally using a 10k resistor. Pressing the switch makes the respective Arduino pin \(A0\) LOW. Switch 3 does not have interrupt function. Arduino keeps polling this switch logic inside the *void loop()*.
- IR Sensor OUT pin is connected to Arduino D4 pin. IR Sensor gives HIGH o/p when no object is placed in front of it and LOW when an object is detected. Arduino keeps polling this switch for controlling the motor rotation inside *void loop()*

### Repository directory structure ###
> The functions of this project is divided between Arduino and Raspberry Pi and the directories are made accordingly. 
---
* Arduino
  * Arduino IDE Code
    * model <- ***Arduino .ino files***  
  * Proteus Simulation
     * Arduino 328 <- ***Proteus simulation of Arduino part of vending machine***
     * Arduino Proteus Library <- ***Arduino simulation library files for proteus***
---
* Raspberry Pi
  * piycodes
    * main.py <- ***main script calls other scripts during execution***
    * tts.py <- ***Text-To-Speech function defined***
    * speech_recog.py <- ***Speech recognition script***

* config.txt <- ***IFTTT KEY and EVENT NAME***
* iftttlog.py <- ***Log the data in google sheets using IFTTT-Webhooks***
* start.py <- ***On startup, Raspberry Pi executes this script***

---
### Data logging using IFTTT ###
- IFTTT is used to log the data in Google Sheets. Logging helps in tracking the Raspberry Pi script execution and determining errors. This comes in handy when Raspberry Pi is mounted onto the vending machine as debugging becomes difficult in this case since connecting external display and keyboard everytime might not be feasible.
- https://ifttt.com An applet is created which is connected to Webhooks and Google sheets service. A POST web request is made with curl in linux along with a JSON data which includes the data to be logged. Read the documentation of Webhooks from here https://ifttt.com/maker_webhooks
> logdata()
- Function accepts two string parameters, \<filename\> and \<log\>, both strings. Uses curl to make a POST request to webhooks and triggers the event. Function reads the config.txt file to get the IFTTT key and event name. 
- config.txt file path can be changed from here inside iftttlog.py
> configfilepath = os.path.expanduser('~/') + '/Desktop/config.txt'
- Syntax of file:<br>
KEY<br>
EVENTNAME
 - Sample config.txt is added in the same directory
 - Function prints 0, indicating that the data was logged successfully
 - Also prints the log serially using *print*

#### Data logging example ###
![log](https://raw.githubusercontent.com/ashvnv/smart-vending-machine/main/temp/googlesheets.png)
> Google Sheets preview
---

### start.py (Raspberry Pi startup script) ###
- When Raspberry Pi boots up, this script is called automatically by adding the path to the startup programs. start.py executes some very important commands which helps in execution of Raspberry Pi
#### Script execution flow: ####
1) Check Internet connection
- The script keeps looping in the same place until Raspberry Pi is connected to a network. Network connection is checked by pinging http://google.com

2) Update the cloned github repository (smart-vending-machine); this script should remain inside smart-vending-machine repository, git pull does not work from other paths
- Once a connection is established, the script then updates the local clone of this repository. This is important as Raspberry Pi can be updated remotely without any need for removing it from a model and attaching external display and keyboard. git is used to achieve this. All the local changes, temporary files are discarded using *git reset --hard* & *git clean -fd* followed by *git pull* which updates the local repository.

3) Call the main.py script <- restart raspberry pi if error encountered (commented)
- After updating the local repository, the script finally calls the main.py inside the Raspberry Pi > piycodes folder. Path of the file can be adjusted by setting the *MAIN_PATH = "~/smart-vending-machine/Raspberry\ Pi/piycodes/main.py"* in start.py script. 

#### ABSOLUTE FILE PATHS ARE USED. IF THE FILES LOCATION IS CHANGED, OTHER SCRIPTS MAY NOT BE ABLE TO CALL THE NECESSARY Python SCRIPTS. IT IS RECOMMENDED TO UPDATE THE PATH INSIDE THE PROGRAMS IF THE FILE LOCATION IS CHANGED. ####
#### THIS REPOSITORY IS INTENDED TO BE CLONED IN THE HOME DIRECTORY (~) AS SCRIPTS PATH IS SET RELATIVE TO HOME DIRECTORY. IF LOCATION IS CHANGED, WITHOUT UPDATING THE PATH INSIDE THE SCRIPTS, THE PROGRAM MAY RETURN AN ERROR ####
> In case of an error, start.py can reboot the system using *os.system("reboot")*, but this is commented as of now

### Arduino and Raspberry Pi integration ###
Arduino UNO busy flag: A5 pin
* LOW: Still processing the previous order
* HIGH: Ready to take the next order

Inside main.py
> def SwitchToggle(pin, tglcount)

The function takes two parameters: pin number and tglcount. Both are integers values. Pin Number is the GPIO pin number the not the actual Raspberry Pi board pin number.
