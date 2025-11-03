# connect

```bash
ssh root@sound-art-rpiX
```
with X being the number of the device you want to connect to.


```bash
mkdir -p /root/sound-art
cd /root/sound-art
mkdir -p /backup
git clone https://github.com/vives-project-xp/PX4-Interactive-Sound-Art.git ./backup
```


copy the py files from the backup to the main folder:
```bash
cp ./backup/Code_Raspberry_Pi/Raspberry_pi4/*.py ./
# instrumenten folder
cp -r ./backup/Geluidsbestanden/Instrumenten ./
touch ./status.json
```
```py
# in main.py
box_id = "Vul_hier_je_box_nummer_in"
```



# install dependencies
```bash
sudo apt update
sudo apt install -y \
  python3-pip python3-dev build-essential \
  libffi-dev libssl-dev \
  python3-rpi.gpio python3-numpy python3-pygame

sudo pip3 install \
  rpi_ws281x \
  flask \
  flask-cors \
  flask-socketio \
  python-socketio \
  requests \
  pygame \
  eventlet

```
# fix rpi_ws281x installation issue
```bash
sudo pip3 install rpi_ws281x --break-systeel-packages
```

# test
```bash
sudo python3 -c "import rpi_ws281x"
```


# auto start on boot
```bash
nano /etc/systemd/system/sound_player.service
```
```bash
[Unit]
Description=Sound Player Service
After=led_sensor.service sound.target
Requires=led_sensor.service

[Service]
User=root
Environment=XDG_RUNTIME_DIR=/run/user/0
Type=simple
WorkingDirectory=/root/sound-art
ExecStart=/usr/bin/python3 /root/sound-art/sound_player.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl daemon-reload
sudo systemctl enable sound_player.service
sudo systemctl start sound_player.service
```
# check status
```bash
sudo systemctl status sound_player.service
```

```bash
nano /etc/systemd/system/led_sensor.service
```
```bash
[Unit]
Description=Sound-Art Main Service (Flask + LED)
After=network.target

[Service]
Type=simple
WorkingDirectory=/root/sound-art
ExecStart=sudo python3  /root/sound-art/main.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl daemon-reload
sudo systemctl enable led_sensor.service
sudo systemctl start led_sensor.service
```
# check status
```bash
sudo systemctl status led_sensor.service
```