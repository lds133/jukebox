import vlc
import time


URL = "test.m3u"




instance = vlc.Instance()
player = instance.media_list_player_new()
media = instance.media_list_new([URL])
player.set_media_list(media)



rc = player.play()   

assert rc!=-1

time.sleep(60)