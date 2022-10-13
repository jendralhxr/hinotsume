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
startx= 0              
stopx= 804
starty=0
stopy= 120

# image section to be processed, within cropped area
cropped_x_start= 0
cropped_x_stop= 800 # shorter window makes life easier
cropped_y_start= 0
cropped_y_stop= 120

thickness_min_horizontal= 30 # maximum width of bondo
thickness_min_vertical= 10 # maximum width of bondo
block_width= 100 # minimum width of vehicle
update_interval= 100 # frames

digit=8;

gate_left=  cropped_x_start+block_width-thickness_min_horizontal # position of ID-assignment gate
gate_right= cropped_x_stop-block_width+thickness_min_horizontal # position of ID-assignment gate

cap = cv2.VideoCapture(sys.argv[1])
ref= cv2.imread(sys.argv[2])
vsize = (int((stopx-startx)/4), int((stopy-starty)/4))

temp= ref
image_prev= ref
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
	
	#remove thin horizontal line (such as cables) ## PERHAPS VERTICAL TOO
	for i in range(cropped_x_start, cropped_x_stop-1):
		blobstart= 0
		blobend= 0
		for j in range(cropped_y_stop-1, cropped_y_start+1, -1):
			if image_cue.item(j,i,1) > THRESHOLD_VAL: # start of object
				if (blobstart== 0):
					blobstart= j
			if image_cue.item(j,i,1) < THRESHOLD_VAL: # end of object
				if (blobstart!= 0):
					blobend= j
			if (blobend-blobstart) < thickness_min_vertical:
				for j in range(blobend, blobstart, -1):
					image_cue.itemset((j,i,1) , 0) # remove all traces, perhaps green only would suffice
					image_cue.itemset((j,i,0) , 0) # blue too
					image_cue.itemset((j,i,2) , 0) # red too
				blobstart= 0
				blobend= 0
	
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
	
	#dateTimeObj = datetime.now()
	#timestampStr = dateTimeObj.strftime("%H:%M:%S.%f")
	#print('scan: ', timestampStr)
	
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
	
	#dateTimeObj = datetime.now()
	#timestampStr = dateTimeObj.strftime("%H:%M:%S.%f")
	#print('bondo: ', timestampStr)
	
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
					image_cue.itemset((1,n,2) , 0) # red
			
			# apply identifier
			elif (block_start!= 0) and (block_end != 0):
				vehicle_detect= vehicle_detect +1
				# from right: red: 1 to 99
				# from left: 101 to 200
				# print("{} start{} stop{}".format(framenum, block_start, block_end))
				
				#from left gate, line3
				if (block_start < gate_left) and (block_end > gate_left):
					vehicle_id=  image_prev.item(3, int((block_start + block_end)/2) ,2)
					if (vehicle_id == 0) :
						vehicle_id= random.randint(1, 99)
						vehicle_detect= vehicle_detect +1
						#if (image_prev.item(3, int((block_start + block_end)/2) ,2] == 0):
						#print("{} {} {} {} leftnew".format(vehicle_id, framenum, block_start, block_end))
					for n in range(block_start, block_end):
						image_cue.itemset((3,n,2) , vehicle_id)
				
				# from right gate, line5
				elif (block_start < gate_right) and (block_end > gate_right):
					vehicle_id= image_prev.item(5, int((block_start + block_end)/2) ,2)
					if (vehicle_id == 0) :
						vehicle_id= random.randint(101, 199)
						vehicle_detect= vehicle_detect +1
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
						vehicle_detect= vehicle_detect +1
						if (vehicle_id != 0):
							break
					if ( vehicle_id != 0) :
						# find the height
						height_start= 99999999 
						height_end= 0
						for i in range(block_start, block_end-1):
							for j in range(cropped_y_stop-2, cropped_y_start+6, -1):
								if image_cue.item(j,i,1) != 0:
									if (j < height_start):
										height_start= j
									if (j > height_end):
										height_end= j
						start_point = (block_start, height_start)
						end_point = (block_end, height_end)	
						label_point= (block_start+10, height_end-20)
						cv2.rectangle(image_display, start_point, end_point, (255,36,12), 1) # blue
						cv2.putText(image_display, str(vehicle_id), label_point, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,36, 12), 1)
						print("{} {} {} {} {} {} 1".format(vehicle_id, framenum, block_start, block_end, height_start, height_end)) # left is '1'
						for n in range(block_start, block_end):
							image_cue.itemset((3,n,2),  vehicle_id)
					# right to left
					for n in range(block_end, block_start, -2):
						vehicle_id = image_prev.item(5, n, 2)
						vehicle_detect= vehicle_detect +1
						if (vehicle_id != 0):
							break
					if ( vehicle_id != 0) :
						# find the height
						height_start= 99999999 
						height_end= 0
						for i in range(block_start, block_end-1):
							for j in range(cropped_y_stop-2, cropped_y_start+6, -1):
								if image_cue.item(j,i,1) != 0:
									if (j < height_start):
										height_start= j
									if (j > height_end):
										height_end= j
						start_point = (block_start, height_start) 
						end_point = (block_end, height_end) 
						label_point= (block_start+10, height_start+20)
						cv2.rectangle(image_display, start_point, end_point, (12,36,255), 1) # red
						cv2.putText(image_display, str(vehicle_id), label_point, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (12,36, 255), 1)
						print("{} {} {} {} {} {} 0".format(vehicle_id, framenum, block_start, block_end, height_start, height_end)) # right is '0'
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
#		image_display.itemset((j,gate_left,1) , 255) # green
#		image_display.itemset((j,gate_right,1) , 255) # green
		image_cue.itemset((j,gate_left,1) , 255) # green
		image_cue.itemset((j,gate_right,1) , 255) # green
	
	# update the reference background
	update= update+FRAME_STEP
	#print("{}/{} v{}".format(update, update_interval, vehicle_detect))
	if ((vehicle_detect==0) and (update>update_interval)):
		#print("{}/{} f{}".format(update, update_interval, framenum))
		update = 0
		ref= frame
	
	cv2.imshow('display',image_display)
	cv2.imshow('cue',image_cue)
	#image_display_resized=cv2.resize(image_display, vsize, interpolation= cv2.INTER_AREA)
	#image_cue_resized = cv2.resize(image_cue, vsize, interpolation = cv2.INTER_AREA)
	#cv2.imshow('display',image_display_resized)
	#cv2.imshow('cue',image_cue_resized)
	   
	dateTimeObj = datetime.now()
	timestampStr = dateTimeObj.strftime("%H:%M:%S.%f")
	
	k = cv2.waitKey(1) & 0xFF
	if k== ord("c"):
		print("saving: "+str(framenum).zfill(digit)+'.png')
		cv2.imwrite(str(framenum).zfill(digit)+'.png', frame)
	if k== ord("r"):
		print("reference: "+str(framenum).zfill(digit)+'.png')
		cv2.imwrite(str(framenum).zfill(digit)+'.png', frame)
		ref= frame
	if k== 27: # esc
		break
	
	# fix the dangling reference image
	#print(str(cv2.sumElems(image_cue)[1]))
	if (cv2.sumElems(ref)[1] > 64000.0):
		ref= frame
	
	out.write(image_display)
	out2.write(image_cue)
	#out.write(image_display_resized)
	#out2.write(image_cue_resized)
	
	#print('time: ', timestampStr, "framenum: ", str(framenum));
	framenum += FRAME_STEP
	cap.set(cv2.CAP_PROP_POS_FRAMES, float(framenum))
	
	if framenum> int(sys.argv[4]):
		break
	
cap.release()
out.release()
cv2.destroyAllWindows()
