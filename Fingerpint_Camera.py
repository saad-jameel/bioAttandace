"""
Interfacing Camera and FingerPrint Sensor
This code is written by Saad Jameel
Contact: 
    email: saadjamil1998@gmail.com
    ph: +92 333 3059002 (whatsApp only)

"""

import time
from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER2
import tempfile
import picamera

def my_sleep_fcn(n):
    t = time.time()
    while int(time.time()) - int(t) != n:
        pass
    return
ui = 0
positionNumber = 0
f = ""
def check_sensor():
    global f
    try:
        f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)
        
        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')
            return False

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        exit(1)
    print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))
    return True

def enroll_finger():
    global f
    global found_match
    global taken_image
    global ui
    global positionNumber
    camera.start_preview()
    time.sleep(1)
    try:
        ui = 1
        print('Waiting for finger...')

        ## Wait that finger is read
        start = time.time()
        while ( f.readImage() == False ):
            if int(time.time())-int(start) == 30:
                ui = 2
                print("FingerPrint Enrollement Time-Out")
                return False
            pass
        
        
        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(FINGERPRINT_CHARBUFFER1)
    
        ## Checks if finger is already enrolled
        result = f.searchTemplate()
        positionNumber = result[0]
    
        if ( positionNumber >= 0 ):
            ui = 3
            print('Template already exists at position #' + str(positionNumber))
            exit(0)
        
        ui = 4
        print('Remove finger...')
        time.sleep(2)
        
        ui = 5
        print('Waiting for same finger again...')
    
        ## Wait that finger is read again
        start = time.time()
        while ( f.readImage() == False ):
            if (int(time.time())-int(start) == 30):
                ui = 2
                print("Finger Enrollement Time-Out")
                return False
            pass
    
        ## Converts read image to characteristics and stores it in charbuffer 2
        f.convertImage(FINGERPRINT_CHARBUFFER2)
    
        ## Compares the charbuffers
        if ( f.compareCharacteristics() == 0 ):
            ui = 6
            raise Exception('Fingers do not match')
    
        ## Creates a template
        f.createTemplate()
    
        ## Saves template at new position number
        positionNumber = f.storeTemplate()
        ui = 7
        print('Finger enrolled successfully!')
        print('New template position #' + str(positionNumber))
        
#         Making The Image
        ui = 8
        print('Downloading image (this take a while)...')

        imageDestination =  tempfile.gettempdir() + '/'+str(positionNumber)+'.bmp'
        f.downloadImage(imageDestination)
        camera.capture(tempfile.gettempdir() +'/'+str(positionNumber)".jpg")
        
        ui = 9
        print('The image was saved to "' + imageDestination + '".')
        print('Picture also captured')
    except Exception as e:
        ui = 10
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)

def find_id():
    ## Tries to search the finger and calculate hash
    try:
        print('Waiting for finger...')
    
        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass
    
        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(FINGERPRINT_CHARBUFFER1)
        taken_image=True
        ## Searchs template
        result = f.searchTemplate()
    
        positionNumber = result[0]
        accuracyScore = result[1]
    
        if ( positionNumber == -1 ):
            found_match=False
            print('No match found!')
            exit(0)
        else:
            found_match=True
            print('Found template at position #' + str(positionNumber))
            print('The accuracy score is: ' + str(accuracyScore))
    
#         ## OPTIONAL stuff
#         ##
#     
#         ## Loads the found template to charbuffer 1
#         f.loadTemplate(positionNumber, FINGERPRINT_CHARBUFFER1)
#     
#         ## Downloads the characteristics of template loaded in charbuffer 1
#         characterics = str(f.downloadCharacteristics(FINGERPRINT_CHARBUFFER1)).encode('utf-8')
#     
#         ## Hashes characteristics of template
#         print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())
    
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)

def delete_identity():
        ## Tries to delete the template of the finger
    try:
        positionNumber = input('Please enter the template position you want to delete: ')
        positionNumber = int(positionNumber)
    
        if ( f.deleteTemplate(positionNumber) == True ):
            print('Template deleted!')
    
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        exit(1)

if check_sensor() == True:
    a = input("Press 'e' for Enrollement\n"
                "Press 'f' for Finding Print\n"
                "Press 'd' for Delete Finger\n")
    if a == 'e':
        enroll_finger()
        camera.stop_preview()
    elif a == 'f':
        find_id()
    elif a == 'd':
        delete_identity()
    else:
        print("Wrong Selection")

