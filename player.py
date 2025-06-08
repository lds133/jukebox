


import os
import time
from threading import Thread, Event, Lock
import subprocess




class Player:

    SOUND_NONE = 1
    SOUND_START = 1
    SOUND_STOP = 2
    SOUND_ERROR = 3

    SOUNDS = {  SOUND_NONE: None,
                SOUND_START : "sound/play.wav",
                SOUND_STOP : "sound/stop.wav",
                SOUND_ERROR : "sound/error.wav",
            }
    


    CMD_APLAYWAV = [r"/usr/bin/aplay","-D","default"] 
    CMD_FFMPEG = [ r"/usr/bin/ffmpeg","-i","https://frequence3.net-radio.fr/frequence3-256.mp3","-f","wav","-acodec","pcm_s16le","-ar","44100","-ac","2","-"]
    CMD_APLAY = [r"/usr/bin/aplay","-f","cd"]
    STR_AMIXER = r"/usr/bin/amixer"
    
    
    DEFAULTVOLUME = 30
    VOLUMESTEP = 5

    def __init__(self):
    
        self.thread = None
        self.p_ffmpeg = None
        self.p_aplay = None
        self.threadstopped = None
        self.threadstarted = None
        self.volume = None 
        self.mutex = Lock()
        


    def PlayUnsafe(self):
        if (self.IsPlaying):
            self.StopUnsafe()
        self.p_ffmpeg = None
        self.p_aplay = None
        self.threadstopped = Event()
        self.threadstarted = Event()
        self.thread = Thread(target = self.ThreadProc )
        self.thread.start()
        self.threadstarted.wait()
        if not self.IsCmdRunning:
            self.UnsafeStop()
            return False
        return True

    def StopUnsafe(self):
        if not self.IsPlaying:
            print(">>>","Already killed")
            return True
        print(">>>","Thread kill")
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
        return True



        
    def Play(self):
        if (self.mutex.locked()):
            print(">>>","Busy. Skip play.")
            return False
        with self.mutex:   
            rc = self.PlayUnsafe()
        return rc



    def Stop(self):
        if (self.mutex.locked()):
            print(">>>","Busy. Skip stop.")
            return False
        with self.mutex:   
            rc = self.StopUnsafe()
        return rc
    


    
    @property
    def IsCmdRunning(self):
        return self.p_ffmpeg and self.p_aplay
        
    def ThreadProc(self):
        print(">>>","Thread start")
        
        self.PlaySound(self.SOUND_START)                                
        
        try:
            self.p_ffmpeg = subprocess.Popen(
                    self.CMD_FFMPEG, 
                    stdout=subprocess.PIPE,
                    )
        except Exception as e:
            print(">>>","Error ffmpeg", str(e))
            time.sleep(0.5)
            self.PlaySound(self.SOUND_ERROR)            
            self.p_ffmpeg = None

        if self.p_ffmpeg:
            try:
                self.p_aplay = subprocess.Popen(self.CMD_APLAY, stdin=self.p_ffmpeg.stdout )
            except Exception as e:
                print(">>>","Error aplay", str(e))
                time.sleep(0.5)
                self.PlaySound(self.SOUND_ERROR)
                self.p_ffmpeg.kill() 
                self.p_aplay = None
                self.p_ffmpeg = None

        self.threadstarted.set()
        if (self.IsCmdRunning):
            print(">>>","Playing...")
            self.p_ffmpeg.wait()
            self.p_aplay.wait()
        
        time.sleep(1)
        self.PlaySound(self.SOUND_STOP)
        print(">>>","Thread stop")
        self.threadstopped.set()
        
        
       
     
    def Next(self):
        pass
        return True
        
    def ChangeVolume(self,dv):
        assert dv==1 or dv==-1 or dv==0
        if (self.volume==None):
            self.volume = self.DEFAULTVOLUME
        v = self.volume + (0 if dv==0 else (self.VOLUMESTEP if dv>0 else (-self.VOLUMESTEP)))
        return self.SetVolume(v)


        
    def RunSync(self, cmd:list[str]):
        print("Run:",cmd)
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        process.wait()
    
        
    def SetVolume(self,volume):
        self.volume = volume
        if self.volume>100:
            self.volume = 100
        if self.volume<0:
            self.volume = 0
        cmd = [self.STR_AMIXER,"set","Master",("%i%%" % self.volume)]
        self.RunSync(cmd)
        return self.volume        
        
        
    def PlaySound(self,soundtype):
        assert( soundtype in self.SOUNDS )
        filename = self.SOUNDS[soundtype]
        if not filename:
            return 
        cmd = self.CMD_APLAYWAV + [filename]
        self.RunSync(cmd)
            
        
        
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