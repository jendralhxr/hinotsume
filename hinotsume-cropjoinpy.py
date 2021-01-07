# python hinotsum-crop.py input-video.mp4 0 82100 label.mp4
# 00000.MTS starts at 400
# 00001.MTS starts at 0

import numpy as np
import math
import cv2
import sys
import random
from datetime import datetime

THRESHOLD_VAL= 40

startx= 140
stopx= 1644
starty=388
stopy= 468

cropped_x_start= 80
cropped_x_stop= 820 # shorter window makes life easier
cropped_y_start= 0
cropped_y_stop= stopy -starty

thickness_min= 10 # maximum width of bondo
block_width= 60 # minimum width of vehicle

gate_left=  cropped_x_start+block_width # position of ID-assignment gate
gate_right= cropped_x_stop-block_width # position of ID-assignment gate

cap = cv2.VideoCapture(sys.argv[1])
cap.set(cv2.CAP_PROP_POS_FRAMES, float(sys.argv[2]))
framenum = int(sys.argv[2])

vsize = (int(1504), int(80))
out = cv2.VideoWriter(sys.argv[4],cv2.VideoWriter_fourcc(*'MP4V'), 60.0, vsize)

while(1):
#dateTimeObj = datetime.now()
#timestampStr = dateTimeObj.strftime("%H:%M:%S.%f")
#print('start: ', timestampStr)
    ret, frame = cap.read()
    cropped = frame[starty:stopy, startx:stopx]
    out.write(cropped)
    print(framenum)
    framenum += 1
    print(framenum);
    if framenum> int(sys.argv[3]):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

from moviepy.editor import VideoFileClip, concatenate_videoclips
clip_1 = VideoFileClip("0.mp4");
clip_2 = VideoFileClip("1.mp4");
final_clip = concatenate_videoclips([clip_1,clip_2])
final_clip.write_videofile("final.mp4")
