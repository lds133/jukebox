# Internet Radio Jukebox
### Using media PC as audio player controlled from local keyboard


#### Environment
linux: Ubuntu 22.04.5 LTS  
python: Python 3.10.12  
user: nuc  
folder:/home/nuc/MYPROJ/jukebox
  
    
	

#### Prepare
```
sudo apt update
sudo apt install python3-dev
sudo apt install gcc
sudo apt install ffmpeg
sudo apt install alsa-utils
```

```
sudo usermod -a -G input $USER
sudo usermod -aG audio $USER
```
:warning: Logout and login after group update



#### Setup

```
python3 -m venv .venv
source .venv/bin/activate
```
  
install packages
```
pip install evdev
```
or
```
pip install -r requirements.txt
```
#### Aplay

List devices
```
dima@ivan-pc:~$ aplay -l
**** List of PLAYBACK Hardware Devices ****
card 0: PCH [HDA Intel PCH], device 0: ALC3246 Analog [ALC3246 Analog]
  Subdevices: 0/1
  Subdevice #0: subdevice #0
card 0: PCH [HDA Intel PCH], device 3: HDMI 0 [HDMI 0]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 0: PCH [HDA Intel PCH], device 7: HDMI 1 [HDMI 1]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 0: PCH [HDA Intel PCH], device 8: HDMI 2 [HDMI 2]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
dima@ivan-pc:~$
```

Test speaker
```
speaker-test -D hw:0,0 -c 2 -t wav
```

Test stream
```
ffmpeg -i https://frequence3.net-radio.fr/frequence3-256.mp3 -f wav -acodec pcm_s16le -ar 44100 -ac 2 - | aplay -f cd -D hw:0,0
```

Set default aplay device 

```
nano ~/.asoundrc
```
```
pcm.!default {
    type hw
    card 0
    device 0
}

ctl.!default {
    type hw
    card 0
}

```

Test ffmpeg and aplay
```
ffmpeg -i https://frequence3.net-radio.fr/frequence3-256.mp3 -f wav -acodec pcm_s16le -ar 44100 -ac 2 - | aplay -f cd
```


Test mixer
```
amixer set Master 10%-
amixer set Master 10%+
```


#### Run

run test_kbd.py to find the keyboard, update the KBD constant in jukebox.py 

```
source .venv/bin/activate
python jukebox.py
```

F5 - Start / Stop  
F6 - Volume up  
F7 - Volume down  


#### Service

```
sudo cp jukebox.service /etc/systemd/system/jukebox.service
sudo systemctl daemon-reload 
sudo systemctl enable jukebox 
sudo systemctl start jukebox 
```


```
sudo systemctl start jukebox 
sudo systemctl status jukebox 
sudo systemctl restart jukebox
sudo systemctl stop jukebox
journalctl -u jukebox
```



