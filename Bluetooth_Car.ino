/* Author: Joel Ahn
 * Purpose: To enable Serial control of electronic car via Bluetooth 
 */

// Left Motors
const int enableA = 10;
const int in1 = 9;
const int in2 = 8;

//Right Motors
const int enableB = 5;
const int in3 = 6;
const int in4 = 7;

int state; 
String cmd; //The input command from the TCP to determine the car's direction
int motorspeed = 120; //the default speed. The minimum speed is 65 at 15.9V. Minimum speed is 255 at 4.8V. 
int limiter = 26; //limits PWM to ensure one wheel spins at same rpm as other (Can be scaled linearly)
const int turnlimiter = 0.9;
 
void setup(){
  pinMode (enableA, OUTPUT);
  pinMode (in1, OUTPUT);
  pinMode (in2, OUTPUT);
  pinMode (enableB, OUTPUT);
  pinMode (in3, OUTPUT);
  pinMode (in4, OUTPUT);
  
  Serial.begin(9600); 
}

//Function Prototypes
void brake(void);
void goForward(void);
void goBack(void);
void goLeft(void);
void goRight(void);

//At motor speed 255, 1100 ms is needed for the car to make a full 360 transition
void loop(){
  while (Serial.available()){
    cmd = Serial.read();
  }

  if (!Serial.available()){
    if (cmd != ""){
      
      state = cmd.toInt();
      
      switch(state){

        // Switch the motor speed
        case '1':
          motorspeed = 100;
          limiter = 20;
          Serial.println("Changing motor speed to gear 1");
          break;

        case '3':
          motorspeed = 150;
          limiter = 22;
          Serial.println("Changing motor speed to gear 2");
          break;

        case '7':
          motorspeed = 200;
          limiter = 24;
          Serial.println("Changing motor speed to gear 3");
          break;

        case '9':
          motorspeed = 250;
          limiter = 26;
          Serial.println("Changing motor speed to gear 4");
          break;
          
        // Switch direction of car
        case '5':
          brake();
          Serial.println("Braking");
          break;
          
        case '8':
          goForward();
          Serial.println("Going forward");
          break;
        
        case '4':
          goLeft();
          Serial.println("Turning Left");
          break;
        
        case '6':
          goRight();
          Serial.println("Turning right");
          break;
          
        case '2':
          goBack();
          Serial.println("Reversing");
          break;
      }

      cmd = ""; //renew the value of cmd
    }
  }
}

void brake(){
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);

  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}

void goForward(){
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(enableA, motorspeed - limiter);

  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  analogWrite(enableB, motorspeed);
 
}

void goBack(){
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  analogWrite(enableA, motorspeed - limiter);

  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  analogWrite(enableB, motorspeed);
}

void goLeft(){
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  analogWrite(enableA, motorspeed - limiter);

  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  analogWrite(enableB, motorspeed);
}

void goRight(){
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  analogWrite(enableA, motorspeed - limiter);

  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  analogWrite(enableB, motorspeed);
}
