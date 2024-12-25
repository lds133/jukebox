import evdev
import threading






class Keyboard:

    def __init__(self, devicepath, client ):
        self.client = client
        self.thread = threading.Thread(target=self.thread_function)
        self.thread.start()
        
            
    def thread_function(self):            
        dev = evdev.InputDevice("/dev/input/event4")
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
    input("Press enter to continue...")