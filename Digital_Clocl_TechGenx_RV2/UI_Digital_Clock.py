
"""
This User Interface is developed by Saad Jameel
Contact:
    Email: saadjamil1998@gmail.com
    Ph: +92 333 3059002 (whatsApp only)
User Interface contains 2 Screens. The main screen is having the Time and Logo. It also contains 3 Buttons for the Preset countdown Time.
Second screen will count down the time as been selected in the previos screen. It also contains different animation depended upon the Client.

This code contain one exit button on the main screen that was not asked by the client. But, when client is satisfied with this HMI it will be removed
"""

from tkinter import *
from PIL import Image, ImageTk
from time import strftime
import datetime
import time

# Making the 2 Windows. One is Main and oher is for the Stopwatch
root = Tk()
root.configure(bg='white')
# Sizing the Window
root.geometry('800x450')

# Hiding the Main Ribbion
root.overrideredirect(1)

# Making Global Variable for Timer and Animations 
timer_stop_run = False
counter_value = 0
y = 0
r = 0
a = 0
ten_mins = 600
three_mins = 180
twenty_mins = 1200

# Defining Stopwatch Function User Interface
def stopwatch(setup_time):
    # Connecting Global Variables
    global timer_stop_run
    global counter_value
    global a
    # global ten_mins
    # global three_mins
    # global twenty_mins
    # Hiding the Root Window
    root.withdraw()
    # Making the Second Window
    second_window = Toplevel()
    second_window.configure(bg='white')
    second_window.geometry('800x450')
    second_window.overrideredirect(1)
    
    
    # Defining Method for Play/Pause
    def play_fcn():
        global timer_stop_run
        global counter_value
        timer_stop_run = False
        # Timer counting Down PLAY button is disabled
        pauseButton["state"] = 'normal'
        playButton["state"] = 'disabled'
        # Calling CountDown Function
        logic_down(counter_value)
       
    def pause_fcn():
        global timer_stop_run
        timer_stop_run = True
        # Timer NOT counting Down PAUSED button is disabled
        pauseButton["state"] = 'disabled'
        playButton["state"] = 'normal'        
    
    # Return Function
    def return_to_main_screen():
        global counter_value
        counter_value = 0
        # Apperaring Root Window and Destroying the Stopwatch Window
        root.deiconify()
        second_window.destroy()
    
   # Making Pause Play and Return BUTTONS
    pauseButton = Button(second_window, image = pause, borderwidth=0, command=pause_fcn, bg = 'white')
    playButton = Button(second_window, image = play, borderwidth=0, command=play_fcn, bg = 'white')
    redoButton = Button(second_window, image = redo, borderwidth=0, command=return_to_main_screen, bg = 'white')
    # ex = Button(second_window, root.destroy)
      
    # Main Logic for the Counting Down of Timer and All the ANIMATIONS
    def logic_down(down_time):
         global r
         global y
         global a
         global counter_value
         # global ten_mins
         # global three_mins
         # global twenty_mins
         
         # Extract Times Format and Place it in the Minutes and Seconds Foramt
         timer = datetime.timedelta(seconds = down_time)
         t = timer.total_seconds()
         sec = t % 60
         mins= (t%3600)//60
         
         # Configuring StopWatch Label
         stopwatch_label.config(text=" "+str(int(mins)).zfill(2)+" : "+str(int(sec)).zfill(2)+" ")
         
         # All the ANIMATION Stuff
         # When Time Less then 10 Mins Border will Toggle Between Black and Yellow
         if down_time <= ten_mins and y%2 == 1 and down_time >= three_mins:
             countdown_timer_frame.config(bg='black')
         if down_time <= ten_mins and y%2 == 0 and down_time >= three_mins:
             countdown_timer_frame.config(bg='yellow')
         
         # Simple Counting Down
         if down_time >= three_mins and timer_stop_run == False:
             stopwatch_label.after(1000, lambda: logic_down(down_time-1))
             counter_value = down_time-1
             y += 1
             
         # Time Less than 3 mins then Border will Toggle Between Red and Black
         if down_time <= three_mins and down_time != 0 and timer_stop_run == False and r%2 == 0:
             countdown_timer_frame.config(bg='red')
             stopwatch_label.after(500, lambda: logic_down(down_time))
             r += 1
         elif down_time <= three_mins and down_time != 0 and timer_stop_run == False and r%2 == 1:
             countdown_timer_frame.config(bg='black')
             stopwatch_label.after(500, lambda: logic_down(down_time-1))
             counter_value = down_time-1
             r += 1
             
         # When Timer is full off Border and Digits will toggle between Red and Black
         elif down_time == 0 and a%2 == 0 and a != twenty_mins:
             r = 0 
             y = 0
             countdown_timer_frame.config(bg='red')
             stopwatch_label.config(fg='black')
             pauseButton["state"] = 'disabled'
             playButton["state"] = 'disabled'
             a += 1
             stopwatch_label.after(1000, lambda: logic_down(0))
         elif down_time == 0 and a%2 == 1 and a != twenty_mins:
             countdown_timer_frame.config(bg='black')
             stopwatch_label.config(fg='red')
             pauseButton["state"] = 'disabled'
             playButton["state"] = 'disabled'
             a += 1
             stopwatch_label.after(1000, lambda: logic_down(0))
             
         # After 20 mins it will automatically returns to main Screen
         elif down_time == 0 and a == twenty_mins:
             pauseButton["state"] = 'disabled'
             playButton["state"] = 'disabled'
             return_to_main_screen()
             
             
    
    # Making Frame for StopWatch Timer
    countdown_timer_frame = LabelFrame(second_window, borderwidth=10, background='black', relief='flat')
    countdown_timer_frame.grid(row=0, column=0, columnspan=5, pady=30, padx=40)
    
    # Making Label for StopWatch Timer
    stopwatch_label = Label(countdown_timer_frame, fg='blue', font=('ds-digital',180), width=6, bg='white')
    second_page_logo_label = Label(second_window, image=second_page_logo, borderwidth=0)
    
    # Showing Everything on Screen
    stopwatch_label.grid(row=0,column=0, columnspan=5)
    pauseButton.grid(row=1, column=2, pady=2, padx=2)
    playButton.grid(row=1, column=1, pady=3, padx=2)
    redoButton.grid(row=1, column=3, pady=3)
    second_page_logo_label.grid(row=1, column=0)
    # ex.grid(row=2, column=0)
    
    # Disable the Play button as it is already PLAYING
    playButton["state"] = 'disabled'
    
    logic_down(setup_time)
   
    
    

# Defining Time Function, This function will updates after every minute
def time_fcn():
    time = strftime("%H : %M")
    # time_main_screen = Label(root, text=time ,font=('ds-digital',80), borderwidth=5, fg = 'blue', relief='solid', height=1, width=6)
    # time_main_screen.grid(row=3, column=0, columnspan=2 )
    time_main_screen.config(text=time)
    time_main_screen.after(1000, time_fcn)

# Importing the Logo
logo = Image.open('logo_image.jpeg')
resized_logo1 = logo.resize((500,350))
main_page_logo = ImageTk.PhotoImage(resized_logo1)
resized_logo2 = logo.resize((180,100), Image.ANTIALIAS)
second_page_logo = ImageTk.PhotoImage(resized_logo2)

# Importing Buttons Image
thirty = ImageTk.PhotoImage(Image.open('thirty.png'))
fourtyfive = ImageTk.PhotoImage(Image.open('fourtyfive.png'))
sixty = ImageTk.PhotoImage(Image.open('sixty.png'))
play = ImageTk.PhotoImage(Image.open('play.png'))
pause = ImageTk.PhotoImage(Image.open('pause.png'))
redo = ImageTk.PhotoImage(Image.open('redo.png'))

# Making Buttons
thirtyButton = Button(root, image = thirty, borderwidth=0, command=lambda: stopwatch(1*60), bg='white', height=110)
fourtyfiveButton = Button(root, image = fourtyfive, borderwidth=0, command=lambda: stopwatch(45*60), bg='white', height=90)
sixtyButton = Button(root, image = sixty, borderwidth=0, command=lambda: stopwatch((60*60)-1), bg='white',height=90 )



# Designing Main Window
logo_label = Label(image=main_page_logo, borderwidth=0)
logo_label.grid(row=0, column=0, rowspan=3, padx=30)
thirtyButton.grid(row=0, column=1, padx=50)
fourtyfiveButton.grid(row=1, column=1, pady=30)
sixtyButton.grid(row=2, column=1)

# Making Frame for the Clock
clock_frame = LabelFrame(root, borderwidth=5, background='black', relief='flat')
clock_frame.grid(row=3,column=0, columnspan=2)

# Making Time Widget
time_main_screen = Label(clock_frame, font=('ds-digital',45), borderwidth=5, fg = 'blue', height=1, width=6)
time_main_screen.grid(row=3, column=0, columnspan=2 )

# Directly Calling Time Function
time_fcn()

# Exit button for the testing Purposes Only
exit_button = Button(root, text='EXIT', command=root.destroy)
exit_button.grid(row=4, column=1)

mainloop()