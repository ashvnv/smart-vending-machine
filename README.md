# Smart Vending Machine [Under development]
>Cautious! This project is still under development. Directories and files of this repo may change constantly.
### Microcontrollers used:
* Raspberry Pi for voice assistance and face recognition
* Arduino UNO for managing vending machine control functions required to move the product to the *product collect window* of the machine

### Preview
- Raspberry Pi provides voice assistance, so the order can be made completely using voice. Face recognition helps in providing personalized voice assistance. The assistant will suggest orders to the person based on their order history.
- After confirming the order, Raspberry Pi sends the information to Arduino UNO. Arduino executes it's predefined functions which moves the selected products to the product collect window of the vending machine.

### Vending machine model ###
For now a small model of vending machine will be used to simulate the working of the project. There will only be two products in the vending machine. The products will be placed on a spiral (spring) which will be rotated by a motor. Arduino will be controlling this motor's rotation. An IR sensor will be used to count how many products moved into the *product collect window* and according Arduino stops the motor when all the required number of product is successfully dispatched.\
Initially the model will be tested without Raspberry Pi.\
There will be 3 switches:
* Switch 1 <= Selecting Product 1
* Switch 2 <= Selecting Product 2
* Switch 3 <= Confirm the order

Each time Switch 1 or 2 is pressed, the quantity of that product increments by 1. Everything is displayed on a LCD. Switch 3 is used to confirm the order.\
> Later on Raspberry Pi will replace these switches


### Directory Structure ###
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
>Arduino UNO busy flag: A5 pin
>* LOW: Still processing the previous order
>* HIGH: Ready to take the next order
