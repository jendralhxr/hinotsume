traffic=dlmread("traffic.txt","\t");
displacement=dlmread("displacement.txt","\t");

clear('pass_length');
clear('pass_speed');
pass_length(size(displacement,1),2)=0;
pass_speed(size(displacement,1),2)=0;

fstart= 2;
fend= 3;
direction= 4;
length= 5;
velocity= 6;
cur= 1;

j = 0;

for i=1:size(traffic,1)
cur= traffic(i, fstart);
  for j=1:traffic(i,fend)
    if ( traffic(i,direction) ==1 )
      pass_length(cur+j-1, 1) = traffic(i, length);
	  pass_speed(cur+j-1, 1) = traffic(i, velocity);
    else
      pass_length(cur+j-1, 2) = -traffic(i, length);
	  pass_speed(cur+j-1, 2) = -traffic(i, velocity);
	  
    endif
  endfor
endfor


displacement=dlmread("mangap.txt","\t");
# in sec
offset=0;
pstart=420*60;
pstop =430*60;
plot(time(pstart:pstop), pass_length(pstart:pstop,:));

subplot(2,1,1)
plot(time(pstart:pstop), pass_length(pstart:pstop,:));
ylabel("vehicle length (m)")
subplot(2,1,2)
plot(time(pstart:pstop), displacement(pstart+offset:pstop+offset,:));
ylabel("vertical displacement (mm)")
xlabel("time (s)");
#---------

sample=dlmread("kucel.txt","\t");
for i=1:size(sample,1)
  upsample(2*i-1,:)= sample(i,:); 
  upsample(2*i,:)  = (sample(i,:) + sample(i+1,:)) /2;
endfor
upsample(size(upsample,1)+1,:)= mean(sample(size(sample,1)-3:size(sample,1),:)) ;
save "kucel-ups.txt" "upsample";