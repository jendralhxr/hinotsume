clear('pass_length');
clear('pass_speed');
pass_length_east(360000,2)=0;
pass_speed_east(360000,1),2)=0;

for i=1:size(trafficeast,1)
cur= trafficeast(i, fstart);
  for j=1:trafficeast(i,fend)
    if ( trafficeast(i,direction) ==1 )
      pass_length_east(cur+j-1, 1) = trafficeast(i, length);
	  #pass_speed_east(cur+j-1, 1) = trafficeast(i, velocity);
    else
      pass_length_east(cur+j-1, 2) = -trafficeast(i, length);
	  #pass_speed_east(cur+j-1, 2) = -trafficeast(i, velocity);
    endif
  endfor
endfor


---------

west2= csvread("west.csv");
east2= csvread("east.csv");


framenum=0:359999;
temp=(framenum/200)';
tempclean= temp;

temp= tempclean;
temp(360000, 5) =0;

for i=1:size(west2,1)
	framenum= west2(i, 1)
	temp(framenum, 2)= west2(i, 2); # left car speed [kph, westward]
	temp(framenum, 3)= west2(i, 3); # left car length [m, westward]
	temp(framenum, 4)= west2(i, 4); # right car speed [kphm, westward]
	temp(framenum, 5)= west2(i, 5); # right car length [m, westward]
endfor
westt=temp;
csvwrite("west2.csv", temp);


--------

the fan graph

# speed
plot( eastt(:,1), eastt(:,2) );
hold on
plot( eastt(:,1), eastt(:,4) );
hold off
set(gca, 'xtick', 0:60:1800);
set(gca, 'ytick', -100:10:100);
set(gca, "linewidth", 2, "fontsize", 4)
axis("tight");
xlabel("Time [s]");
ylabel("Passing vehicle speed [kph]");
title ("Hinotsume Bridge, east span");
filename=sprintf("hinotsume-east-speed.png")
print(filename, '-dpng', '-S2048,480')
close

# length
plot( eastt(:,1), eastt(:,3) );
hold on
plot( eastt(:,1), eastt(:,5) );
hold off
set(gca, 'xtick', 0:60:1800);
set(gca, 'ytick', -24:2:24);
set(gca, "linewidth", 2, "fontsize", 4)
axis("tight");
xlabel("Time [s]");
ylabel("Passing vehicle length [m]");
title ("Hinotsume Bridge, east span");
filename=sprintf("hinotsume-east-length.png")
print(filename, '-dpng', '-S2048,480')
close

# length histogram
clear eastlength;
eastlength= east2(:,3) + east2(:,5);
hist( abs(eastlength), 8)
set(gca, "linewidth", 2, "fontsize", 4)
#axis("tight");
xlabel("Vehicle length [m]");
ylabel("Count [n]");
title ("Hinotsume Bridge, east span");
filename=sprintf("hinotsume-east-lengthhist.png")
print(filename, '-dpng', '-r300')
close

