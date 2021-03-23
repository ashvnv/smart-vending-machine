## Arduino UNO pins used
---
* D2 <= Product 1 Interrupt Switch (Pulled-Up)
* D3 <= Product 2 Interrupt Switch (Pulled-Up)
---
* D4 <= IR Sensor 
---
* D5 <= Product 1 Motor
* D6 <= Product 2 Motor
---
* D7 <= LCD RS
* D8 <= LCD E
* D9 <= LCD D4
* D10 <= LCD D5
* D11 <= LCD D6
* D12 <= LCD D7
---
* A0 <= Order Confirm Switch
* A5 <= Busy Status
---
## Functions ##
* void setup()
> sets the input and output pins of arduino. LCD 16x2 lcd.begin called in this function
* void loop()
> Loop function continuously checks the *order confirm button* state. If the button is pressed (State becomes low), the conditional statement checks how many quantity of Product 1 and 2 consumer wants. If those registers are both 0, program goes back to the start of the loop() where it checks for the *order confirm button* state again. If the registers are not 0, loop function turns on the motor and waits till the required quantity of the chosen product reaches the *product collect window*. IR sensor is used to detect how many specified products passed and according decrements the count registers. Motor is ON till the count register becomes 0. This operation is done individually for Product 1 and Product 2, starting with Product 1. In this function Interrupts are disabled since vending machine is not ready for next order. A5 pin is made LOW here. Once the processing is done (all the products were dispatched), interrupts are enabled and A5 is made high stating that vending machine is ready for the next command.
---
* void welcome()
> Display Welcome! message on LCD when the vending machine is ready to take orders. Welcome message can be set in this function. Message size can is 16x2 characters
* void lcdFirstRow (String msg)
> Used to write \<msg\>  in the first row of LCD
* void lcdSecondRow (String msg)
> Used to write \<msg\>  in the second row of LCD
---
* void enableInterrupts()
> Enable interrupt pin 2 and 3 to call interrupt functions. Uses attachInterrupt() Arduino function
* void disableInterrupts()
> Disable interrupt pin 2 and 3. Uses detachInterrupt() Arduino function
---
* void Product1()
> Called when Product 1 Switch is pressed. Increments the count in Product1 register. Count indicates how many nos of the product consumer wants. Used later inside loop() while processing the order. Also updates the LCD screen with the quantity of product.
* void Product2()
>Called when Product 2 Switch is pressed. Increments the count in Product2 register. Count indicates how many nos of the product consumer wants. Used later inside loop() while processing the order. Also updates the LCD screen with the quantity of product.
---
## How switch bouncing is tackled ##
In order to tackle switch bouncing, a delay code is added while checking the state of the buttons. 
> bounce_err: while(digitalRead(irsens) == HIGH); //detect the product falling into the tray and decriment count by 1\
              delay(100); //100ms software debounce\
              if ((digitalRead(irsens)) == HIGH) {goto bounce_err;} //switch bounce, repeat\ 

irsens is the pin where IR sensor is connected. goto is used for jumping the program to the previous stage if the Arduino misread the pin state in while();
Inside ISR, delay() function cannot be called. So instead we are using delayMicroseconds() for generating small delay.
> delayMicroseconds(1000); //software debounce\
  if (digitalRead(product2Switch) == LOW)
 
 If the pin-state does not remain the same after delay, ISR is ignored and no registers are incremented.
