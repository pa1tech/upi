import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as ss

f = np.loadtxt("RawWaveform_HD2.txt")
time = f[:,0]; pos = f[:,1]; neg = f[:,2]

x2= (pos[2500:5500]+neg[2500:5500])/2; Y2 = np.fft.fft(x2,4000) #Second harmonic

pos_s = pos[2450:5450] #Shifted version of the signal by 
pos1 = pos[2500:5500]; neg1 = neg[2500:5500]

#Clipping the data
ii = np.where(pos1>2.24); pos1[ii]=2.24; ii = np.where(pos1<-2.24); pos1[ii]=-2.24;
Y1 = np.fft.fft(pos1,4000)

'''diff = pos-pos_s
diff[500:] = np.zeros(2500)
plt.plot(pos); plt.plot(pos-diff)
D = np.fft.fft(diff,4000); Y=np.fft.fft(pos,4000)'''


ii = np.where(pos1 >= 2.24)[0]
p1h = np.where(ii<1000)
p1 = len(p1h[0]); p2 = len(np.where(ii<1700)[0])-p1; p3 = len(np.where(ii<2500)[0])-p2-p1
p1h = ii[p1h]
mid = int(0.5*(p1h[0]+p1h[-1]))
l = int((p1-p2)*0.5)

x = np.array(range(-20,20)); y = np.zeros(40)
for i in x:
	pos2 = np.concatenate((pos1[:mid-(l+i)],pos1[mid+(l+i):]))
	Y3 = np.fft.fft(pos2,4000)
	y[i+20] = 20*np.log10(abs(Y1[5])/abs(Y3[10]))
plt.plot(x*0.5,y,label='using pos data'); plt.title("Variation of HD2 with variation in first pulse high time(dB)")
plt.xlabel("Variation in ns"); plt.ylabel("HD2"); plt.legend();plt.show()


i=0
pos1 = np.concatenate((pos1[:mid-(l+i)],pos1[mid+(l+i):]))
Y3 = np.fft.fft(pos1,4000)
print("HD2:", 20*np.log10(abs(Y1[5])/abs(Y1[10])),"with pos")
print("HD2:", 20*np.log10(abs(Y1[5])/abs(Y2[10])),"with pulse cancel")
print("HD2:", 20*np.log10(abs(Y1[5])/abs(Y3[10])),"with trimming")



plt.show()



'''ref = np.zeros(3000); 
ref[275:675] = np.ones(400); ref[675:1075] = -np.ones(400); ref[1075:1475] = np.ones(400); 
ref[1475:1875] = -np.ones(400); ref[1875:2275] = np.ones(400); ref[2275:2675] = -np.ones(400);

ref[675:675+170] = np.linspace(1,-1,170); ref[1075:1075+250] = np.linspace(-1,1,250); 
ref[1475:1475+250] = np.linspace(1,-1,250); ref[1875:1875+250] = np.linspace(-1,1,250); 
ref[2675:2675+250] = np.linspace(1,-1,250); ref[2675:2675+125] = np.linspace(-1,0,125); '''
#plt.plot(ref*2.27)