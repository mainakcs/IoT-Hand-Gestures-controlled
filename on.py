# This file runs when the led is to be turned on

from serial import Serial
print(" I am in on")
ser = Serial("COM6", 9600, timeout = 1)
ser.write(b'B')
print("I am exiting on")

exit()