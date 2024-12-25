import vlc
import time

URL = "https://frequence3.net-radio.fr/frequence3-256.mp3"
DEV = 'Built-in Audio Analog Stereo'



def get_device(player):
    mods = player.audio_output_device_enum()
    if mods:
        mod = mods
        while mod:
            mod = mod.contents
            if DEV in str(mod.description):
                device = mod.device
                module = mod.description
                return device,module
            mod = mod.next
    return None, None





instance = vlc.Instance()
player = instance.media_player_new()
media = instance.media_new(URL)
player.set_media(media)


device,module = get_device(player)
assert device!=None


player.audio_output_device_set(None,device)

vlc.libvlc_audio_output_device_set(player, module, device)


print(player.audio_output_device_get())

player.play()   
time.sleep(60)