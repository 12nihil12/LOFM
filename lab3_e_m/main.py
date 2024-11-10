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

#COSTANTI
U_0 = 4*math.pi *10**(-7) #permeabilità del vuoto 

#SPECIFICHE APPARATO 
R_b= 0.015 #raggio bobina
N=130 #numero spire 



def calc_B (I): 
    return U_0 *8/(5*math.sqrt(5))*N*I/R_b




# PRESA DATI


data=pd.read_csv("data.csv") 

I=data["I"].to_numpy() #corrente
r=data["r"].to_numpy() #raggio
V=data["V"].to_numpy() #potenziale

r=r*10**2
#print(r)
X=2*V 

B_0=calc_B(I)
#print(B_0)
conv=pd.read_csv("conv.csv")
#print(conv)

B_r=np.zeros(len(B_0))

for i in range(0, len(r)): 
    c=0
    if r[i]>8: 
        print(r[i]," > 8. Setting with max value")
        B_r[i]=B_0[i]*conv.iloc[39,1]
        break 
    if r[i]<0.2:
        B_r[i]=B_0[i]
        break
    while r[i]>conv.iloc[c,0]: 
        c=c+1
    #print(conv.iloc[c,0])
    if abs(r[i]-conv.iloc[c,0])<0.1:
        #print(conv.iloc[c,1])
        B_r[i]=B_0[i]*conv.iloc[c,1]
    else: 
        #print(conv.iloc[c-1,1])
        B_r[i]=B_0[i]*conv.iloc[c-1,1]


#print(B_r)

X=2*V 
Y=B_r**2*(r*10**(-3))**2

#print(Y)

fig, axs = plt.subplots(1, figsize=(6, 6))



reg=linear_model.LinearRegression()

X=X.reshape(-1,1)
Y=Y.reshape(-1,1)

reg.fit(X,Y)

print("Coefficienti regressione  | m:", reg.coef_[0][0], "| q:", reg.intercept_[0])





x=np.arange(300,900,0.01)
y=reg.coef_ [0][0]*x+ reg.intercept_[0]
axs.plot(X,Y,"*")
ax1=axs.twinx()
ax1.plot(x,y,"g")


k=1/(1.78*10**11)
ax2=axs.twinx()

y=k*x #retta attesa
ax2.plot(x,y,"r")

axs.set_xlim([300,900])








plt.rc('axes', unicode_minus=False)
axs.set_xlabel("$ 2\Delta  V \; [ \mathrm{V}]$")
plt.ylabel("$ B_r^2 r^2  \; [\mathrm{T}^2\mathrm{m}^2]$")
axs.legend(["Punti sperimentali"],loc="upper right")
ax1.legend(["Fit"],loc="upper right")
ax2.legend([r"Retta attesa con e/m = $ 1.78 \cdot 10^{11} \mathrm{C/kg} $ "],loc="lower right")
plt.grid()

plt.show()
fig.savefig("lab3.eps",format="eps")
fig.savefig("lab3.png",format="png")

print("\n e\m", (1/reg.coef_ [0][0])*10**(-11))








