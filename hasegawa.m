------- for displacement spectrogram

for i=1:6000
bar(i,:)=hino1v(i,:);
endfor

xlabel("Time [s]");
ylabel("Span");
zz=colorbar;
ylabel(zz,"POC displacement [mm]");
title(sprintf("marker%d, t= %d - %d min",markernum, minut*5, (minut+1)*5));

clear bar;
for minut=0:1:29
for i=1:6000
bar(i,:)=hino2x(6000*minut+i,:);
endfor # i

#t+=60;
pcolor(t,span,bar');
shading interp
# axis([0 3600 0 30])
#max(max(abs(hino1x)))
caxis([0 1]) # pick whatever appropriate
xlabel("Time [s]");
ylabel("POC points [span]");
set(gca, "linewidth", 2, "fontsize", 3)
#zz=colorbar;
#set(zz,'YTick', 0:0.1:1);
#set(zz,'fontsize',3);
#ylabel(zz,"POC Response [px]");
title(sprintf("Hino2: axial displacement t= %d - %d min",minut, (minut+1)));

filename=sprintf("hino2x-%02d.png",minut);
#print(filename);
print(filename, '-dpng', '-S1400,400');

endfor # minut


---------- for traffic

for minut=0:1:30

traffic=hino1traffic(6000*minut+1:6000*(minut+1), 2);

#t+=60;

plot(t,traffic)

xlabel("Time [s]");
ylabel("Moment [m00]");
set(gca, "linewidth", 2, "fontsize", 4)
title(sprintf("Traffic t= %d - %d min",minut, (minut+1)));

filename=sprintf("hino1traffic-%02d.png",minut);
#print(filename);
print(filename, '-dpng', '-S1400,400');

endfor # minut



---------- for temporal response

xlabel("Time [s]");
ylabel("POC displacement [px]");
title(sprintf("hino1, POC displacement of point 5"));


for point=1:57
plot(ts, hino1x(:,point));
xlabel("Time [s]");
ylabel("POC displacement [px]");
axis([0 1800])
title(sprintf("hino1, POC displacement (point %02d)", point));
set(gca, 'xtick', 0:60:1800);
set(gca, "linewidth", 2, "fontsize", 4)
filename=sprintf("hino1point-%02d.png",point);
print(filename, '-dpng', '-S1920,480');
endfor

for point=[1 2 3 4 5 13 21 29 37 45 53 54 55 56 57]
for minut=0:1:29
plot(t,hino1vert(6000*minut+1:6000*(minut+1),point),"linewidth",1);
hold on;
plot(t,hino2vert(6000*minut+1:6000*(minut+1),point),"linewidth",1)
hold off;
xlabel("Time [s]");
ylabel("POC displacement [px]");
set(gca, "linewidth", 2, "fontsize", 4)
title(sprintf("POC vertical displacement (point %02d, time %02d-%02d min)", point, minut, minut+1));
filename=sprintf("hino-point%02d-min%02d.png", point, minut);
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


#for point=1:57
for point=[1 11 21 31 41 51 61]
#plot(ts, hino1vert(:,point));
plot(ts, hino1x(:,point));
xlabel("Time [s]");
ylabel("POC displacement [px]");
axis([0 1800])
title(sprintf("hino1, POC displacement (point %02d)", point));
set(gca, 'xtick', 0:60:1800);
set(gca, "linewidth", 2, "fontsize", 4)
filename=sprintf("hino1point-%02d.png",point);
print(filename, '-dpng', '-S1920,480');
endfor

----------- FFT full duration

FFTWINDOW= 200
FFTSTEP= 20
# initialize hino1fft(point, t, FFTWINDOW)
timeframe= floor((size(hino1vert)(1)-FFTWINDOW)/FFTSTEP)-1; 

clear hino1fft
hino1fftx(FFTWINDOW/2, timeframe, size(hino1x)(2))=0; 
hino1ffty(FFTWINDOW/2, timeframe, size(hino1vert)(2))=0; 
hino2fftx(FFTWINDOW/2, timeframe, size(hino2x)(2))=0; 
hino2ffty(FFTWINDOW/2, timeframe, size(hino2vert)(2))=0; 

#calc the full FFT
#for point=[1 11 21 31 41 51 61]
for point=1:57
point
tp=1;
iter=1;
for iter=1:timeframe
#printf("%d %d\n",point, iter)
hino1fftx(:, iter, point)= abs(fft(hino1x(iter*FFTSTEP:iter*FFTSTEP+FFTWINDOW-1, point)))(1:FFTWINDOW/2) / (FFTWINDOW/2);
hino1ffty(:, iter, point)= abs(fft(hino1vert(iter*FFTSTEP:iter*FFTSTEP+FFTWINDOW-1, point)))(1:FFTWINDOW/2) / (FFTWINDOW/2);
hino2fftx(:, iter, point)= abs(fft(hino2x(iter*FFTSTEP:iter*FFTSTEP+FFTWINDOW-1, point)))(1:FFTWINDOW/2) / (FFTWINDOW/2);
hino2ffty(:, iter, point)= abs(fft(hino2vert(iter*FFTSTEP:iter*FFTSTEP+FFTWINDOW-1, point)))(1:FFTWINDOW/2) / (FFTWINDOW/2);
tp+= FFTSTEP;
iter++;
endfor # timeframe
endfor # point

CUTOFF_DISP= 50.0; # Hz

# draw the spec
#for point=1:57
for point=[1 11 21 31 41 51 61]
t_fft = 0:size(hino1fft)(2)-1;
t_fft*= FFTSTEP/SAMPLINGRATE;
freq=0:SAMPLINGRATE/FFTWINDOW:(CUTOFF_DISP-0.001);
#temp= squeeze(hino1fft( 1:size(freq)(2), 1:size(t_fft)(2), point));
temp= squeeze(hino1fftx( 1:size(freq)(2), 1:size(t_fft)(2), point));
pcolor(t_fft,freq,temp);
shading interp
xlabel("Time [s]");
ylabel("FFT Response [Hz]");
set(gca, 'ytick', 0:10:CUTOFF_DISP);
set(gca, 'xtick', 0:60:1800);
zz=colorbar;
ylabel(zz,"POC displacement [px]");
caxis([0 0.4])
#max(max(max(abs(hino1fftx))))
#set(zz,'YTick', 0:0.1:1.0);
set(zz,'YTick', 0:0.1:0.4);
set(zz,'fontsize',4);
set(gca, "linewidth", 2, "fontsize", 4);
set(gca,'TickLength',[0 0]);
axis("tight");
title(sprintf("hino1, Horizontal frequency response (point %02d)", point));
filename=sprintf("hino1fft50hz-%02d.png",point)
print(filename, '-dpng', '-S2048,480');
endfor # point

----------- FFT by minute
clear temp spec;
freq=0:SAMPLINGRATE/FFTWINDOW:10-0.001;
tf= 0:60*SAMPLINGRATE/FFTSTEP-1;
tf*= FFTSTEP/SAMPLINGRATE;

#for point=1:57
for point=[1 2 3 4 5 13 21 29 37 45 53 54 55 56 57]
for minut=0:29 

temp= squeeze(hino1fftx( 1:size(freq)(2), minut*300+1:(minut+1)*300, point));
pcolor(tf,freq,temp)
shading interp
xlabel("Time [s]");
ylabel("FFT Response [Hz]");
axis([0 60 0 5]);
set(gca, 'ytick', 0:5:50);
set(gca, 'xtick', 0:5:60);
zz=colorbar;
ylabel(zz,"POC displacement [px]");
set(gca, "linewidth", 2, "fontsize", 4);
set(gca,'TickLength',[0 0]);
#caxis([0 0.4])
#set(zz,'fontsize',4);
#set(zz,'YTick', 0:0.1:0.4);
axis("tight");
title(sprintf("HINO1, Horizontal frequency response (point %02d, time %02d-%02d min)", point, minut, minut+1));
filename=sprintf("hino1fftx-p%02d-m%02d.png",point, minut)
print(filename, '-dpng', '-S1400,400');

temp= squeeze(hino2fftx( 1:size(freq)(2), minut*300+1:(minut+1)*300, point));
pcolor(tf,freq,temp)
shading interp
xlabel("Time [s]");
ylabel("FFT Response [Hz]");
axis([0 60 0 5]);
set(gca, 'ytick', 0:5:50);
set(gca, 'xtick', 0:5:60);
zz=colorbar;
ylabel(zz,"POC displacement [px]");
set(gca, "linewidth", 2, "fontsize", 4);
set(gca,'TickLength',[0 0]);
#caxis([0 0.4])
#set(zz,'fontsize',4);
#set(zz,'YTick', 0:0.1:0.4);
axis("tight");
title(sprintf("HINO2, Horizontal frequency response (point %02d, time %02d-%02d min)", point, minut, minut+1));
filename=sprintf("hino2fftx-p%02d-m%02d.png",point, minut)
print(filename, '-dpng', '-S1400,400');

endfor # minut
endfor # point

%----------------

for point=[1 2 3 4 5 13 21 29 37 45 53 54 55 56 57]
for minut=0:29 

temp= squeeze(hino1ffty( 1:size(freq)(2), minut*300+1:(minut+1)*300, point));
pcolor(tf,freq,temp)
shading interp
xlabel("Time [s]");
ylabel("FFT Response [Hz]");
axis([0 60 0 5]);
set(gca, 'ytick', 0:5:50);
set(gca, 'xtick', 0:5:60);
zz=colorbar;
ylabel(zz,"POC displacement [px]");
set(gca, "linewidth", 2, "fontsize", 4);
set(gca,'TickLength',[0 0]);
#caxis([0 0.4])
#set(zz,'fontsize',4);
#set(zz,'YTick', 0:0.1:0.4);
axis("tight");
title(sprintf("HINO1, Vertical frequency response (point %02d, time %02d-%02d min)", point, minut, minut+1));
filename=sprintf("hino1ffty-p%02d-m%02d.png",point, minut)
print(filename, '-dpng', '-S1400,400');

temp= squeeze(hino2ffty( 1:size(freq)(2), minut*300+1:(minut+1)*300, point));
pcolor(tf,freq,temp)
shading interp
xlabel("Time [s]");
ylabel("FFT Response [Hz]");
axis([0 60 0 5]);
set(gca, 'ytick', 0:5:50);
set(gca, 'xtick', 0:5:60);
zz=colorbar;
ylabel(zz,"POC displacement [px]");
set(gca, "linewidth", 2, "fontsize", 4);
set(gca,'TickLength',[0 0]);
#caxis([0 0.4])
#set(zz,'fontsize',4);
#set(zz,'YTick', 0:0.1:0.4);
axis("tight");
title(sprintf("HINO2, Vertical frequency response (point %02d, time %02d-%02d min)", point, minut, minut+1));
filename=sprintf("hino2ffty-p%02d-m%02d.png",point, minut)
print(filename, '-dpng', '-S1400,400');

endfor # minut
endfor # point
