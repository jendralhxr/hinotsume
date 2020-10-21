# python hinotsume-track.py input-video.mp4 reference-image.png 0 82100 label.mp4  cue.mp4
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
ref= cv2.imread(sys.argv[2])
vsize = (int(1504), int(80))

temp= ref
image_prev= ref
image_display= ref
out = cv2.VideoWriter(sys.argv[5],cv2.VideoWriter_fourcc(*'MP4V'), 60.0, vsize)
out2 = cv2.VideoWriter(sys.argv[6],cv2.VideoWriter_fourcc(*'MP4V'), 60.0, vsize)

cap.set(cv2.CAP_PROP_POS_FRAMES, float(sys.argv[3]))
framenum = int(sys.argv[3])

while(1):
	#dateTimeObj = datetime.now()
	#timestampStr = dateTimeObj.strftime("%H:%M:%S.%f")
	#print('start: ', timestampStr)
	ret, frame = cap.read()
	cropped = frame[starty:stopy, startx:stopx]
	
	# crop and subtract .item(reference] background
	difference= cv2.absdiff(ref, cropped)
	ret,thresh = cv2.threshold(difference,THRESHOLD_VAL,255,cv2.THRESH_BINARY);
	#print(thresh.shape)
	image_cue = cv2.bitwise_and(cropped, thresh)
	
	#dateTimeObj = datetime.now()
	#timestampStr = dateTimeObj.strftime("%H:%M:%S.%f")
	#print('crop: ', timestampStr)
	
	for i in range(cropped_x_start, cropped_x_stop-1):
		for j in range(cropped_y_stop-1, cropped_y_start, -1):
			if  image_cue.item(j,i,1) > THRESHOLD_VAL: # if detect object, based on green
				image_cue.itemset((1,i,0) , 255) # blue
				image_cue.itemset((3,i,2) , 0) # clear the ID, if noise happens
				image_cue.itemset((5,i,2) , 0) # clear the ID, if noise happens
				break
	
	#dateTimeObj = datetime.now()
	#timestampStr = dateTimeObj.strftime("%H:%M:%S.%f")
	#print('scan: ', timestampStr)
	
	# join to obtain contiguous block using green lines	
	block_start= 0	
	for i in range(cropped_x_start, cropped_x_stop-1):
		if image_cue.item(1,i,0) > THRESHOLD_VAL:
			block_start= i
		else:
			if (i-block_start) < thickness_min: 
				image_cue.itemset((1,i,1) , 255) # green
				image_cue.itemset((3,i,2) , 0) # clear the ID, if noise happens
				image_cue.itemset((5,i,2) , 0) # clear the ID, if noise happens
			else: 
				block_start= 0
	
	#dateTimeObj = datetime.now()
	#timestampStr = dateTimeObj.strftime("%H:%M:%S.%f")
	#print('bondo: ', timestampStr)
	
	block_start= 0
	block_end= 0
	image_display= cropped
	for i in range(cropped_x_start, cropped_x_stop-1):
		if (image_cue.item(1,i,0) != 0 or image_cue.item(1,i,1) != 0) and block_start==0:
			block_start= i
		elif (image_cue.item(1,i,0) == 0 and image_cue.item(1,i,1) == 0) and block_end==0:
			block_end= i
			#remove spurious lines less than minimum block width
			if ((block_end-block_start) <= block_width) and block_start!=0 and block_end != 0:
				for n in range(block_start, block_end):
					image_cue.itemset((1,n,0) , 0) # blue
					image_cue.itemset((1,n,1) , 0) # green
					image_cue.itemset((1,n,2) , 0) # red
			
			# apply identifier
			elif (block_start!= 0) and (block_end != 0):
				# from right: red: 1 to 99
				# from left: 101 to 200
				#print("{} start{} stop{}".format(framenum, block_start, block_end))
				
				#from left gate
				if (block_start < gate_left) and (block_end > gate_left):
					vehicle_id=  image_prev.item(3, int((block_start + block_end)/2) ,2)
					if (vehicle_id == 0) :
						vehicle_id= random.randint(1, 99)
						#if (image_prev.item(3, int((block_start + block_end)/2) ,2] == 0):
						#print("{} {} {} {} leftnew".format(vehicle_id, framenum, block_start, block_end))
					for n in range(block_start, block_end):
						image_cue.itemset((3,n,2) , vehicle_id)
				
				# from right gate
				elif (block_start < gate_right) and (block_end > gate_right):
					vehicle_id= image_prev.item(5, int((block_start + block_end)/2) ,2)
					if (vehicle_id == 0) :
						vehicle_id= random.randint(101, 199)
						#if (image_prev.item(2, int((block_start + block_end)/2) ,2] == 0):
						#print("{} {} {} {} rightnew {}".format(vehicle_id, framenum, block_start, block_end, gate_right))
					for n in range(block_start, block_end):
						image_cue.itemset((5,n,2) , vehicle_id)
				
				# retain the value while in the middle
				else:
				#if (block_start >= gate_left) and (block_end <= gate_right):
					# left to right
					vehicle_id = 0
					for n in range(block_start, block_end, 2):
						vehicle_id = image_prev.item(3, n, 2)
						if (vehicle_id != 0):
							break
					if ( vehicle_id != 0) :
						print("{} {} {} {} 1".format(vehicle_id, framenum, block_start, block_end)) # left is '1'
						start_point = (block_start, 8) 
						end_point = (block_end, 72) 
						label_point= (block_start+10, 30)
						cv2.rectangle(image_display, start_point, end_point, (255,36,12), 2) # blue
						cv2.putText(image_display, str(vehicle_id), label_point, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,36, 12), 2)
						for n in range(block_start, block_end):
							image_cue.itemset((3,n,2),  vehicle_id)
					# right to left
					for n in range(block_end, block_start, -2):
						vehicle_id = image_prev.item(5, n, 2)
						if (vehicle_id != 0):
							break
					if ( vehicle_id != 0) :
						print("{} {} {} {} 0".format(vehicle_id, framenum, block_start, block_end)) # right is '0'
						start_point = (block_start, 8) 
						end_point = (block_end, 72) 
						label_point= (block_start+10, 65)
						cv2.rectangle(image_display, start_point, end_point, (12,36,255), 2) # red
						cv2.putText(image_display, str(vehicle_id), label_point, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (12,36, 255), 2)
						for n in range(block_start, block_end):
							image_cue.itemset((5,n,2), vehicle_id)
							
			block_start= 0
			block_end= 0
	
	#dateTimeObj = datetime.now()
	#timestampStr = dateTimeObj.strftime("%H:%M:%S.%f")
	#print('traffic: ', timestampStr)
	
	image_prev= image_cue;

	#draw the gate
	for j in range(cropped_y_start, cropped_y_stop):
		image_display.itemset((j,gate_left,1) , 255) # green
		image_display.itemset((j,gate_right,1) , 255) # green
	
	#cv2.imshow('display',image_display)
	#cv2.imshow('cue',image_cue)
	
	#k = cv2.waitKey(1) & 0xFF
	#if k== ord("c"):
	#	print("snap reference")
	#	cv2.imwrite("ref.png", cropped)
	#if k== 27: # esc
	#	break
	
	out.write(image_display)
	out2.write(image_cue)
	
	dateTimeObj = datetime.now()
	timestampStr = dateTimeObj.strftime("%H:%M:%S.%f")
	print('time: ', timestampStr)
	
	#print(framenum)
	framenum += 1
	if framenum> int(sys.argv[4]):
		break
	
cap.release()
out.release()
cv2.destroyAllWindows()
