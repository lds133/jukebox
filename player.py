
import time
from threading import Thread, Event
import subprocess




class Player:


    CMD_FFMPEG = [ "ffmpeg","-i","https://frequence3.net-radio.fr/frequence3-256.mp3","-f","wav","-acodec","pcm_s16le","-ar","44100","-ac","2","-"]
    CMD_APLAY = ["aplay","-f","cd"]
    
    VOLCMDTEMPLATE = "amixer set Master %i%%"

    def __init__(self):
    
        self.thread = None
        self.p_ffmpeg = None
        self.p_aplay = None
        self.threadstopped = None
        self.threadstarted = None
        self.iskilling = False
        
        
    def Play(self):
        if (self.IsPlaying):
            self.Stop()
            
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
            return False
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
                    preexec_fn=os.setsid # detaches the subprocess from the terminal control group
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
            return True
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
        cmd = self.VOLCMDTEMPLATE % dv
        print("Run:",cmd)
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        process.wait()
        return dv
        
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
    