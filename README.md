# Internet Radio Jukebox
### Using media PC as audio player controlled from local keyboard


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



