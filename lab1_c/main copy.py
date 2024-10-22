import pandas as pd
import numpy as np 
import math
import matplotlib.pyplot as plt 
import matplotlib 
import scipy as sc
from sklearn import linear_model

font = {'family' : 'serif',
         'size'   : 12,
         'serif':  'cmr10'
         }

matplotlib.rc('font', **font)
matplotlib.rcParams["mathtext.fontset"]="cm"
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
    return math.sqrt(der_D**2*sD**2 + der_a**2*sa**2+der_f2**2*sf2**2)



# PRESA DATI
data=pd.read_csv("data.csv") #frequenza, delta, delta err


#print(data)

n=int(data.size/3)

w=np.zeros(n) #omega
d=np.zeros(n) #delta


#for i in range (0,w.size):
    #w[i]=2*math.pi*(data.iloc[i,1])-w0
    #d[i]=(data.iloc[i,2])-d0


#plt.plot(w,d,"*")
plt.plot(data["Dw[rad/s]"],data["|Dd|[mm]"],".")

# CONFRONTO CON RETTA ATTESA

c=2.997*10**11 #velocità luce
k=4*f2*D**2/((D+a-f2)*c)
#x=np.arange(4000,10000,0.01)#omega
#y=k*x #delta

ax = plt.gca()
ax.set_xlim([4000, 10000])

[m,q]=np.polyfit(data["Dw[rad/s]"],data["|Dd|[mm]"],1)

print(q/m)

x=np.arange(4000,10000,0.01)#omega
y=m*x +q #delta
plt.plot(x,y, "g")
y=k*x #delta
plt.plot(x,y, "r")

plt.xlabel("$\Delta \omega \; \mathrm{[rad/s]}$")
plt.ylabel("$\Delta \delta \; \mathrm{[mm]}$")
plt.legend([ "Punti sperimentali","Fit", r"Retta attesa con $ c=2.997 \cdot 10^{11} [\mathrm{mm/s}]$"],loc="upper left")


reg=linear_model.LinearRegression()

x=data["Dw[rad/s]"].to_numpy()
y=data["|Dd|[mm]"].to_numpy()
x=x.reshape(-1,1)

reg.fit(x,y)

print(reg.coef_)
print(reg.intercept_)




plt.grid()
#plt.show()



""" 

c=pd.read_csv("c.csv")
print(c)
c_g=(1/(math.sqrt(2*math.pi)*0.02))*math.e**(-((c-2.83)**2)/(2*0.02*2)) 
#plt.plot(c,c_g,"*")

x=np.arange(1.5,4,0.01)
y=(1/(math.sqrt(2*math.pi)*0.02))*math.e**(-((x-2.83)**2)/(2*0.02*2)) 
plt.plot(x,y, "g")

#plt.show()

def istogramma(dati,max,min,nbins):
    min=min-0.01

    d = (max - min)/nbins; 
    count=np.zeros(nbins)
    
    for k in range(0,len(dati)):
        if dati.iloc[k,0]> min and dati.iloc[k,0] <= max:
            shift=0 
            while min + shift*d < dati.iloc[k,0]: 
                shift=shift +1
            
        #print( dati[k] , " < ",  min + shift * d )
        count[shift - 1]=count[shift-1]+1; 
    
    for k in range(0,nbins):
        print( round((min + k* d),2), " to ", round(( min + (k+1)*d),2), " | ",end="")    
        for j in range(0,int(count[k])): 
            print( "*",end=" ")
        print("\n")

    return count

istogramma(c,2.98,2.57,10)

counts, bins = np.histogram(c,10)
print(counts,bins)
plt.bar(bins,counts)

"""


plt.show()
