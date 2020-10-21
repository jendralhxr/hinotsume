# video0 is 82381 frames
# video1 is 82494 frames

COL_ID                =1;
COL_FRAMENUM    =2;
COL_START            =3;
COL_STOP         =4;
COL_DIRECTION     =5; # right is 0, left is 1
COL_WIDTH            =6;
COL_POSITION        =7;

load logsorted.txt

#calculate the width and center position of vehicle
for i=1:size(raw,1)
    raw(i, COL_WIDTH)= raw(i, COL_STOP) - raw(i, COL_START);
    raw(i, COL_POSITION)= (raw(i, COL_STOP) + raw(i, COL_START)) /2;
endfor

# remove entries from overlapping lane detection 
# repeat until clear
raw= sortrows(raw, [2 1]);
for i=1:size(raw,1)
 if    (raw(i,COL_FRAMENUM)== raw(i+1,COL_FRAMENUM)) &&    (raw(i,COL_START)     == raw(i+1,COL_START)) && (raw(i,COL_STOP)== raw(i+1,COL_STOP))
 raw(i:i+1,:)=[];
 endif
endfor

#remove the width of padding (in px)
raw(:,COL_WIDTH) -= 10; 

#--------- filter post-overlap passes
# for each segement with the same frame number, find the position of that particular ID 
# from previous segment (increment track back)
# discard the frame based 
# iterate in one increment

raw= sortrows(raw, [2 1]);

i=1;
while i<size(raw,1)
    if (raw(i, COL_FRAMENUM) == raw(i+1, COL_FRAMENUM)) && (raw(i, COL_ID) == raw(i+1, COL_ID))
        TEMP_FRAMENUM= raw(i, COL_FRAMENUM);
        TEMP_ID= raw(i, COL_ID);
        fin=1;
        
        while (raw(i, COL_FRAMENUM)==TEMP_FRAMENUM) && (raw(i, COL_ID)==TEMP_ID)
            #-----
            for j=1:20
                if (raw(i-j, COL_ID) == TEMP_ID) && (raw(i-j, COL_ID) < TEMP_FRAMENUM) # found the duplicate
                    printf("dup %d at %d-%d\n", raw(i, COL_ID), i, j);
                    
                    if (raw(i, COL_ID) < 100) && (raw(i, COL_POSITION) <= raw(i-j, COL_POSITION))
                        printf("dela %d %d/%d %d-%d\n", raw(i, COL_ID), raw(i, COL_POSITION), raw(i-j, COL_POSITION), i, j);
                        raw(i,:)= [];
                        fin= 0;
                        break; # from for20
                    elseif (raw(i, COL_ID) > 100) && (raw(i, COL_POSITION) >= raw(i-j, COL_POSITION))
                        printf("delb %d %d/%d %d-%d\n", raw(i, COL_ID), raw(i, COL_POSITION), raw(i-j, COL_POSITION), i, j);
                        raw(i,:)= [];
                        fin= 0;
                        break; # from for20
                    endif
                endif
            endfor
            #-----

            if fin==0
                break
            endif

            i++;
        endwhile
    else 
        i++;
    endif
endwhile
 
save logbersih.txt raw


#----- calculating traffic passes 
raw= sortrows(raw, [1 2]);
POS_JUMP= 240;

clear traffic;
start= 1;
n=1;
pos_max= 0;
pos_min= 1000;
for i=2:size(raw,1)
    if (raw(start,COL_ID) != raw(i,COL_ID)) || (raw(start,COL_DIRECTION) != raw(i,COL_DIRECTION)) ||    (( abs (raw(i,COL_FRAMENUM) - raw(i-1,COL_FRAMENUM))) > POS_JUMP )
        stop= i-1;
        
        traffic(n,1)= raw(start, COL_ID);
        traffic(n,2)= raw(start, COL_FRAMENUM);
        traffic(n,3)= raw(stop, COL_FRAMENUM) - raw(start, COL_FRAMENUM);
        traffic(n,4)= raw(start, COL_DIRECTION);
        traffic(n,5)= mean(raw(start:stop, COL_WIDTH));
        traffic(n,6)= raw(start, COL_POSITION);
        traffic(n,7)= pos_max;
        traffic(n,8)= pos_min;
        
        start=i;
        pos_max= 0;
        pos_min= 1000;
        
    n+=1;
    endif
    if ( raw(i, COL_POSITION) < pos_min)
    pos_min= raw(i, COL_POSITION);
    endif
    if ( raw(i, COL_POSITION) > pos_max)
    pos_max= raw(i, COL_POSITION);
    endif
endfor

# filter the wrong-direction output (opposite-end detection)
# repeat until clear
do
    size_prev= size(traffic,1);        
    for n=1:size(traffic,1)-1
        if traffic(n,3)<10
            traffic(n,:) = [];    
    endif
    endfor
    size_cur= size(traffic,1);
until (size_cur==size_prev)

save logsorted.txt raw
save trafficwidthcorrected.txt traffic
        
#---------

TIME_CLUSTER= 3 # mins

traffic(:, COL_FRAMENUM) /= 3600; # now in minutes
COL_DIRECTION=4;

#count per direction
clear sum_direction;
sum_direction(2, ceil(max(traffic(:,COL_FRAMENUM)) / TIME_CLUSTER))=1;
for i=1:size(traffic,1)
    if ( traffic(i, COL_DIRECTION) < 1)
            sum_direction(1, ceil(traffic(i,COL_FRAMENUM)/TIME_CLUSTER) ) += 1;
    else
            sum_direction(2, ceil(traffic(i,COL_FRAMENUM)/TIME_CLUSTER) ) += 1;
    endif
endfor

timestamp= 0:TIME_CLUSTER:max(traffic(:,COL_FRAMENUM));
plot(timestamp, sum_direction);
# sort from framenum/time of occurence
