


import os
import time
from threading import Thread, Event
import subprocess




class Player:


    CMD_FFMPEG = [ "ffmpeg","-i","https://frequence3.net-radio.fr/frequence3-256.mp3","-f","wav","-acodec","pcm_s16le","-ar","44100","-ac","2","-"]
    CMD_APLAY = ["aplay","-f","cd"]
    
    DEFAULTVOLUME = 30
    VOLUMESTEP = 5

    def __init__(self):
    
        self.thread = None
        self.p_ffmpeg = None
        self.p_aplay = None
        self.threadstopped = None
        self.threadstarted = None
        self.iskilling = False
        self.isstarting = False
        self.volume = None 
        
        
    def Play(self):
           
        if (self.isstarting):
            print(">>>","Thread start in progress")
            return
        if (self.iskilling):
            print(">>>","Thread kill in progress")
            return            

        if (self.IsPlaying):
            print(">>>","Thread restart")
            self.Stop()
            
        self.isstarting = True            
        self.iskilling = False
        self.p_ffmpeg = None
        self.p_aplay = None
        self.threadstopped = Event()
        self.threadstarted = Event()
        self.thread = Thread(target = self.ThreadProc )
        self.thread.start()
        self.threadstarted.wait()
        if not self.IsCmdRunning:
            self.Stop()
            self.isstarting = False
            return False
        self.isstarting = False
        return True
    
    @property
    def IsCmdRunning(self):
        return self.p_ffmpeg and self.p_aplay
        
    def ThreadProc(self):
        print(">>>","Thread start")
        
        try:
            self.p_ffmpeg = subprocess.Popen(
                    self.CMD_FFMPEG, 
                    stdout=subprocess.PIPE,
                    )
        except Exception as e:
            print(">>>","Error ffmpeg", str(e))
            self.p_ffmpeg = None

        try:
            self.p_aplay = subprocess.Popen(self.CMD_APLAY, stdin=self.p_ffmpeg.stdout )
        except Exception as e:
            print(">>>","Error aplay", str(e))
            self.p_aplay = None

        self.threadstarted.set()
        if (self.IsCmdRunning):
            print(">>>","Playing...")
            self.p_ffmpeg.wait()
            self.p_aplay.wait()
        self.threadstopped.set()
        print(">>>","Thread stop")
        
        

    def Stop(self):
        if not self.IsPlaying:
            print(">>>","Thread already stopped")
            return True
        if self.iskilling:
            print(">>>","Thread kill in progress")
            return False
        if self.isstarting:
            print(">>>","Thread start in progress")
            return False
            
        print(">>>","Thread kill")
        self.iskilling = True
        if self.p_ffmpeg:
            self.p_ffmpeg.kill() 
        if self.p_aplay:
            self.p_aplay.kill()
        self.threadstopped.wait()
        self.thread = None
        self.threadstopped = None
        self.threadstarted = None
        self.p_fmpeg = None
        self.p_aplay = None
        self.iskilling = False
        return True
    
    

        
        
     
    def Next(self):
        pass
        return True
        
    def ChangeVolume(self,dv):
        assert dv==1 or dv==-1 or dv==0
        if (self.volume==None):
            self.volume = self.DEFAULTVOLUME
        v = self.volume + (0 if dv==0 else (self.VOLUMESTEP if dv>0 else (-self.VOLUMESTEP)))
        return self.SetVolume(v)


        
    def SetVolume(self,volume):
        self.volume = volume
        if self.volume>100:
            self.volume = 100
        if self.volume<0:
            self.volume = 0
        VOLCMD = ["amixer","set","Master",("%i%%" % self.volume)]
        print("Run:",VOLCMD)
        process = subprocess.Popen(VOLCMD, stdout=subprocess.PIPE)
        process.wait()
        return self.volume        
        
        
        
        
    @property
    def IsPlaying(self):
        return (self.thread!=None)
            
            
            
if __name__ == "__main__":

    box = Player()

    box.Play()
    
    print("----------------- SLEEP")
    time.sleep(15)
    
    box.Stop()
    
    print("----------------- SLEEP")
    time.sleep(15)

    box.Play()
    
    print("----------------- SLEEP")
    time.sleep(15)

    box.Stop()
    
    print("*** ")    
    print("*** Warning: after the test the terminal get corrupted ")    
    print("*** To unstuck it type 'reset<enter>' (symbols will not be shown)")    
    print("*** ")    