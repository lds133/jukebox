# Radio Player
### Using media PC as audio player controlled from keyboard


#### Environment
linux: Ubuntu 22.04.5 LTS  
python: Python 3.10.12  
user: nuc  
folder:/home/nuc/MYPROJ/jukebox

#### Prepare

```
sudo apt install python3-dev
sudo apt install gcc
sudo apt install vlc

sudo usermod -a -G input nuc
```

open vlc on desktop and check output audio devices 

#### Setup

```
python3 -m venv .venv
source .venv/bin/activate
```
  
check if headers exists
```
sudo apt install linux-headers-$(uname -r)
```
  
make the headers available
```
export PATH="/usr/src/linux-headers-5.15.0-125/include/uapi/linux:$PATH"
```
  
install packages
```
pip install evdev
pip install python-vlc

```
or
```
pip install -r requirements.txt
```


#### Run

```
source .venv/bin/activate
python jukebox.py
```

F5 - Start / Stop
F6 - Volume up
F7 - Volume down


#### Service

```
sudo cp jukebox.service /etc/systemd/system/jukebox.service

sudo systemctl daemon-reload 

sudo systemctl enable jukebox 
```


```
sudo systemctl start jukebox 
sudo systemctl status jukebox 
sudo systemctl restart jukebox
sudo systemctl stop jukebox
journalctl -u jukebox
```



---------------



#### F5 pressed

```
event at 1735060264.801996, code 04, type 04, val 458814
event at 1735060264.801996, code 63, type 01, val 01
event at 1735060264.801996, code 00, type 00, val 00
event at 1735060264.905995, code 04, type 04, val 458814
event at 1735060264.905995, code 63, type 01, val 00
event at 1735060264.905995, code 00, type 00, val 00
```

#### F6 pressed

```
event at 1735061376.547441, code 04, type 04, val 458815
event at 1735061376.547441, code 64, type 01, val 01
event at 1735061376.547441, code 00, type 00, val 00
event at 1735061376.715284, code 04, type 04, val 458815
event at 1735061376.715284, code 64, type 01, val 00
event at 1735061376.715284, code 00, type 00, val 00
```
