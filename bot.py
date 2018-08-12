import telepot
import time
import urllib3
import cv2
import numpy as np
import time



# ----------------------------------------------------------------------------------------------------------------------------------

def recordVideo():
    start_time = time.time()
    while(int(time.time() - start_time) < capture_duration):
        ret, frame = cap.read()
 
        if ret == True: 
     
            # Write the frame into the file 'output.avi'
            out.write(frame)
 
            # Display the resulting frame    
            #cv2.imshow('frame',frame)
 
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

def examine(result, type):
    try:
        print 'Examining %s ......' % type

        nt = type(**result)
        assert equivalent(result, nt), 'Not equivalent:::::::::::::::\n%s\n::::::::::::::::\n%s' % (result, nt)

        if type == telepot.namedtuple.Message:
            print 'Message glance: %s' % str(telepot.glance(result, long=True))

        pprint.pprint(result)
        pprint.pprint(nt)
        print
    except AssertionError:
        traceback.print_exc()
        answer = raw_input('Do you want to continue? [y] ')
        if answer != 'y':
            exit(1)

def handle(msg):

    content_type, chat_type, chat_id, msg_date, msg_id = telepot.glance(msg, long=True)
    command = msg['text']

    if command == '/start':
        TelegramBot.sendMessage(
            chat_id, "Welcome to my bot".format(msg["text"]))
    elif command == '/info':
        TelegramBot.sendMessage(
            chat_id, "Grabando video (10s)...".format(msg["text"]))
        
        recordVideo()
        
        TelegramBot.sendMessage(
            chat_id, "Enviando...".format(msg["text"]))

        TelegramBot.sendChatAction(chat_id, 'upload_video')

        r = TelegramBot.sendVideo(chat_id, open('outpy.mp4', 'rb'))
        #examine(r, telepot.namedtuple.Message)
        time.sleep(0.5)

        try:
            file_id = r['video']['file_id']

            TelegramBot.sendVideo(chat_id, file_id, duration=5, caption='Hong Kong traffic',
                          reply_to_message_id=msg_id, reply_markup=nt_show_keyboard)
            time.sleep(0.5)
            TelegramBot.sendVideo(chat_id, file_id, reply_markup=remove_keyboard)
            time.sleep(0.5)

        except KeyError:
            # For some reason, Telegram servers may return a document.
            print '****** sendVideo returns a DOCUMENT !!!!!'

            file_id = r['document']['file_id']

            TelegramBot.sendDocument(
                chat_id, file_id, reply_to_message_id=msg_id, reply_markup=nt_show_keyboard)
            time.sleep(0.5)
            TelegramBot.sendDocument(chat_id, file_id, reply_markup=remove_keyboard)
            time.sleep(0.5)

# ----------------------------------------------------------------------------------------------------------------------------------

token = '561324939:AAHSxWRMaRjwSNcIWgTCtrSoXCQY1uxBHiY'
TelegramBot = telepot.Bot(token)

capture_duration = 8
 
# Create a VideoCapture object
cap = cv2.VideoCapture(0)
 
# Check if camera opened successfully
if (cap.isOpened() == False): 
  print("Unable to read camera feed")
 
# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
 
# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
out = cv2.VideoWriter('outpy.mp4',cv2.VideoWriter_fourcc(*'MP4V'), 20, (frame_width,frame_height))

TelegramBot.message_loop(handle)

print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
