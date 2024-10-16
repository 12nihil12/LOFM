import pandas as pd
import numpy as np 
import math
import matplotlib.pyplot as plt 


# SPECIFICHE APPARATO (in mm)
#fuochi
f1=48
f2=252

l12=1#distanza lenti
D=1 #distanza specchio concavo-rotante
a=1 #distanza L2-specchio rotante
b=f2*(D+a)/(D+a-f2) #distanza sorgente-L2


def err_m (dw,dd,sw,sd)
    k=(4*f2*D**2)/(D+a-f2)
    inc= k*math.root(sw**2/dd**2 + sd**2*dw**2/dd**4)

    return

def err_s(sD,sa,sf2)
    0000000000

# PRESA DATI
data=pd.read_csv("data.csv") #frequenza, delta, delta err
w0=1 
d0=0

print(data)

n=int(data.size/3)

w=np.zeros(n) #omega
d=np.zeros(n) #delta


for i in range (0,w.size):
    w[i]=2*math.pi*(data.iloc[i,1])-w0
    d[i]=(data.iloc[i,2])-d0


plt.plot(w,d,"*")

# CONFRONTO CON RETTA ATTESA

c=3*10**11 #velocità luce
k=4*f2*D**2/((D+a-f2)*c)
x=np.arange(60,6000,0.01)#omega
y=k*x #delta

plt.plot(x,y, "g")
plt.xlabel("Dw [rad/s]")
plt.ylabel("Dd [mm]")
plt.show()



