import evdev
import threading
import time





class Keyboard:

    RESTART_DELAY_SEC = 30


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

    KBD = "/dev/input/event4"
    kbd = Keyboard(KBD,None)
    input("Press enter to continue...\n\n")