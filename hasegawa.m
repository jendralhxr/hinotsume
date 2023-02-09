
i=1
for a= 1:5:315
hase11x(:,i)=hase11(:,a);
hase11y(:,i)=hase11(:,a+1);
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


for minut=0:1:13
minut
for i=1:6000
#bar(i,:)=hase11x(6000*minut+i,:);
bar(i,:)=hase11y(6000*minut+i,:);
endfor
#t+=60;
pcolor(t,span,bar');
shading interp
#axis([0 3600 0 30])
#max(max(abs(hase9x)))
caxis([-0.4 .4]) # pick whatever appropriate
xlabel("Time [s]");
ylabel("POC points [span]");
set(gca, "linewidth", 2, "fontsize", 4)
#zz=colorbar;
#ylabel(zz,"POC Response [px]");
#set(zz,'fontsize',4);
#set(zz,'YTick', -0.4:0.1:0.4);
#title(sprintf("HASE11 horizontal displacement t= %d - %d min",minut, (minut+1)));
#filename=sprintf("hase9x-%02d.png",minut);
title(sprintf("HASE11 vertical displacement t= %d - %d min",minut, (minut+1)));
filename=sprintf("hase9y-%02d.png",minut);
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

for point=[1 7 13 19 20 21 22 23 24 25 26 34 42 50 60]
for minut=0:1:13
#plot(t,hase11x(6000*minut+1:6000*(minut+1),point))
plot(t,hase11y(6000*minut+1:6000*(minut+1),point))
xlabel("Time [s]");
set(gca, "linewidth", 2, "fontsize", 4)
#ylabel("Horizontal POC displacement [px]");
#title(sprintf("HASE11, POC horizontal displacement (point %02d, time %02d-%02d min)", point, minut, minut+1));
#filename=sprintf("hase11x-point%02d-min%02d.png", point, minut);
ylabel("Vertical POC displacement [px]");
title(sprintf("HASE11, POC vertical displacement (point %02d, time %02d-%02d min)", point, minut, minut+1));
filename=sprintf("hase11y-point%02d-min%02d.png", point, minut);
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

---------- FFT full duration

FFTWINDOW= 200
FFTSTEP= 20
# initialize hase9fft(point, t, FFTWINDOW)
timeframe= floor((size(hase11x)(1)-FFTWINDOW)/FFTSTEP)-1; 

clear hase9fft
hase11fftx(FFTWINDOW/2, timeframe, size(hase11x)(2))=0; 
hase11ffty(FFTWINDOW/2, timeframe, size(hase11y)(2))=0; 

#calc the full FFT
#for point=[1 11 21 31 41 51 61]
for point=1:62
point
tp=1;
iter=1;
for iter=1:timeframe
#printf("%d %d\n",point, iter)
hase11fftx(:, iter, point)= abs(fft(hase11x(iter*FFTSTEP:iter*FFTSTEP+FFTWINDOW-1, point)))(1:FFTWINDOW/2) / (FFTWINDOW/2);
hase11ffty(:, iter, point)= abs(fft(hase11y(iter*FFTSTEP:iter*FFTSTEP+FFTWINDOW-1, point)))(1:FFTWINDOW/2) / (FFTWINDOW/2);
tp+= FFTSTEP;
iter++;
endfor # timeframe
endfor # point


# draw the spec
#for point=1:63
#for point=[1 11 21 31 41 51 61]

CUTOFF_DISP= 10; # Hz
for point=[1 7 13 19 20 21 22 23 24 25 26 34 42 50 60]
t_fft = 0:size(hase11fftx)(2)-1;
t_fft*= FFTSTEP/SAMPLINGRATE;
freq=0:SAMPLINGRATE/FFTWINDOW:(CUTOFF_DISP-0.001);
#temp= squeeze(hase11fftx( 1:size(freq)(2), 1:size(t_fft)(2), point));
temp= squeeze(hase11ffty( 1:size(freq)(2), 1:size(t_fft)(2), point));
pcolor(t_fft,freq,temp);
shading interp
xlabel("Time [s]");
ylabel("FFT Response [Hz]");
set(gca, 'ytick', 0:10:CUTOFF_DISP);
set(gca, 'xtick', 0:60:1800);
caxis([0 0.4])
set(gca, "linewidth", 2, "fontsize", 4);
set(gca,'TickLength',[0 0]);
#max(max(max(abs(hase9fftx))))
#zz=colorbar;
#ylabel(zz,"POC displacement [px]");
#set(zz,'YTick', 0:0.1:0.4);
#set(zz,'fontsize',4);
axis("tight");
#title(sprintf("HASE11, Horizontal frequency response (point %02d)", point));
#filename=sprintf("hase11fft%0dx-%02d.png", CUTOFF_DISP, point)
title(sprintf("HASE11, Vertical frequency response (point %02d)", point));
filename=sprintf("hase11fft%0dy-%02d.png", CUTOFF_DISP, point)
print(filename, '-dpng', '-S2048,480')
endfor # point

----------- FFT by minute
clear temp spec;
freq=0:SAMPLINGRATE/FFTWINDOW:5.0;
tf= 0:60*SAMPLINGRATE/FFTSTEP-1;
tf*= FFTSTEP/SAMPLINGRATE;

#for point=1:13
for point=[1 7 13 19 20 21 22 23 24 25 26 34 42 50 60 61]
for minut=0:13
temp= squeeze(hase11fftx( 1:size(freq)(2), minut*300+1:(minut+1)*300, point));
#temp= squeeze(hase11ffty( 1:size(freq)(2), minut*300+1:(minut+1)*300, point));
pcolor(tf,freq,temp)
shading interp
xlabel("Time [s]");
ylabel("FFT Response [Hz]");
axis([0 60 0 5]);
set(gca, 'ytick', 0:1:5);
set(gca, 'xtick', 0:5:60);
zz=colorbar;
ylabel(zz,"POC displacement [px]");
caxis([0 0.4])
#set(zz,'YTick', 0:0.1:0.4);
#set(zz,'fontsize',4);
set(gca, "linewidth", 2, "fontsize", 4);
set(gca,'TickLength',[0 0]);
axis("tight");
title(sprintf("HASE11, Horizontal frequency response (point %02d, time %02d-%02d min)", point, minut, minut+1));
filename=sprintf("hase11fftx-p%02d-m%02d.png",point, minut)
#title(sprintf("HASE11, Vertical frequency response (point %02d, time %02d-%02d min)", point, minut, minut+1));
#filename=sprintf("hase11ffty-p%02d-m%02d.png",point, minut)
print(filename, '-dpng', '-S1400,400');
endfor # minut
endfor # point
