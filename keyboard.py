import evdev
import threading
import time





class Keyboard:

    RESTART_DELAY_SEC = 30

    @staticmethod
    def FindPath(KBD_MARK_NAME,KBD_MARK_PHYS):
        for device in [evdev.InputDevice(path) for path in evdev.list_devices()]:
            if KBD_MARK_NAME==None or len(KBD_MARK_NAME)==0 or (KBD_MARK_NAME in device.name):
                if KBD_MARK_PHYS==None or len(KBD_MARK_PHYS)==0 or (KBD_MARK_PHYS in device.phys):
                    return device.path
        return None
    
    @staticmethod
    def PrintAll():
        for device in [evdev.InputDevice(path) for path in evdev.list_devices()]:
            print(device.path," : ", device.name," - ", device.phys)  


    def __init__(self, devicepath, client ):
        self.devicepath = devicepath
        self.client = client
        self.thread = threading.Thread(target=self.thread_function_withrestart)
        self.thread.start()
        
        
    def thread_function_withrestart(self):                    
        
        while(True):
        
            print("Keyboard start")
            try:
                self.thread_function() 
            except Exception as e:
                print("Keyboard exception: "+str(e))
                print("Keyboard wait %i secons before restart..." % (int(self.RESTART_DELAY_SEC)))
                time.sleep(self.RESTART_DELAY_SEC)
                print("\n")
                



    def thread_function(self):            
        dev = evdev.InputDevice(self.devicepath)
        print("Using:",dev)    
        for event in dev.read_loop(): 
            if event.type != 1:
                continue        
            if (self.client==None):
                print(event)
            else:
                self.client.OnKeyPressed(event.code,event.value)   
            
            
            
            
if __name__ == "__main__":

    KBD = Keyboard.FindPath("RPI Wired Keyboard","input0")
    if KBD!=None:
        kbd = Keyboard(KBD,None)
        input("Press enter to continue...\n\n")
    else:
        print("Keyboard not found\n")
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            print(device.path," : ", device.name," - ", device.phys)        