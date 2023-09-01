# This file runs when led is to be turned off

from serial import Serial
print("I am in off")
ser = Serial("COM6", 9600, timeout = 1)
ser.write(b'b')
print("I am exiting off")

exit()