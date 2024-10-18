import pandas as pd
import numpy as np 
import math
import matplotlib.pyplot as plt 


# SPECIFICHE APPARATO (in mm)
#fuochi
f1=48
f2=252

l12=316#distanza lenti
D=13350 #distanza specchio concavo-rotante
a=505 #distanza L2-specchio rotante
b=f2*(D+a)/(D+a-f2) #distanza sorgente-L2


def err_m (dw,dd,sw,sd):
    k=(4*f2*D**2)/(D+a-f2)
    inc= k*math.sqrt(sw**2/dd**2 + sd**2*dw**2/dd**4)

    return inc 

def err_s(sD,sa,sf2,wm,dm):
    der_D= 4*f2*wm/dm * (D**2+2*a*D-2*f2*D)/(D+a -f2)**2
    der_a = 4*f2*D**2*wm/dm*1/(D+a-f2)**2
    der_f2=4*D**2*wm/dm*(D+a)/(D+a-f2)**2
    inc= math.sqrt(der_D**2*sD**2 + der_a**2*sa**2+der_f2**2*sf2**2)

# PRESA DATI
data=pd.read_csv("data.csv") #frequenza, delta, delta err
#w0=60*2*math.pi
#d0=8.28#mm

#print(data)

n=int(data.size/3)

#w=np.zeros(n) #omega
#d=np.zeros(n) #delta


#for i in range (0,w.size):
    #w[i]=2*math.pi*(data.iloc[i,1])-w0
    #d[i]=(data.iloc[i,2])-d0


#plt.plot(w,d,"*")
plt.plot(data["Dw[rad/s]"],data["|Dd|[mm]"],".")

# CONFRONTO CON RETTA ATTESA

c=2.997*10**11 #velocità luce
k=4*f2*D**2/((D+a-f2)*c)
x=np.arange(4000,10000,0.01)#omega
y=k*x #delta

plt.plot(x,y, "g")
plt.xlabel("$\Delta \omega \; \mathrm{[rad/s]}$")
plt.ylabel("$\Delta \delta \; \mathrm{[mm]}$")
plt.legend([ "Punti sperimentali", r"Retta attesa con $ c=2.997 \cdot 10^{11} \mathrm{[m/s]}$"])
plt.grid()
plt.show()



