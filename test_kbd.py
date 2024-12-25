#!/usr/bin/python3
import evdev

devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
for device in devices:
  print(device.fn, device.name, device.phys)

device = evdev.InputDevice("/dev/input/event4")
print(device)
for event in device.read_loop(): 
  print(event)