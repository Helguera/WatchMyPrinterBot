# WatchMyPrinterBot

WatchMyPrinterBot (**WMPBot**) is a Telegram Bot made to check how your 3D printer is working when you are not at home. Basically it records a video of the seconds that you want and send it to your Telegram App (desktop, web or mobile).

It's  **important** to know that this bot is not allocated on a public server. So you have to download it and execute it on a machine (preferably a Raspberry Pi) with a camera connected to it. There is a full-explained tutorial below, don't worry.

## Commands

  - **/start** - starts the bot
  - **/commands** - list of available commands
  - **/info** - displays info about the bot and its developer ([@helguera](https://github.com/helguera))
  - **/checkPrinter** - sends a video of what your camera is aiming
  - **/setSeconds 'seconds'** - change seconds to be recorded

![alt-text](https://raw.githubusercontent.com/Helguera/WatchMyPrinterBot/master/images/tutorial1.png)




## Installation
### Create a Telegram Bot
1. Start a conversation with [@BotFather](https://telegram.me/BotFather)
2. Write '*/newbot*' and follow the instructions. It will give you a **token**, please, remember it!

![alt-text](https://raw.githubusercontent.com/Helguera/WatchMyPrinterBot/master/images/tutorial2.png)
### Set up everything on a Raspberry Pi

WMPBot requires [Python2.7](https://www.python.org/), [Telepot](https://github.com/nickoala/telepot) and [OpenCV](https://opencv.org/) to run.
I'am using [Dietpi](https://dietpi.com/) with no reason, I just like it. You can use [Raspbian Stretch Lite](https://www.raspberrypi.org/downloads/raspbian/) instead.

Write the following commands one by one and relax, it will take 1 or 2 hours to install.

```sh
$ sudo apt-get install build-essential git cmake pkg-config
$ sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
$ sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
$ sudo apt-get install libxvidcore-dev libx264-dev
$ sudo apt-get install libgtk2.0-dev
$ sudo apt-get install libatlas-base-dev gfortran
$ cd ~
$ git clone https://github.com/Itseez/opencv.git
$ cd opencv
$ git checkout 3.1.0
$ cd ~
$ git clone https://github.com/Itseez/opencv_contrib.git
$ cd opencv_contrib
$ git checkout 3.1.0
```

```sh
$ sudo apt-get install python2.7-dev
$ wget https://bootstrap.pypa.io/get-pip.py
$ sudo apt-get install python
$ sudo python get-pip.py
$ pip install numpy
$ pip install telepot
$ cd ~/opencv
$ mkdir build
$ cd build
$ cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_C_EXAMPLES=OFF \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
    -D BUILD_EXAMPLES=ON .. \
    -DENABLE_PRECOMPILED_HEADERS=OFF
$ make -j4
$ sudo make install
$ sudo ldconfig
```

Well, just a few more commands to execute the bot at the boot of the Raspberry.

```sh
cd
mkdir WMPBot
cd WMPBot
wget https://raw.githubusercontent.com/Helguera/WatchMyPrinterBot/master/WMPBot.py
sudo nano /etc/rc.local
```

Write this line in the rc.local file:
```sh
python /root/WMPBot/WMPBot.py -token 'THE TOKEN TELEGRAM GAVE YOU'
```
Ctrl+O to save and Ctrl+X to exit. And **finished!**
### Tech

WMPBot uses a two open source projects to work properly:

* [Telepot](https://github.com/nickoala/telepot) - Python framework for Telegram Bot API 
* [OpenCV](https://opencv.org/) - Open Source Computer Vision Library

### Development

You are free to use, copy, modify and share this code. But please, always give credits.


