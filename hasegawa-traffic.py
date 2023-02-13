# python -u hasetraffic.py  video.mp4 24000000000000 log.csv

import math
import cv2 as cv
import numpy as np
import sys
import csv

def find_if_close(cnt1,cnt2):
    row1,row2 = cnt1.shape[0],cnt2.shape[0]
    for i in range(row1):
        for j in range(row2):
            dist = np.linalg.norm(cnt1[i]-cnt2[j])
            if abs(dist) < 50 :
                return True
            elif i==row1-1 and j==row2-1:
                return False
                
framenum= 0
THRESH_VAL= 40
STEP= 3

k=0

cap = cv.VideoCapture(sys.argv[1])
height = int(cap.get(cv.CAP_PROP_FRAME_WIDTH));
width = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT));
vsize = (int(height/2), int(width/2))        

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
    
    contours,hierarchy = cv.findContours(cue, 1, 2)
    #cv.drawContours(frame_col, contours, -1, (0, 255, 0), 3)
    #print( len(cnt) )
    LENGTH = len(contours)
    status = np.zeros((LENGTH,1))
    
    for i,cnt1 in enumerate(contours):
        x = i    
        if i != LENGTH-1:
            for j,cnt2 in enumerate(contours[i+1:]):
                x = x+1
                dist = find_if_close(cnt1,cnt2)
                if dist == True:
                    val = min(status[i],status[x])
                    status[x] = status[i] = val
                else:
                    if status[x]==status[i]:
                        status[x] = i+1

    unified = []
    maximum = int(status.max())+1
    for i in range(maximum):
        pos = np.where(status==i)[0]
        if pos.size != 0:
            cont = np.vstack(contours[i] for i in pos)
            hull = cv.convexHull(cont)
            unified.append(hull)

    cv.drawContours(frame_col,unified,-1,(0,255,0),2)
    cv.drawContours(cue,unified,-1,255,-1)
    
    numlist= [framenum, M["m00"], M["m10"], M["m01"]];
    #numlist= [framenum, M["m00"], M["m10"], M["m01"], topmost, bottommost, leftmost, rightmost];
    writer.writerow(numlist);
    
    #  if (framenum):
    if (framenum%50 == 0):
        print("{} {}".format(framenum, M["m00"]))
        display=cv.resize(frame_col, vsize, interpolation= cv.INTER_AREA)
        cv.imshow('display',frame_col)
        k = cv.waitKey(1) & 0xFF
    
    # if k== 27: # esc
        # break
    
    
cap.release
