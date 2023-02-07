# scratchpad for hasegawa

i=1
for a= 2:5:315
hase9vert(:,i)=hase9(:,a);
i++;
endfor

hase9v=abs(hase9vert);

%---------

i=1
for a= 1:5:314
hase9x(:,i)=hase9(:,a);
i++;
endfor



hase11v= abs(hase11vert);

------- for displacement spectrogram

for i=1:6000
bar(i,:)=hase9v(i,:);
endfor

xlabel("Time [s]");
ylabel("Span");
zz=colorbar;
ylabel(zz,"POC displacement [mm]");
title(sprintf("marker%d, t= %d - %d min",markernum, minut*5, (minut+1)*5));


for minut=0:1:29

for i=1:6000
bar(i,:)=hase9x(6000*minut+i,:);
endfor
#t+=60;
pcolor(t,span,bar');
shading interp
# axis([0 3600 0 30])
#max(max(abs(hase9x)))
caxis([0 .8]) # pick whatever appropriate
xlabel("Time [s]");
ylabel("POC points [span]");
set(gca, "linewidth", 2, "fontsize", 4)
zz=colorbar;
ylabel(zz,"POC Response [px]");
title(sprintf("Axial displacement t= %d - %d min",minut, (minut+1)));

filename=sprintf("hase9axial-%02d.png",minut);
#print(filename);
print(filename, '-dpng', '-S1400,400');

endfor # minut


---------- for traffic

for minut=0:1:30

traffic=hase9traffic(6000*minut+1:6000*(minut+1), 2);

#t+=60;

plot(t,traffic)

xlabel("Time [s]");
ylabel("Moment [m00]");
set(gca, "linewidth", 2, "fontsize", 4)
title(sprintf("Traffic t= %d - %d min",minut, (minut+1)));

filename=sprintf("hase9traffic-%02d.png",minut);
#print(filename);
print(filename, '-dpng', '-S1400,400');

endfor # minut



---------- for temporal response

xlabel("Time [s]");
ylabel("POC displacement [px]");
title(sprintf("HASE9, POC displacement of point 5"));


for point=1:63
plot(ts, hase9vert(:,point));
xlabel("Time [s]");
ylabel("POC displacement [px]");
axis([0 1800])
title(sprintf("HASE9, POC displacement (point %02d)", point));
set(gca, 'xtick', 0:60:1800);
set(gca, "linewidth", 2, "fontsize", 4)
filename=sprintf("hase9point-%02d.png",point);
print(filename, '-dpng', '-S1920,480');
endfor

for point=[1 11 21 31 41 51 61]
for minut=0:1:29
plot(t,hase9x(6000*minut+1:6000*(minut+1),point))
xlabel("Time [s]");
ylabel("POC displacement [px]");
set(gca, "linewidth", 2, "fontsize", 4)
title(sprintf("HASE9, POC horizontal displacement (point %02d, time %02d-%02d min)", point, minut, minut+1));
filename=sprintf("hase9x-point%02d-min%02d.png", point, minut);
print(filename)
print(filename, '-dpng', '-S1400,400');
endfor # minut
endfor # point

------- for frequency response

SAMPLINGRATE= 100

FFTWINDOW= 200 # 2 secs fft window
a=2*sin(2*pi()*t);
af4=abs(fft(a(1:FFTWINDOW)));
fr4=0:100/FFTWINDOW:SAMPLINGRATE-0.0001;
plot(fr4',af4/(FFTWINDOW/2));


#for point=1:63
for point=[1 11 21 31 41 51 61]
#plot(ts, hase9vert(:,point));
plot(ts, hase9x(:,point));
xlabel("Time [s]");
ylabel("POC displacement [px]");
axis([0 1800])
title(sprintf("HASE9, POC displacement (point %02d)", point));
set(gca, 'xtick', 0:60:1800);
set(gca, "linewidth", 2, "fontsize", 4)
filename=sprintf("hase9point-%02d.png",point);
print(filename, '-dpng', '-S1920,480');
endfor

----------- FFT full duration

FFTWINDOW= 200
FFTSTEP= 20
# initialize hase9fft(point, t, FFTWINDOW)
timeframe= floor((size(hase9vert)(1)-FFTWINDOW)/FFTSTEP)-1; 

clear hase9fft
hase9fft(FFTWINDOW/2, timeframe, size(hase9vert)(2))=0; 
hase9fftx(FFTWINDOW/2, timeframe, size(hase9vert)(2))=0; 

#calc the full FFT
#for point=[1 11 21 31 41 51 61]
for point=1:63
point
tp=1;
iter=1;
for iter=1:timeframe
#printf("%d %d\n",point, iter)
#hase9fft(:, iter, point)= abs(fft(hase9vert(iter*FFTSTEP:iter*FFTSTEP+FFTWINDOW-1, point)))(1:FFTWINDOW/2) / (FFTWINDOW/2);
hase9fftx(:, iter, point)= abs(fft(hase9x(iter*FFTSTEP:iter*FFTSTEP+FFTWINDOW-1, point)))(1:FFTWINDOW/2) / (FFTWINDOW/2);
tp+= FFTSTEP;
iter++;
endfor # timeframe
endfor # point

CUTOFF_DISP= 50.0; # Hz

# draw the spec
#for point=1:63
for point=[1 11 21 31 41 51 61]
t_fft = 0:size(hase9fft)(2)-1;
t_fft*= FFTSTEP/SAMPLINGRATE;
freq=0:SAMPLINGRATE/FFTWINDOW:(CUTOFF_DISP-0.001);
#temp= squeeze(hase9fft( 1:size(freq)(2), 1:size(t_fft)(2), point));
temp= squeeze(hase9fftx( 1:size(freq)(2), 1:size(t_fft)(2), point));
pcolor(t_fft,freq,temp);
shading interp
xlabel("Time [s]");
ylabel("FFT Response [Hz]");
set(gca, 'ytick', 0:10:CUTOFF_DISP);
set(gca, 'xtick', 0:60:1800);
zz=colorbar;
ylabel(zz,"POC displacement [px]");
caxis([0 0.4])
#max(max(max(abs(hase9fftx))))
#set(zz,'YTick', 0:0.1:1.0);
set(zz,'YTick', 0:0.1:0.4);
set(zz,'fontsize',4);
set(gca, "linewidth", 2, "fontsize", 4);
set(gca,'TickLength',[0 0]);
axis("tight");
title(sprintf("HASE9, Horizontal frequency response (point %02d)", point));
filename=sprintf("hase9fft50hz-%02d.png",point)
print(filename, '-dpng', '-S2048,480');
endfor # point

----------- FFT by minute
clear temp spec;
freq=0:SAMPLINGRATE/FFTWINDOW:5.0;
tf= 0:60*SAMPLINGRATE/FFTSTEP-1;
tf*= FFTSTEP/SAMPLINGRATE;

for point=1:63
for minut=0:29 
#temp= squeeze(hase9fft( 1:size(freq)(2), minut*300+1:(minut+1)*300, point));
temp= squeeze(hase9fftx( 1:size(freq)(2), minut*300+1:(minut+1)*300, point));
pcolor(tf,freq,temp)
shading interp
xlabel("Time [s]");
ylabel("FFT Response [Hz]");
axis([0 60 0 5]);
set(gca, 'ytick', 0:1:5);
set(gca, 'xtick', 0:5:60);
#zz=colorbar;
#ylabel(zz,"POC displacement [px]");
caxis([0 0.4])
#set(zz,'YTick', 0:0.1:0.4);
#set(zz,'fontsize',4);
set(gca, "linewidth", 2, "fontsize", 4);
set(gca,'TickLength',[0 0]);
axis("tight");
title(sprintf("HASE9, Horizontal frequency response (point %02d, time %02d-%02d min)", point, minut, minut+1));
filename=sprintf("hase9fftx-p%02d-m%02d.png",point, minut)
print(filename, '-dpng', '-S1400,400');
endfor # minut
endfor # point
