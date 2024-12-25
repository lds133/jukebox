import vlc
import time



class Player:

    def __init__(self, file_m3u ):
        instance = vlc.Instance()
        self.player = instance.media_list_player_new()
        media = instance.media_list_new([file_m3u])
        self.player.set_media_list(media)
        
    def Play(self):   
        return self.player.play() 
        
    def Stop(self):   
        return self.player.stop() 
      
    def Next(self):
        return self.player.next() 
        
    def ChangeVolume(self,dv):
        value = self.player.get_media_player().audio_get_volume()    
        value+=dv
        if (value>100):
            value=100
        if (value<0):
            value=0
        self.player.get_media_player().audio_set_volume(value)
        return value
        
    @property
    def IsPlaying(self):
        return self.player.is_playing() != 0
            
            
            
if __name__ == "__main__":

    box = Player("test.m3u")
    box.Play()
    input("Press enter to continue...")