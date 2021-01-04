STF=36000;

threshold=3; # mm
displacement_thre(size(displacement,1), 7)=0; 
#for j=1:size(displacement,1)
for j=STF:size(displacement,1)
 for i=2:8
  temp= displacement(j,i);
  if (temp<threshold) && (temp>-threshold)
   displacement_thre(j,i-1)= 0;
  else 
   displacement_thre(j,i-1)= abs(displacement(j,i));
   #displacement_thre(j,i-1)= abs(displacement(j,i));
  endif
 endfor
endfor
plot(displacement_thre(:,4));

#########

did not mention how to compute relative displacement. 
You should describe how to compute this in detail as algorithm description. 
Some of setting is conducted by my python program. 

Additionally, you had better show all the photos when large displacements (e.g. >2mm). 
Several left lane cars are misdetected as large displacement, but you should explain it with this. 

did not indicate this paper is extension of your previous JRM paper. 
Tandem-marker based motion capture realize very simple bridge observation.