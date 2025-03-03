### Kan nog incompleet zijn!!

Gebruik deze commands voor de juiste library's enzo:
```
sudo apt update
sudo apt install python3-dev python3-pip
sudo pip3 install RPi.GPIO
sudo pip3 install rpi_ws281x
```

Moeite met de rpi_ws281x probeer:
```
sudo pip3 install rpi_ws281x --break-systeel-packages
```
Test of het correct is geinstaleerd: 
```
sudo python3 -c "import rpi_ws281x"
```
Hiervan zou je geen errors moeten krijgen.

Run file:
```
sudo python3 /home/RPI2/Documents/test1.py
```


