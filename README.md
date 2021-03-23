# Smart Vending Machine [Under development]
>Cautious! This project is still under development. Directories and files of this repo may change constantly.
### Microcontrollers used:
* Raspberry Pi for voice assistance and face recognition
* Arduino UNO for managing vending machine control functions required to move the product to the *product collect window* of the machine

### Preview of our idea:
- Raspberry Pi provides voice assistance, so the order can be made completely using voice. Face recognition helps in providing personalized voice assistance. The assistant will suggest orders to the person based on their order history.
- After confirming the order, Raspberry Pi sends the information to Arduino UNO. Arduino executes it's predefined functions which moves the selected products to the product collect window of the vending machine.

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
