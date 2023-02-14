COL_DURATION= 0;
COL_WIDTH= 0;
COL_HEIGHT= 0;
start= 0
stop=0 

start=traffic(2,1)
#for i=2:100
for i=2:size(traffic,1)
	if (stop== 0) # start of pass
		stop= traffic(i,1);
		COL_WIDTH=traffic(i, 8);
		COL_HEIGHT=traffic(i, 9);
		printf("%d,%d,%d,%d,%d\n", start, stop, COL_DURATION, COL_WIDTH, COL_HEIGHT)
		
	elseif (traffic(i,1) != stop+1)
		start= traffic(i,1);
		stop= 0;
	else # during pass
		COL_DURATION= stop-start;
		for j=[8, 12, 16]
			if (traffic(i,j) > COL_WIDTH) COL_WIDTH= traffic(i,j); endif
			if (traffic(i,j+1) > COL_HEIGHT) COL_HEIGHT= traffic(i,j+1); endif
		endfor
		stop= traffic(i,1);
		
	endif
endfor # traffic
