Proteus 8
* Add the files to C:\Program Files (x86)\Labcenter Electronics\Proteus 8 Professional\DATA\LIBRARY
* Arduino will be visible in the components section inside Proteus

Library consists of
- Arduino UNO
- Arduino Mega 2560
- Arduino Mega 1280
- Arduino Nano
- Arduino Mini
- Arduino Pro Mini

How to simulate Arduino
* In the Proteus schematic window, Right click on Arduino > Edit Properties
* There will be an option to add the program file
* Import the Hex file of Arduino from the respective directory

Creating Arduino Hex file on Arduino IDE
* In Arduino IDE go to File > Preferences
* Tick Compilation

* Now after compiling the code, in the Arduino Terminal window, a .hex file location will be displayed
* Navigate to that folder from proteus and import the hex file

* In order to navigate to the hex folder, make sure hidden files are visible in Windows Explorer
* Roughly hex files are creates by the IDE in this folder C:\Users\<username>\AppData\Local\Temp\<your_arduino_build_name>
> eg C:\Users\Ashwin\AppData\Local\Temp\arduino_build_269746
