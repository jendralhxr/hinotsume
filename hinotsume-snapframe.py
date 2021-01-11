import numpy as np
import math
import cv2
import sys
import random
from datetime import datetime
import csv

digit=6
marker=2
threshold=2
offset=0;

#filename="data.csv"
#with open(filename) as csv_file:
with open(sys.argv[2]) as csv_file:
    reader = csv.reader(csv_file, quoting=csv.QUOTE_NONNUMERIC);
    l = [row for row in reader];
    l_T = [list(x) for x in zip(*l)];


EDF = len(l_T[0]);
STF=36000;

cap = cv2.VideoCapture(sys.argv[1]);

for framenum in range(STF, EDF):
    for markernum in range(1,7):
        if l_T[markernum+1][framenum] > threshold:
            cap.set(cv2.CAP_PROP_POS_FRAMES, float(framenum));
            print('{}-{}'.format(framenum, markernum));
            ret, frame = cap.read()
            cv2.imwrite('{}-{}.png'.format(str(framenum).zfill(digit), markernum), frame)
            
            