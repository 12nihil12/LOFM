import pandas as pd
import numpy as np 
import math
import matplotlib.pyplot as plt 
import matplotlib.colors as colors
import matplotlib 
import scipy as sc
from sklearn import linear_model



font = {'family' : 'serif',
         'size'   : 12,
         'serif':  'cmr10'
         }

matplotlib.rc('font', **font)
matplotlib.rcParams["mathtext.fontset"]="cm"



colors=["darkviolet", "blueviolet","blue","deepskyblue", "lawngreen","yellow","gold","red"]
data=pd.read_csv("data.csv")


A=[4.047E-07,
4.077E-07,
4.358E-07,
4.966E-07,
5.461E-07,
5.770E-07,
5.790E-07,
6.720E-07]
lA=np.array(A)

l=data["l"].to_numpy()

Y=data["Y"].to_numpy()**2
print(Y)

X=1/l**2 
lA=1/lA**2

fig, axs = plt.subplots(1, figsize=(6, 6))
reg=linear_model.LinearRegression()

plt.grid(color='gray', linestyle='dashed')

plt.scatter(X,Y,80,c=colors,edgecolors="k",zorder=1)
#plt.scatter(lA,Y,80,c="k",marker="X",edgecolors="k",zorder=1)

err=[2.716E+10,2.656E+10,2.175E+10,1.511E+10,
1.470E+10,
1.105E+10,
9.370E+09,
9.273E+09]

#plt.errorbar(X,Y,fmt="none",ecolor="k",xerr=err,yerr=0.0014)

X=X.reshape(-1,1)
Y=Y.reshape(-1,1)

reg.fit(X,Y)

print("Coefficienti regressione  | m:", reg.coef_[0][0], "| q:", reg.intercept_[0])




x=np.arange(2*10**12,6.5*10**12,100000000)
y=reg.coef_ [0][0]*x+ reg.intercept_[0]
#axs.plot(X,Y,"*")
axs.plot(x,y,"k",zorder=-1)



axs.set_xlim([2*10**12,6.5*10**12])







plt.rc('axes', unicode_minus=False)
axs.set_xlabel(r"$  \frac{1}{\lambda^2}  \ [ \mathrm{m}^{-2}] $")
plt.ylabel(r"$ n^2(\lambda)$")
axs.legend(["Punti sperimentali" ,r"Punti sperimentali con $\lambda$ tabulate", "Regressione"])

plt.show()



