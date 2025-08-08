
import time
from keyboard import Keyboard
from player import Player
from alarm import Alarm




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

    KEY_STATE_RELEASE = 0
    KEY_STATE_PRESS = 1
    
    KEY_FAKE	=	10000
    KEY_FAKE_NONE	=	KEY_FAKE
    KEY_FAKE_STOP	=	1 + KEY_FAKE
    KEY_FAKE_PLAY	=	2 + KEY_FAKE



    def __init__(self, kbddevice, defaultvolume ):
        self.kbd = Keyboard(kbddevice,self)
        self.aud = Player()
        self.aud.SetVolume(defaultvolume)
        
    def KeyPress(self,code):
        if (code != self.KEY_FAKE_NONE):
            print("Fake keypress: %i" % code)
            self.OnKeyPressed(code,self.KEY_STATE_PRESS)
        
    def OnKeyPressed(self,code,val):
        if (val==self.KEY_STATE_RELEASE):
            return

        if (code == self.KEY_F5):
            code = self.KEY_FAKE_STOP if (self.aud.IsPlaying) else self.KEY_FAKE_PLAY


        if (code == self.KEY_FAKE_STOP):
            print("Stop!")
            self.aud.Stop()
        elif (code == self.KEY_FAKE_PLAY):
            print("Play!")
            self.aud.Play()
        elif (code == self.KEY_F6):
            v = self.aud.ChangeVolume(1)
            print("Volume:",v)
        elif (code == self.KEY_F7):
            v = self.aud.ChangeVolume(-1)
            print("Volume:",v)
        
        
        
        



        
        
if __name__ == "__main__":
        
        
    kbd_name_part = "RPI Wired Keyboard"
    kbd_phys_part = "input0"
        
        
    print("* Inet Radio Jukebox * AUG 2025")
    
    KBD = None
    while True:
        KBD = Keyboard.FindPath(kbd_name_part,kbd_phys_part)
        if (KBD == None):
            n = 300
            print("Keyboard not found. Sleep %i sec before retry." % n)
            time.sleep(n)
        else:
            print("Using keyboard: %s" % KBD)
            break
    
    VOLUME = 70
    
    box = Jukebox(KBD,VOLUME)
    alarm = Alarm(Jukebox.KEY_FAKE_NONE)
    alarm.Add(Jukebox.KEY_FAKE_STOP,23,00) # automatic turn off at night
    
    while True:
        box.KeyPress( alarm.Check() )
        time.sleep(60)        
        