import sys, math, time

emg = MuscleSensor (3)
led_object = LED (5)
servo = Servo (8)
motor = (forward = 16, backward = 20 )
t_end = time.time() + 60

while True:
    servo.min (-1)
    servo.max (1) #Replace with correct values
    servo.mid (0)

    led_object.on()
    emg_value = emg.muscle_raw()

    if emg_value == 0: #Replace with resting value or when EMG light is off and not recieving data
        while time.time() < t_end:
        motor.backward() #Change argument to speed you want

    elif emg_value >0 and emg_value < 40: #Replace values with correct range










