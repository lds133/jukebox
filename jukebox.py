
import time
from keyboard import Keyboard
from player import Player





class Jukebox():


    KEY_F1		=	59
    KEY_F2		=	60
    KEY_F3		=	61
    KEY_F4		=	62
    KEY_F5		=	63
    KEY_F6		=	64
    KEY_F7		=	65
    KEY_F8		=	66
    KEY_F9		=	67
    KEY_F10		=	68


    def __init__(self, kbddevice, defaultvolume ):
        self.kbd = Keyboard(kbddevice,self)
        self.aud = Player()
        self.aud.SetVolume(defaultvolume)
        
        
    def OnKeyPressed(self,code,val):
        if (val==0): # key release
            return

        if (code == self.KEY_F5):
            if (self.aud.IsPlaying):
                print("Stop!")
                self.aud.Stop()
            else:
                print("Play!")
                self.aud.Play()
            return
            
        if (code == self.KEY_F6):
            v = self.aud.ChangeVolume(1)
            print("Volume:",v)
            return
                
        if (code == self.KEY_F7):
            v = self.aud.ChangeVolume(-1)
            print("Volume:",v)
            return
        
        
        
        
if __name__ == "__main__":
        
    KBD = "/dev/input/event4"   
    VOLUME = 30
    
    print("* Inet Radio Jukebox * DEC 2024")
    
    box = Jukebox(KBD,VOLUME)
    
    while True:
        time.sleep(60)