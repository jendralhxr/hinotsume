# python -u hasetraffic.py video.mp4 24000000000000 log.csv
# agglomerative contour clustering thanks to CullenSUN https://gist.githubusercontent.com/CullenSUN/d325c1c321667aab513a5e9731bda3f1/raw/879815eca2a5df9ff30ec646ab9ccd20c834015b/contours_clustering.py

import math
import cv2 as cv
import numpy as np
import sys
import csv

def calculate_contour_distance(contour1, contour2): 
    x1, y1, w1, h1 = cv.boundingRect(contour1)
    c_x1 = x1 + w1/2
    c_y1 = y1 + h1/2

    x2, y2, w2, h2 = cv.boundingRect(contour2)
    c_x2 = x2 + w2/2
    c_y2 = y2 + h2/2

    return max(abs(c_x1 - c_x2) - (w1 + w2)/2, abs(c_y1 - c_y2) - (h1 + h2)/2)

def merge_contours(contour1, contour2):
    return np.concatenate((contour1, contour2), axis=0)

def agglomerative_cluster(contours, threshold_distance=100.0):
    current_contours = contours
    while len(current_contours) > 1:
        min_distance = None
        min_coordinate = None

        for x in range(len(current_contours)-1):
            for y in range(x+1, len(current_contours)):
                distance = calculate_contour_distance(current_contours[x], current_contours[y])
                if min_distance is None:
                    min_distance = distance
                    min_coordinate = (x, y)
                elif distance < min_distance:
                    min_distance = distance
                    min_coordinate = (x, y)

        if min_distance < threshold_distance:
            index1, index2 = min_coordinate
            current_contours[index1] = merge_contours(current_contours[index1], current_contours[index2])
            del current_contours[index2]
        else: 
            break

    return current_contours
    
def take_biggest_contours(contours, max_number=20):
    sorted_contours = sorted(contours, key=lambda x: cv.contourArea(x), reverse=True)
    return sorted_contours[:max_number]    
  
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
    #cv.drawContours(cue, contours, -1, (255), 20)
    #cv.drawContours(frame_col, contours, -1, (0, 255, 0), 3)
    contours = take_biggest_contours(contours)
    #print("contours after take_biggest_contours: %s" % len(contours))
    contours = agglomerative_cluster(contours)
    #print("contours after agglomerative_cluster: %s" % len(contours))

    numlist= [framenum, M["m00"], M["m10"], M["m01"],  ];
    
    objects = []
    for c in contours:
        rect = cv.boundingRect(c)
        x, y, w, h = rect
        numlist.append([x, y, w, h])
        objects.append(rect)
    
    #if (len(objects)):
    #numlist= [framenum, M["m00"], M["m10"], M["m01"], topmost, bottommost, leftmost, rightmost];
    writer.writerow(numlist);
    
    #if (framenum):
    if (framenum%50 == 0):
        print("{} {} {}".format(framenum, M["m00"], len(objects)))
        #display=cv.resize(frame_col, vsize, interpolation= cv.INTER_AREA)
        #cv.imshow('display',frame_col)
      #  cv.imshow('display',cue)
       # k = cv.waitKey(1) & 0xFF
    
    # if k== 27: # esc
        # break
    
    
cap.release
