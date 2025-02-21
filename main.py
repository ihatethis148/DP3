#Import all needed libraries
from sensor_library import *
import sys, math, time
from gpiozero import Servo
from gpiozero import Motor
from gpiozero import PWMLED

#Create instances of the sensor, LED, servo, and motor with corresponding PIN numbers
emg = MuscleSensor (0)
led_object = LED(5)
servo = Servo (8)
motor = Motor(forward = 12, backward= 16)

#Tracking variables for time to ensure user is in resting position for certain time before activating motor
t_start = None
t_end = None
threshold_t = 5


#Define a function to get the emg value
def get_emg_value ():
    return emg.muscle_raw()

#Define a function that accepts emg values and adds them to a list
def get_rolling_avg (emg_value, values_list):
    values_list.append(emg_value)
    #If the length of the list == 10, calculate the average and remove the first element to update the list
    if len(values_list) == 10:
        avg = round(sum(values_list) / len(values_list),2)
        values_list.pop(0)

    #If the list is not full, output the average as None
    elif len(values_list) <10:
        avg = None

    #Return the average emg value
    return avg


#Define a function that accepts the calculated average emg value to move the servo motor position
def servo_motor (avg_emg):

    #while True:
    #avg_emg = rolling_avg(get_emg_value(), all_emg_values)

    #Do not move the servo motor when there is no average or input of invalid data
    if avg_emg == None or avg_emg <65:
        servo.value = 0
    #Do not move the servo motor when user is in resting position
    elif 65 <= avg_emg <=72: #Resting Position
        servo.value = 0

    elif  72< avg_emg <=85: #Weak Position
        servo.value = 0.4

    elif  85< avg_emg <= 100: #Intermediate Position
        servo.value = 0.6

    elif 100< avg_emg <= 120: #Strong Position
        servo.value = 0.8

    elif avg_emg >120: #Very Strong Position
        servo.value = 1.0

#Define a function that activates the motor to reset the device when user is in resting position
def dc_motor (avg_emg):

    global t_start #Declare t_start as a global variable

    #Check if avg_emg is in resting position
    if 65<=avg_emg<=72: #First time the emg value is in resting position range
        if t_start == None:
            t_start = time.time() #Start the timer

        elif time.time() - t_start >= threshold_t: #Check if the time passed surpassed threshold time
            motor.forward()
            time.sleep(5) #Change the time depending on how much it needs to be pushed back
            motor.stop()
            t_start = None #Reset the timer once motor spins everything back in position


    else: #Do not start the timer if not in range of resting value
        t_start = None


#Define a function that accepts the average EMG value as an argument and changes flashing speed and brightness
def led_light (avg_emg):

        if avg_emg == None or avg_emg <65: #Keep the LED light off if there is no average or invalid data
            led_object.off()


        elif 65<=avg_emg<=72: #Resting Position, keep the light dim and flash slowly
            led_object.value(0.2)
            time.sleep(2)
            led_object.off()


        elif 72<=avg_emg<=85: #Weak Position
            led_object.value (0.4)
            time.sleep(0.8)
            led_object.off()



        elif 85<avg_emg<=100: #Intermediate Position
            led_object.value(0.6)
            led_object.on()
            time.sleep(0.6)
            led_object.off()



        elif 100<avg_emg<=120: #Strong Position, increased brightness and fast flashing
            led_object.value (0.8)
            time.sleep(0.4)
            led_object.off()



        else: #avg_emg >120 Very Strong Position, keep the LED on
            led_object.on()

def main():

    all_emg_values = []

    while True:
        try:
            raw_emg_value = get_emg_value()
            rolling_avg = get_rolling_avg(raw_emg_value, all_emg_values)

            if rolling_avg != None:
                servo_motor(rolling_avg)
                led_light(rolling_avg)
                dc_motor(rolling_avg)

        except KeyboardInterrupt:
            led_object.off()
            motor.stop()
            servo.value = 0
            sys.exit(0)



'''def data_input (): #Function to calculate the rolling average using data input
    #Initialize an empty list to store our EMG values to keep updating the rolling average
    all_emg_values = []
    #Continuiously recieve data from the data and append to the list
    while True:
        emg_value = emg.muscle_raw()
        all_emg_values.append(emg_value)
        #If the list does not have enough values to calculate the average, output None
        if len(all_emg_values) <10:
            avg = None #Make sure to double check if this is correct

        if len(all_emg_values) == 10:
            avg = round(sum(all_emg_values) / len(all_emg_values),2)
            all_emg_values.pop (0)
            all_emg_values.append(emg_value)

        return avg
'''









