load("displacement.csv");

window_width=60; # 1 s
sample_width= 360; # 6 s
jump=2;  # advances by .1 s
duration_width= 3600;

for minut=0:1:12

for markernum=1:7
clear freqbar; 
freqbar(duration_width/jump, sample_width/2)=0;

step= 1;
for i=1:jump:duration_width
	window_sample= displacement(i + minut*duration_width: i+window_width-1 + minut*duration_width, markernum);
	window_sample= window_sample .* hamming(window_width);
	sample=0; sample(sample_width)=0;
	sample(1:window_width)= window_sample;
	freqbar(step,:)=(abs(fft(sample))/sample_width*2)(:,1:sample_width/2); # normalize by sample count/2 horizontal, only to 30 Hz vertically
	step++;
endfor

t=0: jump/60 : jump/60*(step-2);
#t+=1080;
freq=0:30/size(freqbar,2):29.9999;
pcolor(t,freq,freqbar');
shading interp
# axis([0 3600 0 30])
caxis([0 0.3]) # pick whatever appropriate
	
xlabel("Time [s]");
ylabel("Frequency [Hz]");
#zz=colorbar;
#ylabel(zz,"Frequency Response [mm]");
#title(sprintf("marker%d, t= %d - %d min",markernum, minut*5, (minut+1)*5));

filename=sprintf("t%02dm%02d.png",minut,markernum);
#print(filename);
print(filename, '-dpng', '-S1200,400');
endfor
endfor
