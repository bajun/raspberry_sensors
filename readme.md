## Raspberry Sensors

This repository contains script for obtaining data from Adafruit DHT sensor (https://www.adafruit.com/product/385) and mh-z19 sensor (https://revspace.nl/MHZ19)
It's using `aiohttp` as web-framework for rendering results and websocket connection, `Chart.js` for building graphics and specific libs for read from sensors _(I'm too lazy to play with GPIO, yeah)_ 

**Tested on Python 3.6 version.**

Installation : 
1. Plug all needed sensors according to the instructions. 
    _(don't forget to enable serial connection via `raspi-config`)_
2. Install from `requirements.txt` all needed modules
3. Make changes in your configuration files according to your setup
4. Make changes in `services/*.service` files, according to your enviroment
5. Launch services _(I recommend official manual https://www.raspberrypi.org/documentation/linux/usage/systemd.md)_
6. Enjoy :)
     
 