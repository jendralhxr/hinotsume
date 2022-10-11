#!/usr/bin/python3
# python hinotsume-track.py input-video.mp4 reference-image.png 0 82100 label.mp4  cue.mp4
# 00000.MTS starts at 400
# 00001.MTS starts at 0

import numpy as np
import math
import cv2
import sys
import random
#from skimage import morphology
from datetime import datetime

THRESHOLD_VAL= 30
FRAME_STEP= 10

# margin in the actual image, to be cropped
startx= 880               
stopx= 4096
starty=0
stopy= 480

# image section to be processed, within cropped area
cropped_x_start= 0
cropped_x_stop= 800 # shorter window makes life easier
cropped_y_start= 0
cropped_y_stop= 120

thickness_min_horizontal= 20 # maximum width of bondo
thickness_min_vertical= 10 # maximum width of bondo
block_width= 100 # minimum width of vehicle
update_interval= 200 # frames

digit=8;

gate_left=  cropped_x_start+block_width # position of ID-assignment gate
gate_right= cropped_x_stop-block_width # position of ID-assignment gate

cap = cv2.VideoCapture(sys.argv[1])
ref= cv2.imread(sys.argv[2])
vsize = (int((stopx-startx)/4), int((stopy-starty)/4))

image_display= ref
#ref = ref[starty:stopy, startx:stopx] # if reference image is not cropped already

out = cv2.VideoWriter(sys.argv[5],cv2.VideoWriter_fourcc(*'MP4V'), 60.0, vsize)
out2 = cv2.VideoWriter(sys.argv[6],cv2.VideoWriter_fourcc(*'MP4V'), 60.0, vsize)

cap.set(cv2.CAP_PROP_POS_FRAMES, float(sys.argv[3]))
framenum = int(sys.argv[3])
FRAME_STEP= int(sys.argv[7])
update= 0

while(1):
	#dateTimeObj = datetime.now()
	#timestampStr = dateTimeObj.strftime(vh"%H:%M:%S.%f")
	#print('start: ', timestampStr)
	ret, frame = cap.read()
	
#	print(frame.shape)
#	print(ref.shape)
	
	# crop and subtract .item(reference] background
	difference= cv2.absdiff(ref, frame)
	ret,thresh = cv2.threshold(difference,THRESHOLD_VAL,255,cv2.THRESH_BINARY);
	image_cue = cv2.bitwise_and(frame, thresh)
	
	#dateTimeObj = datetime.now()
	#timestampStr = dateTimeObj.strftime("%H:%M:%S.%f")
	#print('crop: ', timestampStr)
	
	# blue: object 
	# green: bondo (probable object behind occlusion)
	# red: assigned ID
	
	for i in range(cropped_x_start, cropped_x_stop-1):
		for j in range(cropped_y_stop-1, cropped_y_start+1, -1):
			if  image_cue.item(j,i,1) > THRESHOLD_VAL: # if detect object, based on green
				#print("f{} j{} i{}".format(framenum, j, i))
				image_cue.itemset((1,i,0) , 255) # blue
				image_cue.itemset((3,i,2) , 0) # clear the ID, if noise happens
				image_cue.itemset((5,i,2) , 0) # clear the ID, if noise happens
				break

	# join to obtain contiguous block using green lines	
	block_start= 0	
	for i in range(cropped_x_start, cropped_x_stop-1):
		if image_cue.item(1,i,0) > THRESHOLD_VAL:
			block_start= i
		else:
			if (i-block_start) < thickness_min_horizontal: 
				image_cue.itemset((1,i,1) , 255) # green
				image_cue.itemset((3,i,2) , 0) # clear the ID, if noise happens
				image_cue.itemset((5,i,2) , 0) # clear the ID, if noise happens
			else: 
				block_start= 0
	
	block_start= 0
	block_end= 0
	vehicle_detect= 0
	
	image_display= frame
	
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
					image_cue.itemset((3,n,2) , 0) # red
					image_cue.itemset((5,n,2) , 0) # red
			
			height_start= 99999999 
			height_end= 0
			for i in range(block_start, block_end-1):
				for j in range(cropped_y_stop-2, cropped_y_start+6, -1):
					if image_cue.item(j,i,1) != 0:
						if (j < height_start):
							height_start= j
						if (j > height_end):
							height_end= j
					start_point = (block_start, height_start)   #CHECKHERE!!
					end_point = (block_end, height_end)	  #CHECKHERE!!
					label_point= (block_start+10, height_end-20)
					cv2.rectangle(image_display, start_point, end_point, (255,36,12), 2) # blue
					cv2.putText(image_display, str(vehicle_id), label_point, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,36, 12), 2)
					print("{} {} {} {} {} {} 1".format(vehicle_id, framenum, block_start, block_end, height_start, height_end)) # left is '1'
							
			block_start= 0
			block_end= 0
	
	#draw the gate
	for j in range(cropped_y_start, cropped_y_stop):
#		image_display.itemset((j,gate_left,1) , 255) # green
#		image_display.itemset((j,gate_right,1) , 255) # green
		image_cue.itemset((j,gate_left,1) , 255) # green
		image_cue.itemset((j,gate_right,1) , 255) # green
	
	# update the reference background
	update= update+FRAME_STEP
	#print("{}/{} v{}".format(update, update_interval, vehicle_detect))
	if (vehicle_detect==0) and (update>update_interval):
		print("{}/{} f{}".format(update, update_interval, framenum))
		update = 0
		ref= cropped
	
	cv2.imshow('display',image_display)
	cv2.imshow('cue',image_cue)
	#image_display_resized=cv2.resize(image_display, vsize, interpolation= cv2.INTER_AREA)
	#image_cue_resized = cv2.resize(image_cue, vsize, interpolation = cv2.INTER_AREA)
	#cv2.imshow('display',image_display_resized)
	#cv2.imshow('cue',image_cue_resized)
	   
	dateTimeObj = datetime.now()
	timestampStr = dateTimeObj.strftime("%H:%M:%S.%f")
	
	k = cv2.waitKey(1000) & 0xFF
	if k== ord("c"):
		print("saving: "+str(framenum).zfill(digit)+'.png')
	#	cv2.imwrite(str(framenum).zfill(digit)+'.png', frame)
		ref= frame
	if k== 27: # esc
		break
	
	out.write(image_display)
	out2.write(image_cue)
	#out.write(image_display_resized)
	#out2.write(image_cue_resized)
	
	print('time: ', timestampStr, "framenum: ", str(framenum));
	framenum += FRAME_STEP
	cap.set(cv2.CAP_PROP_POS_FRAMES, float(framenum))
	
	if framenum> int(sys.argv[4]):
		break
	
cap.release()
out.release()
cv2.destroyAllWindows()
