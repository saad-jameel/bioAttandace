########################################################
"""
This code is written by Saad Jameel
Contact: 
    email: saadjamil1998@gmail.com
    ph: +92 333 3059002 (whatsApp only)
"""
########################################################

# Interfacing FignerPrint Sensor and SQLite DataBase.
# Saved Finger's Unique ID is saved in SQLite DataBase.

########################################################

import time
# import board
# import busio
from digitalio import DigitalInOut, Direction
import adafruit_fingerprint
import RPi.GPIO as GPIO
import sqlite3                                     # For SQL Database
from datetime import datetime, timezone            # For Storing Time in Database

# Onboard Running Time
a = datetime.now(timezone.utc)
my_time = a.strftime("%d-%m-%Y  %H:%M")

# PushButton and LEDs Setup
detected_finger = 5    
reg_button = 6         
error_led = 26          
GPIO.setup(detected_finger, GPIO.OUT)
GPIO.setup(error_led, GPIO.OUT)
GPIO.setup(reg_button, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Pin is High, Button would be reference to ground

# Open / Making Database
SQL_DB = sqlite3.connect("Access_Members_List.sqlite")
point = SQL_DB.cursor()

# Bit for Registeration
FLAG = 0
if GPIO.input(reg_button) == GPIO.LOW:
    FLAG = 1

# Making Table in SQL Database
point.executescript('DROP TABLE IF EXISTS Identification; CREATE TABLE Identification (id INTEGER PRIMARY KEY, DateTime TEXT)');
SQL_DB.commit()

# For Raspberry Pi TTL Convertor
import serial
uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)


# Checking FingerPrint Stored
def get_fingerprint(flag):
    """Get a finger print image, template it, and see if it matches!"""
    print("Waiting for image...")
    while finger.get_image() != adafruit_fingerprint.OK and flag != 1:
        if GPIO.input(reg_button) == GPIO.LOW:
            flag = 1
        pass
    print("Templating...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    print("Searching...")
    if finger.finger_search() != adafruit_fingerprint.OK:
        return False
    return True


# For Enrolling New Fingers
""" REMEMBER!!!
    For Storing New Fingers you have to place it twice
"""

# When Program is in Storing Mode One LED will on Everytime to Let User Know.
# When Any Error Falls Other LED will Blink.
def enroll_finger(location):
    print("ENROLLMENT")
    for fingerimg in range(1, 3):
        GPIO.output(detected_finger, True)
        if fingerimg == 1:
            print("Place finger on sensor...", end="", flush=True)
        else:
            print("Place same finger again...", end="", flush=True)

        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                print("Image taken")
                break
            if i == adafruit_fingerprint.NOFINGER:
                print(".", end="", flush=True)
            elif i == adafruit_fingerprint.IMAGEFAIL:
                GPIO.output(error_led, True)
                print("Imaging error")
                return False
            else:
                GPIO.output(error_led, True)
                print("Other error")
                return False

        print("Templating...", end="", flush=True)
        i = finger.image_2_tz(fingerimg)
        if i == adafruit_fingerprint.OK:
            print("Templated")
        else:
            if i == adafruit_fingerprint.IMAGEMESS:
                GPIO.output(error_led, True)
                print("Image too messy")
            elif i == adafruit_fingerprint.FEATUREFAIL:
                GPIO.output(error_led, True)
                print("Could not identify features")
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                GPIO.output(error_led, True)
                print("Image invalid")
            else:
                GPIO.output(error_led, True)
                print("Other error")
            return False

        if fingerimg == 1:
            GPIO.output(detected_finger, False)
            print("Remove finger")
            time.sleep(1)
            while i != adafruit_fingerprint.NOFINGER:
                i = finger.get_image()

# If Finger is Enrolled Twice It will Generate an Error
    print("Creating model...", end="", flush=True)
    i = finger.create_model()
    if i == adafruit_fingerprint.OK:
        if finger.finger_search() == adafruit_fingerprint.OK:
            GPIO.output(error_led, True)
            print("Finger Enrolled Previously!")
            return False
        print("Created")
        
# Storing New Users in the Database Their User ID and Time 
        point.execute('INSERT INTO Identification (DateTime, id) VALUES (?,?)',(my_time, userid))
        SQL_DB.commit()
        GPIO.output(detected_finger, True)
    else:
        GPIO.output(error_led, True)
# If Print Missmatches ERROR LED Will Lightup
        if i == adafruit_fingerprint.ENROLLMISMATCH:
            print("Prints did not match")
            time.sleep(1)
        else:
            print("Other error")
            time.sleep(1)
        return False

    print("Storing model #%d..." % location, end="", flush=True)
    i = finger.store_model(location)
    if i == adafruit_fingerprint.OK:
        print("Stored")
    else:
        GPIO.output(error_led, True)
        if i == adafruit_fingerprint.BADLOCATION:
            print("Bad storage location")
        elif i == adafruit_fingerprint.FLASHERR:
            print("Flash storage error")
        else:
            print("Other error")
        return False

    GPIO.output(detected_finger, False)
    return True



while True:
    
    if GPIO.input(reg_button) == GPIO.LOW:
        FLAG = 1
    else:
        FLAG = 0
    userid = len(finger.templates) + 1

# When Memory is FULL 
    if userid >= 128:
        print("Sorry! Memory Full")
        GPIO.output(error_led, True)
    
    print("----------------")
    if finger.read_templates() != adafruit_fingerprint.OK:
        raise RuntimeError("Failed to read templates")
    print("Fingerprint templates:", finger.templates)
    print("----------------")

# Routine for Storing New FingerID
    if FLAG == 1:
        enroll_finger(userid)
        time.sleep(2)
        GPIO.output(error_led, False)
        GPIO.output(detected_finger, False)

# Routine for Checking ID
    if FLAG == 0:
        GPIO.output(detected_finger, False)
        if get_fingerprint(FLAG):
            GPIO.output(detected_finger, True)
            print("Detected #", finger.finger_id, "with confidence", finger.confidence)
            time.sleep(1)
            GPIO.output(detected_finger, False)
        else:
            GPIO.output(error_led, True)
            print("Finger not found")
            time.sleep(1)
            GPIO.output(error_led, False)
            
# It is of No USE for User. This is for DEVELOPERS 
    point.execute('SELECT * FROM Identification')
    data = point.fetchall()
    print(data)


