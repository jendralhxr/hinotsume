
import pandas as pd
east_traffic = pd.read_csv("east.csv").values
west_traffic = pd.read_csv("west.csv").values
east_pass= pd.read_csv("east2.csv").values
west_pass= pd.read_csv("west2.csv").values
east_length= pd.read_csv("el.csv").values
west_length= pd.read_csv("wl.csv").values

wl0= pd.read_csv("wl0.txt").values
wl1= pd.read_csv("wl1.txt").values
ws0= pd.read_csv("ws0.txt").values
ws1= pd.read_csv("ws1.txt").values
el0= pd.read_csv("el0.txt").values
el1= pd.read_csv("el1.txt").values
es0= pd.read_csv("es0.txt").values
es1= pd.read_csv("es1.txt").values

tt=np.linspace(0, 1800, 360000)

----



ts= 0
te= 1800


total_txt_out = 'Hinotsume Bridge, east side: 2021-12-02_12.30.54';

# Speeds of Detected Vehicles
fig = plt.figure(figsize=(12,4), dpi=300)
plt.xlim(0, 1800)
plt.plot(east_pass[:,0], east_pass[:,1], linewidth=1,label='left-going');
plt.plot(east_pass[:,0], east_pass[:,3], linewidth=1,label='right-going');
plt.xlabel('Time [s]')
plt.ylabel('Speed [km/h]')
plt.legend(fontsize=8,loc='upper right' );
plt.title('Speeds of Detected Vehicles',loc='right',fontsize=14)
fig.text(0.13, 0.9, total_txt_out);
#plt.show();
plt.savefig("east-speed.png")
plt.close()

# Speeds of Detected Vehicles
fig = plt.figure(figsize=(12,4), dpi=300)
plt.xlim(0, 1800)
plt.plot(east_pass[:,0], east_pass[:,2], linewidth=1,label='left-going');
plt.plot(east_pass[:,0], east_pass[:,4], linewidth=1,label='right-going');
plt.xlabel('Time [s]')
plt.ylabel('Length [m]')
plt.legend(fontsize=8,loc='upper right' );
plt.title('Speeds of Detected Vehicles',loc='right',fontsize=14)
fig.text(0.13, 0.9, total_txt_out);
#plt.show();
plt.savefig("east-length.png")
plt.close()

---------

west_l0= wl0;
west_l1= wl1;
west_s0= ws0;
west_s1= ws1;

total_txt_out = 'Hinotsume Bridge, west side: 2021-12-02_12.30.54';

# Car Length Histogram
fig = plt.figure(figsize=(12,4), dpi=300)
dl_bin= 0.5; # 20cm pitch
l_max0 = np.max(west_l0.flatten());
l_max1 = np.max(west_l1.flatten());
l_max = np.max((l_max1,l_max0));
b_num=int(np.floor(l_max/dl_bin));
le=b_num*dl_bin;
x1=0;
x2=le;
plt.xlim(x1, x2)
#txt_g_label='markers displacement';
plt.hist([west_l0.flatten(), west_l1.flatten()],range=(0,le),bins=b_num,rwidth=0.7,label=['left-going','right-going'])
plt.xlabel('Length [m]')
txt_ylabel='Number';
plt.ylabel(txt_ylabel)
plt.legend(fontsize=8,loc='upper right' );
plt.title('Vehicle Length Histogram (per 50 cm)',loc='right',fontsize=14)
fig.text(0.13, 0.9, total_txt_out);
plt.savefig("west-lengthhist.png")
plt.close()

# Car Speed Histogram
fig = plt.figure(figsize=(12,4), dpi=300)
dl_bin= 5; # 20cm pitch
l_max0 = np.max(west_s0.flatten());
l_max1 = np.max(west_s1.flatten());
l_max = np.max((l_max1,l_max0));
b_num=int(np.floor(l_max/dl_bin));
le=b_num*dl_bin;
x1=0;
x2=le;
plt.xlim(x1, x2)
plt.hist([west_s0.flatten(), west_s1.flatten()],range=(0,le),bins=b_num,rwidth=0.7,label=['left-going','right-going'])
plt.xlabel('Speed [km/h]')
txt_ylabel='Number';
plt.ylabel(txt_ylabel)
plt.legend(fontsize=8,loc='upper right' );
plt.title('Vehicle Speed Histogram (per 5 km/h)',loc='right',fontsize=14)
fig.text(0.13, 0.9, total_txt_out);
plt.savefig("west-speedhist.png")
plt.close()
