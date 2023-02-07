# python -u hasetraffic.py  video.mp4 24000000000000 log.csv

import numpy as np
import math
import cv2 as cv
import sys
import csv

framenum= 0
THRESH_VAL= 40
STEP= 3

k=0

cap = cv.VideoCapture(sys.argv[1])
height = int(cap.get(cv.CAP_PROP_FRAME_WIDTH));
width = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT));
vsize = (int(height/4), int(width/4))        

lastframe= int(sys.argv[2])
csvlog = open(sys.argv[3], 'w', newline='')
writer = csv.writer(csvlog)
header= ['framenum','m00','m10','m01']
writer.writerow(header);

while (framenum<lastframe):
    ret, frame_col = cap.read()
    framenum += 1
    frame = cv.cvtColor(frame_col, cv.COLOR_BGR2GRAY)
    #print(ref.shape)
    tee = cv.bitwise_not(frame)
    
    ret,cue = cv.threshold(tee,10,255,cv.THRESH_BINARY);
        
    M = cv.moments(cue)
    numlist= [framenum, M["m00"], M["m10"], M["m01"]];
    writer.writerow(numlist);
    
    if (framenum%100 == 0):
        print("{} {}".format(framenum, M["m00"]))
        # display=cv.resize(cue, vsize, interpolation= cv.INTER_AREA)
        # cv.imshow('display',display)
        # k = cv.waitKey(1) & 0xFF
    
    # if k== 27: # esc
        # break
    
    
cap.release
