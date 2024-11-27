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


data=pd.read_csv("data.csv")

n=data["n"].to_numpy()
l=data["l"].to_numpy()
Y=n
X=1/l**2 

fig, axs = plt.subplots(1, figsize=(6, 6))
reg=linear_model.LinearRegression()


X=X.reshape(-1,1)
Y=Y.reshape(-1,1)

reg.fit(X,Y)

print("Coefficienti regressione  | m:", reg.coef_[0][0], "| q:", reg.intercept_[0])



x=np.arange(2.5e12,6.5e12,0.01)
y=reg.coef_ [0][0]*x+ reg.intercept_[0]
axs.plot(X,Y,"*")
axs.plot(x,y,"g")

plt.show()
