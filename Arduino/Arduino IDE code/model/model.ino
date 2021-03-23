/*
 * Mini Project FCRIT SEM 4
 * 
 * A0: Confirm Button
 * A5: -
 * Pin 2: Product 1 Interrupt Switch
 * Pin 3: Product 2 Interrupt Switch
 * Pin 4: IR Sensor (for counting)
 * Pin 5: Motor 1
 * Pin 6: Motor 2
 * Pin 7 - 12: LCD
*/

#include <LiquidCrystal.h> //import lcd library

//-------------------------PINS-------------------------------------------------
int confirmbutton = A0; // product selection confirm button
int busystatus = A5; // redundant, indicates whether vending machine is ready to take orders [for raspberry pi]



const byte product1Switch = 2; //Switch to select Product 1
const byte product2Switch = 3; //Switch to select Product 2

const byte irsens = 4; //used to count

const byte motor1 = 5; //PWM
const byte motor2 = 6; //PWM


//------------------LCD pins--------------------
LiquidCrystal lcd(7, 8, 9, 10, 11, 12); //RS, E, D4, D5, D6, D7
//----------------------------------------------
//-------------------------------------------------------------------------------



//------------------------------Variables--------------------------------------

//=====================================
//max 13 characters ["name" + ":" + xx] where xx is the product count set by the program
const String product1name = "Toblerone";
const String product2name = "FerreroRocher";
//=====================================

const byte pwm = 255; //pwm value for motor 1 and motor 2

int product1count = 0;
int product2count = 0;

//------------------------------------------------------------------------------


void setup() {
  pinMode(motor1, OUTPUT); //motor 1 transistor
  analogWrite(motor1, 0); //motor off
  
  pinMode(motor2, OUTPUT); //motor 2 transistor
  analogWrite(motor2, 0); //motor off
  
  pinMode(irsens, INPUT_PULLUP); //IR Sensor
  
  pinMode(product1Switch, INPUT_PULLUP); //switch 1 interrupt pin
  pinMode(product2Switch, INPUT_PULLUP); //switch 2 interrupt pin


//========================
  lcd.begin(16, 2); //16x2 lcd selected
//========================

  

}


void loop() {
   welcome(); //call the lcd welcome function
   enableInterrupts(); //enable switch 1 and 2 interrupts
   analogWrite(busystatus, 255); //free indication @@@ for Rasp pi

   while (analogRead(confirmbutton) > 600); //wait till user selects the product
   
   if (product1count == 0 && product2count == 0) {
       //no product selected! ignore
       
   } else {
          
          disableInterrupts(); //disable all interrupts, enabled at the start of loop()
          analogWrite(busystatus, 0); //busy indication @@@ for Rasp pi


       //--------------------------------------------Product 1----------------------------------------------------------
          if (product1count > 0) { //product 1 selected
            lcd.clear(); //clear lcd
            //lcdFirstRow(product1name + ": " + product1count); //this line is moved inside the while loop below
            lcdSecondRow("Processing..."); //Max 16 characters

            while(product1count != 0) {
              lcdFirstRow(product1name + ": " + product1count);
              analogWrite(motor1, pwm); //start motor 1
              
  bounce_err: while(digitalRead(irsens) == HIGH); //detect the product falling into the tray and decriment count by 1
              delay(100); //100ms software debounce
              if ((digitalRead(irsens)) == HIGH) {goto bounce_err;} //switch bounce, repeat check

              
              while(digitalRead(irsens) == LOW); //wait for the product to pass the ir
              
              product1count -= 1;
            }
            analogWrite(motor1, 0); //stop motor 1
            
          }



       //--------------------------------------------Product 2----------------------------------------------------------
          if (product2count > 0) { //product 2 selected
            lcd.clear(); //clear lcd
            //lcdFirstRow(product2name + ": " + product2count); //this line is moved inside the while loop below
            lcdSecondRow("Processing..."); //Max 16 characters

            while(product2count != 0) {
              lcdFirstRow(product2name + ": " + product2count);
              analogWrite(motor2, pwm); //start motor 2
              
 bounce_err2: while(digitalRead(irsens) == HIGH); //detect the product falling into the tray and decriment count by 1
              delay(100); //100ms software debounce
              if ((digitalRead(irsens)) == HIGH) {goto bounce_err2;} //switch bounce, repeat check

              
              while(digitalRead(irsens) == LOW); //wait for the product to pass the ir
              
              product2count -= 1;
            }
            analogWrite(motor2, 0); //stop motor 2
            
          }
          
   }
   

}


//---------------------------LCD------------------------------------

void welcome() {
 lcd.clear(); //Clear the LCD screen
 lcdFirstRow("Welcome!");
 lcdSecondRow(""); //Max 16 characters
}

//LCD First row
void lcdFirstRow(String msg) {
  lcd.setCursor(0,0); //cursor(column, row);
  lcd.print(msg);
}


//LCD Second row
void lcdSecondRow(String msg) {
  lcd.setCursor(0,1); //cursor(column, row);
  lcd.print(msg);
}



//---------------------------Interrupt functions for selecting product count------------------------

void enableInterrupts() {//enable interrupt pins
  attachInterrupt(digitalPinToInterrupt(product1Switch), Product1, FALLING); //goto Product1() during interrupt
  attachInterrupt(digitalPinToInterrupt(product2Switch), Product2, FALLING); //goto Product2() during interrupt
  
}

void disableInterrupts() {//disable interrupt pins
  detachInterrupt(digitalPinToInterrupt(product1Switch)); 
  detachInterrupt(digitalPinToInterrupt(product2Switch));
  
}


void Product1() {
    delayMicroseconds(1000); //software debounce
    if (digitalRead(product1Switch) == LOW) { //check if the pin is still low
      product1count += 1; //increment count by 1
    
      lcd.clear();
      lcdFirstRow(product1name + ": " + String(product1count)); //concatenate name and nos
      lcdSecondRow(product2name + ": " + String(product2count)); //concatenate name and nos
    }
    
}

void Product2() {
  delayMicroseconds(1000); //software debounce
  if (digitalRead(product2Switch) == LOW) { //check if the pin is still low
      product2count += 1; //increment count by 1
  
      lcd.clear();
      lcdFirstRow(product1name + ": " + String(product1count)); //concatenate name and nos
      lcdSecondRow(product2name + ": " + String(product2count)); //concatenate name and nos
  }
}
