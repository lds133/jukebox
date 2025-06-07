#!/usr/bin/python3
import evdev

print("Device list:")

devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
for device in devices:
  print( device )


devid = "/dev/input/event4"

print("")
print("Device test: "+devid)

device = evdev.InputDevice(devid)
print(device)
print("Test started. Press buttons on the PC keyboard. ")
for event in device.read_loop(): 
  print(event)