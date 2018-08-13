#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telepot
import time
import urllib3
import cv2
import numpy as np
import datetime
import os
import signal
import sys
import argparse

# ----------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument("-token","--token", type=str, help="the base", required="True")
args = parser.parse_args()

token = args.token
capture_duration = 5
cam_num = 0
video_name = ""
idd = 0

# ----------------------------------------------------------------------------------------------------------------------------------


def signal_handler(sig, frame):
    TelegramBot.sendMessage(
        int(idd), "◾ You stopped me, I´ll wait for the next time, see you!")
    sys.exit(0)

# ----------------------------------------------------------------------------------------------------------------------------------


def recordVideo():
    global video_name

    # Create a VideoCapture object
    cap = cv2.VideoCapture(cam_num)
    cap.set(3, 640)
    cap.set(4, 480)

    # Check if camera opened successfully
    if (cap.isOpened() == False):
        print("Unable to read camera feed")

    # Default resolutions of the frame are obtained.The default resolutions are system dependent.
    # We convert the resolutions from float to integer.
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
    video_name = "rec_" + datetime.datetime.today().strftime('%Y-%m-%d') + ".mp4"
    out = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(
        *'MP4V'), 20, (frame_width, frame_height))

    start_time = time.time()
    while(int(time.time() - start_time) < capture_duration):
        ret, frame = cap.read()

        if ret == True:

            # Write the frame into the file 'output.avi'
            out.write(frame)

            # Display the resulting frame
            # cv2.imshow('frame',frame)

            # Press Q on keyboard to stop recording
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break

    # When everything done, release the video capture and video write objects
    cap.release()
    out.release()

    # Closes all the frames
    cv2.destroyAllWindows()

# ----------------------------------------------------------------------------------------------------------------------------------


def handle(msg):
    global token
    global capture_duration
    global cam_num
    global idd

    content_type, chat_type, chat_id, msg_date, msg_id = telepot.glance(
        msg, long=True)
    command = msg['text']
    idd = chat_id

    if command == '/start':
        idd = chat_id
        TelegramBot.sendMessage(
            chat_id, """
Welcome to WatchMyPrinterBot made by Helguera. Any questions? Please, feel free to contact me -> @javierhelguera

⬇⬇    List of commands    ⬇⬇ 

☑ /start -> start the bot
☑ /commands -> list of commands
☑ /info -> info about the bot and its developer
☑ /checkPrinter -> sends a video of what your camera is aiming
☑ /setSeconds 'seconds' -> change seconds to be recorded

            """.format(msg["text"]))

    elif command == '/info':
        TelegramBot.sendMessage(
            chat_id, """

This bot is made to check how your 3D printer is working while you are not at home.
The easiest way to use it is executing the code in a Raspberry Pi (initial script) with a webcam connected to it

 ⬇⬇    Useful links    ⬇⬇

◾ Telegram: @javierhelguera
◾ Github: https://github.com/Helguera/WatchMyPrinterBot/blob/master/bot.py
◾ Email: contact@javierhelguera.com

            """.format(msg["text"]))

    elif command == '/commands':
        TelegramBot.sendMessage(
            chat_id, """
⬇⬇    List of commands    ⬇⬇

☑ /start -> start the bot
☑ /commands -> list of commands
☑ /info -> info about the bot and its developer
☑ /checkPrinter -> sends a video of what your camera is aiming
☑ /setSeconds 'seconds' -> change seconds to be recorded
            """.format(msg["text"]))

    elif command == '/checkPrinter':
        text = "Recording a " + str(capture_duration) + " seconds video..."
        TelegramBot.sendMessage(
            chat_id, text.format(msg["text"]))

        recordVideo()

        TelegramBot.sendMessage(
            chat_id, "Done!".format(msg["text"]))

        TelegramBot.sendMessage(
            chat_id, "Now, Sending video...".format(msg["text"]))

        TelegramBot.sendChatAction(chat_id, 'upload_video')

        r = TelegramBot.sendVideo(chat_id, open(video_name, 'rb'))
        #examine(r, telepot.namedtuple.Message)
        time.sleep(0.5)

        os.remove(video_name)

    elif '/setSeconds' in command:
        if int(command.split(" ")[1]) < 1:
            TelegramBot.sendMessage(
                chat_id, "Well... I thought you were smarter than that...".format(msg["text"]))
        else:
            capture_duration = int(command.split(" ")[1])
            text = "Received, next time I will record " + \
                str(capture_duration) + " seconds"
            TelegramBot.sendMessage(
                chat_id, text.format(msg["text"]))


# ----------------------------------------------------------------------------------------------------------------------------------
def showCameraInfo():
    1

# ----------------------------------------------------------------------------------------------------------------------------------


TelegramBot = telepot.Bot(token)

signal.signal(signal.SIGINT, signal_handler)

try:
    os.remove(video_name)
except:
    1

TelegramBot.message_loop(handle)

# Keep the program running.
while 1:
    time.sleep(10)
