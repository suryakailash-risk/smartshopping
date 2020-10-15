import os
from Tkinter import *
import smbus
import time

def fun():
    #!/usr/bin/env python

    import RPi.GPIO as GPIO
    from mfrc522 import SimpleMFRC522
    reader = SimpleMFRC522()

    try:
        id, text = reader.read()
        print(id)
        print(text)
        
        Wprice = 100
        Cprice = 30
        Bprice = 70
        Mprice = 50
        tt=text
        uu=str(id)
        price = 0
        list.append(1)
        if (uu == '630315633063'):
            price = Wprice
        if (uu == '936755026282'):
            price = Bprice
        if (uu == '901151880100'):
            price = Cprice
        if (uu == '656907585949'):
            price = Mprice
        
        n = len(list)
        size = 0
        for i in range(n):
            size+=list[i]
        total.append(price)
        tn = len(total)
        tamt = 0
        for j in range(tn):
            tamt+=total[j]
        print(price)
        frame = Frame(win, bg="white")
        frame.pack(fill='x',pady=10)

        w = Label(frame, text=size)
        w.pack(padx=50, pady=5, side="left")
        w = Label(frame, text=tt)
        w.pack(padx=30, pady=5, side="left")
        w = Label(frame, text=price)
        w.pack(padx=50, pady=5, side="left")
        w = Label(frame, text="1" )
        w.pack(padx=50, pady=5, side="left")
        bl.config(text=tamt, bg="white")
        
        
        sd =" "+tt+"="+str(price)
        sd.strip()
        tl=" Total = "+str(tamt)
        print(sd)
        # Send some test
        lcd_string("      E-Kart    ",LCD_LINE_1)
        lcd_string(sd,LCD_LINE_2)
        lcd_string("                ",LCD_LINE_3)
        lcd_string(tl,LCD_LINE_4)

        time.sleep(1)
        
    finally:
        GPIO.cleanup()

def Rst():
    del list[:]
    del total[:]
    for wid in win.winfo_children():
        wid.destroy()
    
    home()
    customerid.append(1)
    kk=len(customerid)
    cs = 0
    for i in range(kk):
        cs+=customerid[i]
    
    cl.config(text=cs, bg="white")
    # Send some test
    lcd_string("                ",LCD_LINE_1)
    lcd_string("                ",LCD_LINE_2)
    lcd_string("                ",LCD_LINE_3)
    lcd_string("                ",LCD_LINE_4)

    time.sleep(1)
    
    
# Define some device parameters
I2C_ADDR  = 0x27 # I2C device address
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable bit

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1


def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = the data
  # mode = 1 for data
  #        0 for command

  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  # High bits
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  # Low bits
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  # Toggle enable
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def home():
    l1=Label(win, text="Smart E-Kart", bg="white")
    l1.config(font=("Courier", 25))
    l1.pack(fill='x',pady=10)

    customerframe = Frame(win, bg="white")
    customerframe.pack(fill='x',pady=10)

    c = Label(customerframe, text="Customer ID : ")
    c.pack(padx=5, pady=10, side="left")

    cl = Label(customerframe, text=cs, bd=5)
    cl.pack(padx=5, pady=10, side="left")

    B1 = Button(customerframe, text="Reset", command=Rst, bd =5)
    B1.pack(padx=5, pady=10, side="left")

    A1 = Button(customerframe, text="ADD", command=fun, bd =5)
    A1.pack(padx=5, pady=10, side="left")



    frame = Frame(win)
    frame.pack(fill='x',pady=10)

    w = Label(frame, text="Sl.No")
    w.pack(padx=50, pady=10, side="left")
    w = Label(frame, text="Product Name")
    w.pack(padx=50, pady=20, side="left")
    w = Label(frame, text="Price")
    w.pack(padx=50, pady=20, side="left")
    w = Label(frame, text="Qty" )
    w.pack(padx=50, pady=20, side="left")

    frameb = Frame(win, bg="white")
    frameb.pack(fill='x',pady=10, side="bottom")

    w = Label(frameb, text="Total : ", bg="white" )
    w.pack(padx=50, pady=20, side="left")
    bl = Label(frameb, text="0", bg="white" )
    bl.pack(padx=50, pady=20, side="left")


customerid=[]
customerid.append(1000)
cs=customerid
list=[]
total=[]
win = Tk()
win.title("Smart E-Kart")
win.configure(background="white")
win.attributes('-zoomed', True)
l1=Label(win, text="Smart E-Kart", bg="white")
l1.config(font=("Courier", 25))
l1.pack(fill='x',pady=10)

customerframe = Frame(win, bg="white")
customerframe.pack(fill='x',pady=10)

c = Label(customerframe, text="Customer ID : ")
c.pack(padx=5, pady=10, side="left")

cl = Label(customerframe, text=cs, bd=5)
cl.pack(padx=5, pady=10, side="left")

B1 = Button(customerframe, text="Reset", command=Rst, bd =5)
B1.pack(padx=5, pady=10, side="left")

A1 = Button(customerframe, text="ADD", command=fun, bd =5)
A1.pack(padx=5, pady=10, side="left")



frame = Frame(win)
frame.pack(fill='x',pady=10)

w = Label(frame, text="Sl.No")
w.pack(padx=50, pady=10, side="left")
w = Label(frame, text="Product Name")
w.pack(padx=50, pady=20, side="left")
w = Label(frame, text="Price")
w.pack(padx=50, pady=20, side="left")
w = Label(frame, text="Qty" )
w.pack(padx=50, pady=20, side="left")

frameb = Frame(win, bg="white")
frameb.pack(fill='x',pady=10, side="bottom")

w = Label(frameb, text="Total : ", bg="white" )
w.pack(padx=50, pady=20, side="left")
bl = Label(frameb, text="0", bg="white" )
bl.pack(padx=50, pady=20, side="left")

lcd_init()

win.mainloop()




