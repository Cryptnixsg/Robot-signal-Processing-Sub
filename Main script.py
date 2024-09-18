import time
import RPi.GPIO as GPIO

global UltrasonicDistance  
global threshold  
global ldr_value
global Motor_Running

Motor_Running = False
intrusion_detected = False


# Define ultrasonic pins
ULTRASONIC_TRIGGER_Pin = 18  # Trigger pin
ULTRASONIC_ECHO_Pin = 16  # Echo pin for middle sensor

#Define Motor control pin
MOTOR_CONTROL = 12

#Define LED pins
Left_LED = 33   #Green LED
Right_LED = 31  #Red Led

#Define LDR pin
LDR_PIN = 13 #Change the Pin to correct one

#Define Buzzer pin
LED_ALARM = 35

#Global Variables values
AllowedDistance = 15 # Max allowable distance is 15cm

#GPIO Setmode
GPIO.setmode(GPIO.BOARD)
GPIO.setup(MOTOR_CONTROL,GPIO.OUT)
GPIO.setwarnings(False)

#PWM Setup
pwm=GPIO.PWM(MOTOR_CONTROL,50)# 50hz frequency
pwm.start(2.5)# starting duty cycle ( it set the servo to 0 degree )

# GPIO Setup
GPIO.setup(ULTRASONIC_TRIGGER_Pin, GPIO.OUT)
GPIO.setup(ULTRASONIC_ECHO_Pin, GPIO.IN)
GPIO.setup(MOTOR_CONTROL, GPIO.OUT)
GPIO.setup(LDR_PIN, GPIO.IN)
GPIO.setup(Left_LED, GPIO.OUT)
GPIO.setup(Right_LED, GPIO.OUT)
GPIO.setup(LED_ALARM, GPIO.OUT)


###Functions###

def forward():
    print("Robot is moving forward...")
    GPIO.output(LED_ALARM, False)
    for i in range(10): # Loop runs for 10 iterations
        GPIO.output(Left_LED, True) #Left LED on
        GPIO.output(Right_LED, True) #Right LED on
        time.sleep(1)
    print("Robot Moving forward sucessful") #Test 1
    # Turn off the LEDs after the loop
    GPIO.output(Left_LED, False) # Left LED off
    GPIO.output(Right_LED, False) # Right LED off

def reverse():
    print("Robot is Reversing...")
    GPIO.output(LED_ALARM, False)
    for i in range(5):  # Loop runs for 5 iterations
        GPIO.output(Left_LED, True)  # Left LED on
        GPIO.output(Right_LED, True)  # Right LED on
        time.sleep(0.5)  # Keep the LEDs on for 0.5 seconds
        GPIO.output(Left_LED, False)  # Left LED off
        GPIO.output(Right_LED, False)  # Right LED off
        time.sleep(0.5)  # Keep the LEDs off for 0.5 seconds
    print("Robot reversing is successful") #Test 2

def Turning_Right():
    print("Robot is turning Right...")
    GPIO.output(LED_ALARM, False)
    GPIO.output(Left_LED, False)  # Right LED on
    GPIO.output(Right_LED, True)  # Right LED on
    time.sleep(0.5)  # Keep the LED on for 0.5 seconds
    GPIO.output(Left_LED, False)  # Right LED off
    GPIO.output(Right_LED, False)  # Right LED off
    time.sleep(0.5)  # Keep the LED on for 0.5 seconds
    print("Robot Turning Right is successful")   #Test 3

def Turning_Left():
    print("Robot is Turning Left...")
    GPIO.output(LED_ALARM, False)
    GPIO.output(Left_LED, True)  # Left LED on
    GPIO.output(Right_LED, False)  # Right LED on
    time.sleep(0.5)  # Keep the LED on for 0.5 seconds
    GPIO.output(Left_LED, False)  # Left LED off
    GPIO.output(Right_LED, False)  # Right LED on
    time.sleep(0.5)  # Keep the LED on for 0.5 seconds
    print("Robot Turning Left is successful") #Test 4



#Motor Control and Sensor

def Turn_Motor():
    angle = 0  # Initialize angle variable
    
    # Rotate from 0 to 180 degrees (to the right)
    for angle in range(0, 181, 10):  # Change the increment value to adjust speed
        duty_cycle = 2 + (angle / 18)
        pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.1)  # Adjust delay to change rotation speed

    # Rotate from 180 to 0 degrees (to the left)
    for angle in range(180, -1, -10):  # Change the decrement value to adjust speed
        duty_cycle = 2 + (angle / 18)
        pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.1)  # Adjust delay to change rotation speed

    return angle  # Return the final angle after both loops have executed
    



# Ultrasonic sensor readings 
def getUltrasonicReadings(ULTRASONIC_TRIGGER_Pin, ULTRASONIC_ECHO_Pin):
    GPIO.output(ULTRASONIC_TRIGGER_Pin, True)
    time.sleep(0.00001)
    GPIO.output(ULTRASONIC_TRIGGER_Pin, False)

    StartTime = time.time()
    StopTime = time.time()

    while GPIO.input(ULTRASONIC_ECHO_Pin) == 0:
        StartTime = time.time()

    while GPIO.input(ULTRASONIC_ECHO_Pin) == 1:
        StopTime = time.time()

    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2  # Speed of sound = 34300 cm/s

    return round(distance, 2)

def light_detection(): #Light Detection on LDR
    # Read the LDR sensor value
    # Check if light is detected based on the LDR sensor value and threshold
        print("Light is detected!")
        print("Intruder detected!")
        GPIO.output(LED_ALARM, True) #Turn Buzzer on
        GPIO.output(Left_LED, False) #Left LED off
        GPIO.output(Right_LED, False) #Right LED off


#Evasive function 
def evasive_action(distance, angle):
    # Check for obstacles using Ultrasonic Sensor
    distance = getUltrasonicReadings(ULTRASONIC_TRIGGER_Pin, ULTRASONIC_ECHO_Pin)
    # Position-based handling of obstacle
    #motor_angle = 0  # Placeholder for motor angle value obtained from motor position
    if (0 <= angle <= 90) and (distance > AllowedDistance):  # Obstacle detected in 0-90 degrees range
        reverse()  # Reverse
        Turning_Right()  # Turn right
        print(f"Distance of Left detected obstacle: {distance} cm")  # Print detected obstacle distance
    elif (90 < angle <= 180) and (distance > AllowedDistance) :  # Obstacle detected in 180-90 degrees range
        reverse()  # Reverse
        Turning_Left()  # Turn left
        print(f"Distance of Right detected obstacle: {distance} cm")  # Print detected obstacle distance

# Main # 
def main():
    global intrusion_detected
    global Motor_Running
    global distance  # Declare distance as a global variable

    try:
        while True:
            print("Motor will start turning")
            #Turn_Motor()  # Start the motor rotation
            Turn_Motor()
            angle = Turn_Motor()
            time.sleep(2)  # Wait for 2 seconds

            # Enable ultrasonic sensor to take readings
            distance = getUltrasonicReadings(ULTRASONIC_TRIGGER_Pin, ULTRASONIC_ECHO_Pin)

            if GPIO.input(LDR_PIN) == GPIO.HIGH:
                light_detection()
            else:
                # Obtain the motor angle and distance
                distance = getUltrasonicReadings(ULTRASONIC_TRIGGER_Pin, ULTRASONIC_ECHO_Pin)
                evasive_action(distance, angle)
                forward()

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

# Call the main function to start the program
if __name__ == "__main__":
    main()
