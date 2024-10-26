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



# PRESA DATI


data=pd.read_csv("data.csv") #frequenza, delta, delta err

data= data.reset_index()

cw_w=np.array(1)
cw_d=np.array(1)
ccw_w=np.array(1)
ccw_d=np.array(1)


for index, row in data.iterrows(): 
    if row["senso"] == 'A': 
        ccw_d=np.append(ccw_d,row["Dd[mm]"])
        ccw_w=np.append(ccw_w,row["Dw[rad/s]"])
    else: 
        cw_d=np.append(cw_d,row["Dd[mm]"])
        cw_w=np.append(cw_w,row["Dw[rad/s]"])



ccw_d=np.delete(ccw_d,0)
ccw_w=np.delete(ccw_w,0)
cw_w=np.delete(cw_w,0)
cw_d=np.delete(cw_d,0)

w=np.concatenate((cw_w,ccw_w))
d=np.concatenate((abs(cw_d),ccw_d))

fig1, axs = plt.subplots(1, figsize=(8,8))

plt.plot(cw_w,cw_d,"o")
plt.plot(ccw_w,ccw_d,"s")


reg_cw=linear_model.LinearRegression()
reg_ccw=linear_model.LinearRegression()

cw_w=cw_w.reshape(-1,1)
reg_cw.fit(cw_w,cw_d)
ccw_w=ccw_w.reshape(-1,1)
reg_ccw.fit(ccw_w,ccw_d)

x=np.arange(4000,10000,0.01)
y=reg_cw.coef_ *x + reg_cw.intercept_

print("Coefficienti regressione (punti senso orario) | m:", reg_cw.coef_, "| q:", reg_cw.intercept_)
print("Coefficienti regressione (punti senso antiorario) | m:", reg_ccw.coef_, "| q:", reg_ccw.intercept_)


plt.plot(x,y,"g")

x=np.arange(4000,10000,0.01)
y=reg_ccw.coef_ *x + reg_ccw.intercept_

plt.plot(x,y,"r")



axs.set_xlim([4000, 10000])


c=2.997*10**11 #velocità luce
k=4*f2*D**2/((D+a-f2)*c)

y=-k*x #delta

plt.plot(x,y,"b")


y=k*x #delta

plt.plot(x,y,"m")




plt.rc('axes', unicode_minus=False)
plt.xlabel("$\Delta \omega \; \mathrm{[rad/s]}$")
plt.ylabel("$\Delta \delta \; \mathrm{[mm]}$")
plt.legend([ "Punti sperimentali(senso orario)","Punti sperimentali (senso antiorario)", "Fit","Fit",r"Retta attesa con $ c=2.997 \cdot 10^{11} [\mathrm{mm/s}]$",r"Retta attesa con $ c=2.997 \cdot 10^{11} [\mathrm{mm/s}]$"])
plt.grid()



plt.show()
fig1.savefig("lab1_c_1.eps",format="eps")
fig1.savefig("lab1_c_1.png",format="png")




fig2, axs = plt.subplots(1, figsize=(8, 8))



reg=linear_model.LinearRegression()

w=w.reshape(-1,1)
reg.fit(w,d)
w=w.reshape(-1,1)
reg.fit(w,d)

print("Coefficienti regressione (|Dd|) | m:", reg.coef_, "| q:", reg.intercept_)




plt.plot(w,d,".")
y=reg.coef_ *x + reg.intercept_
plt.plot(x,y,"g")
y=k*x #retta attesa
plt.plot(x,y,"r")



axs.set_xlim([4000, 10000])

plt.rc('axes', unicode_minus=False)
plt.xlabel("$\Delta \omega \; \mathrm{[rad/s]}$")
plt.ylabel("$ |\Delta \delta | \; \mathrm{[mm]}$")
plt.legend([ "Punti sperimentali", "Fit",r"Retta attesa con $ c=2.997 \cdot 10^{11} [\mathrm{mm/s}]$"])
plt.grid()

plt.show()
fig2.savefig("lab1_c_2.eps",format="eps")
fig2.savefig("lab1_c_2.png",format="png")









