STF=36000;

threshold=2.5; # mm
displacement_thre(size(displacement,1), 7)=0; 
#for j=1:size(displacement,1)
for j=STF:size(displacement,1)
 for i=2:8
  temp= abs(displacement(j,i));
  if (temp<threshold)
   displacement_thre(j,i-1)= 0;
  else 
   displacement_thre(j,i-1)= abs(displacement(j,i));
  endif
 endfor
endfor
plot(displacement_thre);



