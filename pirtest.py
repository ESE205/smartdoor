import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.IN)
GPIO.setup(3,GPIO.OUT)
while True:
    i=GPIO.input(12)
    if i==0:
        print("No intruders", i)
        GPIO.output(3,0)
        time.sleep(0.1)
    elif i==1:
        print("Intruder detected", i)
        GPIO.output(3,1)
        time.sleep(0.1)
