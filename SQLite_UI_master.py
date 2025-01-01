"""
This code is written by Saad Jameel
Contact: 
    email: saadjamil1998@gmail.com
    ph: +92 333 3059002 (whatsApp only)

"""

import sqlite3
from tkinter import *
import time
from PIL import Image, ImageTk
import datetime
from time import strftime
import Fingerprint_Camera as fc


serial_no = 1
conn = sqlite3.connect('Employee.db')
cur = conn.cursor()

cur.execute("""
                SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Employee_Data'
            """)
if cur.fetchone()[0]==0:
    cur.execute("""
                    CREATE TABLE Employee_Data(
                        S_No           integer         PRIMARY KEY,
                        Name            text            NOT NULL,
                        Employee_Image  blob            NOT NULL,
                        Fingerprint_1   blob            NOT NULL,
                        Fingerprint_2   blob,
                        Fingerprint1_ID integer         NOT NULL,
                        Fingerprint2_ID integer
                        )                    
                """)
    conn.commit()


def submit_fcn():
    global serial_no
    global name_entry
    global enroll_win
    # Making Label
    a = name_entry.get()
    
    if a != '':
        fc.enroll_finger()
        if fc.ui == 1:
            label1 = Label(enroll_win, text='Please! Place your finger on Scanner', font=('times',10), fg = 'black', bg='white')
        elif fc.ui == 2:
            label1 = Label(enroll_win, text='Sorry! Sensor Times Out', font=('times',15), fg = 'red', bg='white')
        elif fc.ui == 3:
            label1 = Label(enroll_win, text='This Sample Already Exists at '+str(fc.positionNumber), font=('times',15), fg = 'red', bg='white')
        elif fc.ui == 4:
            label1 = Label(enroll_win, text='Finger Captured\nRemove this Finger\nPlease Wait...', font=('times',15), fg = 'blue', bg='white')
        elif fc.ui == 5:
            label1 = Label(enroll_win, text='Please! Place same finger again.', font=('times',15), fg = 'black', bg='white')
        elif fc.ui == 6:
            label1 = Label(enroll_win, text='Ops!!! Figners does not Match...', font=('times',15), fg = 'red', bg='white')
        elif fc.ui == 7:
            label1 = Label(enroll_win, text='Figner Enrolled Sucessfully at '+str(positionNumber), font=('times',15), fg = 'Green', bg='white')
        elif fc.ui == 8:
            label1 = Label(enroll_win, text='Please Wait ... Downloading the Fingerprint\Please! Look In the Camera' , font=('times',15), fg = 'black', bg='white')
        elif fc.ui == 9:
            label1 = Label(enroll_win, text='Fingerprint and Image Captured and Stored Successfully', font=('times',15), fg = 'Blavk', bg='white')
            label2 = Label(enroll_win, text="Images Stored in 'temp' directory "+ str(positionNumber), font=('times',15), fg = 'black', bg='white')
            # fingerprint
        elif fc.ui == 10:
            label1 = Label(enroll_win, text='Operation Failed! Please, Check Console', font('times', 15), fg='red', bg='white')
        serial_no += 1
        
        
        

    else:
        error_label = Label(enroll_win, text='Please! Enter the Name First', font=('times',15), fg = 'red', bg='white')
    
    
    return

def back_fcn():
    global enroll_win
    root.deiconify()
    enroll_win.destroy()

def enrollement_fcn():
    global serial_no
    global enroll_win
    global name_entry
    root.withdraw()
    enroll_win = Toplevel()
    enroll_win.config(bg='white')
    enroll_win.attributes('-fullscreen', True)
    
    # Making Labels
    title_table = Label(enroll_win, text='ENROLLEMENT', font=('times',30), fg = 'black', bg='white')
    name_lable = Label(enroll_win, text='Name', font=('times', 15), fg='black', bg='white')
    name_entry = Entry(enroll_win, bg='yellow', borderwidth=3, width=50)
    submit_button = Button(enroll_win, text='SUBMIT', height=2, width=15, command=submit_fcn)
    back_button = Button(enroll_win, text='BACK', height=2, width=15, command=back_fcn)
    
    # Fitting On Screen
    title_table.grid(row=0, column=0, columnspan=3)
    name_lable.grid(row=1, column=0, pady=10)
    name_entry.grid(row=1, column=1, columnspan=2)
    submit_button.grid(row=2, column=2)
    back_button.grid(row=2, column=1)
    
    
    

def delete_fcn():
    return

def edit_fcn():
    return


def time_fcn():
    Time = strftime("%H : %M")
    time_main_screen.config(text=Time)
    time_main_screen.after(1000, time_fcn)
    
# Making Main Window
root = Tk()
root.configure(bg='white')
# root.geometry('800x450')
root.attributes('-fullscreen', True)

# Importing Logo
logo = ImageTk.PhotoImage(Image.open('Logo.png'))

# Making Buttons and Logo Labels
logo_label = Label(image=logo)
time_main_screen = Label(root, font=('ds-digital',25), borderwidth=2, fg = 'blue', height=1, width=6, relief='solid', bg='white')
enrollment_button = Button(root, text='ENROLLEMENT', height=2, width=15, command=enrollement_fcn)
delete_button = Button(root, text='DELETE', height=2, width=15, command=delete_fcn)
edit_button = Button(root, text='EDIT', height=2, width=15, command=edit_fcn)
exit_button = Button(root, text='EXIT', command=root.destroy)
wait_label = Label(root, text='Waiting for the Biometry....', font=('ds-digital',15), fg = 'black', bg='white')

# Calling Functions
time_fcn()


# Placing Everything in the Main Screen
logo_label.grid(row=0, column=0, columnspan=4)
time_main_screen.grid(row=1, column=3)
delete_button.grid(row=1, column=0)
enrollment_button.grid(row=1, column=1)
edit_button.grid(row=1, column=2)
exit_button.grid(row=2, column=3)
wait_label.grid(row=3, column=0, columnspan=4)





conn.close()
mainloop()