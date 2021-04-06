# Smart Vending Machine [Under development]
>Cautious! This project is still under development. Directories and files of this repo may change constantly.
### Microcontrollers used:
* Raspberry Pi for voice assistance and face recognition
* Arduino UNO for managing vending machine control functions required to move the product to the *product collect window* of the machine

### Preview
- Raspberry Pi provides voice assistance, so the order can be made completely using voice. Face recognition helps in providing personalized voice assistance. The assistant will suggest orders to the person based on their order history.
- After confirming the order, Raspberry Pi sends the information to Arduino UNO. Arduino executes it's predefined functions which moves the selected products to the product collect window of the vending machine.

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
- Switch 1 and 2 is connected to pin 2 and 3 respectively for interrupting the Arduino. Switches are pulled_high internally by Arduino. Pressing the switch will make the respective Arduino pin LOW. ***Interrupt is initialized during the falling edge of the pulse.***
- Switch 3 is pulled_high externally using a 10k resistor. Pressing the switch makes the respective Arduino pin \(A0\) LOW. Switch 3 does not have interrupt function. Arduino keeps polling this switch logic inside the *void loop()*.
- IR Sensor OUT pin is connnected to Arduino D4 pin. IR Sensor gives HIGH o/p when no object is placed in front of it and LOW when an object is detected. Arduino keeps polling this switch for controlling the motor rotation inside *void loop()*

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

---

### Arduino and Raspberry Pi integration ###
Arduino UNO busy flag: A5 pin
* LOW: Still processing the previous order
* HIGH: Ready to take the next order
