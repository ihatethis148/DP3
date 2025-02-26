#Import all needed libraries
from sensor_library import *
import sys, math, time
from gpiozero import LED
from gpiozero import Servo
from gpiozero import Motor


#Create instances of the sensor, LED, servo, and motor with corresponding PIN
emg = MuscleSensor (0)
led_object = LED(26)
servo = Servo (8)
motor = Motor(forward = 12, backward= 16)

#Tracking variables for time to ensure user is in resting position for certain time before activating motor
obj = time.gmtime(0)
epoch = time.asctime(obj)
threshold_t = 2
start_time = None


#Define a function to get the emg value
def get_emg_value ():
    return emg.muscle_raw()

#Define a function that accepts emg values and adds them to a list
def get_rolling_avg (values_list):
    #If the length of the list == 10, calculate the average and remove the first element to update the list
    if len(values_list) == 11:
        avg = round(sum(values_list) / 10 ,2)
        values_list.pop(0)
        return avg

    #If the list is not full, output the average as None
    elif len(values_list) <10:
        return None


#Define a function that accepts the calculated average emg value to move the servo motor position
def servo_motor (avg_emg):
    global start_time
    #Servo position = 0 is going to give us the max resistance, servo position = 1 gives us no resistance

    #Do not move the servo motor when there is no average or input of invalid data, starting position is 1
    if avg_emg == None or avg_emg <65:
        servo.value = 1
    #Do not move the servo motor when user is in resting position
    elif 65 <= avg_emg <=72: #Resting Position
        servo.value = 1
        print ("Resting")
        if start_time == None:
            start_time = time.time()


    elif  72< avg_emg <=85: #Weak Position
        print ("Weak")
        servo.value = 0.7

    elif  85< avg_emg <= 100: #Intermediate Position
        print ("Intermediate")
        servo.value = 0.4

    elif 100< avg_emg <= 120: #Strong Position
        print ("Strong")
        servo.value = 0.1

    elif avg_emg >120: #Very Strong Position
        print ("Very Strong")
        servo.value = 0

#Define a function that activates the motor to reset the device when user is in resting position
def dc_motor (avg_emg):

    global start_time #Declare start_time as a global variable

    if start_time != None:
        while time.time() - start_time >= threshold_t:
            print ("Moving")
            motor.forward (speed = 0.13)
            time.sleep(3.84)
            motor.stop()
            start_time = None
            return

#Define a function that accepts the average EMG value as an argument and changes flashing speed and brightness
def led_light (avg_emg):

        if avg_emg == None or avg_emg <65: #Keep the LED light off if there is no average or invalid data
            led_object.off()


        elif 65<=avg_emg<=72: #Resting Position, keep the light dim and flash slowly
            led_object.on()
            time.sleep(2)
            led_object.off()
            time.sleep(2)


        elif 72<=avg_emg<=85: #Weak Position
            led_object.on()
            time.sleep(0.8)
            led_object.off()
            time.sleep(0.8)



        elif 85<avg_emg<=100: #Intermediate Position
            led_object.on()
            time.sleep(0.6)
            led_object.off()
            time.sleep(0.6)



        elif 100<avg_emg<=120: #Strong Position, increased brightness and fast flashing
            led_object.on()
            time.sleep(0.4)
            led_object.off()
            time.sleep(0.4)



        else: #avg_emg >120 Very Strong Position, keep the LED on
            led_object.on()
            time.sleep(0.2)
            led_object.off()
            time.sleep(0.2)

def main():

    print ("Electrical Potential Difference (Raw)", "\t", "Electric Potential Difference (Avg)", "\t", "LED Brightness", "\t", "D.C Motor", "\t","Servo Positioning")

    all_emg_values = []
    start_time = None

    while True:
        try:
            raw_emg_value = get_emg_value()
            all_emg_values.append(raw_emg_value)
            rolling_avg = get_rolling_avg(all_emg_values)

            if rolling_avg is not None:
                if rolling_avg < 65:
                    servo_position = "1"
                    motor_state = "Off"
                    led_state = "Off"
                elif 65 <= rolling_avg <= 72:
                    servo_position = "1"
                    motor_state = "Off"
                    led_state = "Slow Flash"
                elif 72 < rolling_avg <= 85:
                    servo_position = "0.7"
                    motor_state = "Off"
                    led_state = "Medium Flash"
                elif 85 < rolling_avg <= 100:
                    servo_position = "0.4"
                    motor_state = "Off"
                    led_state = "Faster Flash"
                elif 100 < rolling_avg <= 120:
                    servo_position = "0.1"
                    motor_state = "Rotating"
                    led_state = "Fast Flash"
                else:  # avg_emg > 120
                    servo_position = "0"
                    motor_state = "Rotating"
                    led_state = "Max Flash"
                print(raw_emg_value, "\t", rolling_avg, "\t",led_state,  "\t",motor_state,  "\t",servo_position)

            if rolling_avg != None:
                servo_motor(rolling_avg)
                led_light(rolling_avg)
                dc_motor(rolling_avg)

            else:
                continue

        except KeyboardInterrupt:
            led_object.off()
            motor.stop()
            servo.value = 1
            sys.exit(0)

#Main function call
main()







