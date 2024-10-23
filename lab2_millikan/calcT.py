import pandas as pd
import numpy as np 
import math
import matplotlib.pyplot as plt 
from sklearn import linear_model

T=np.arange(10,40,1)
R=np.array([3.239,3.118,3.004,2.897,2.795,2.700,2.610,2.526,2.446,2.371,2.300,2.233,2.169,2.110,2.053,2.000,1.950,1.902,1.857,1.815,1.774,1.736,1.700,1.666,1.634,1.603,1.574,1.547,1.521,1.496])


fig2, axs = plt.subplots(1, figsize=(8, 8))


reg=linear_model.LinearRegression()

R=R.reshape(-1,1)
reg.fit(R,T)


plt.plot(R,T,".")
x=np.arange(1.4,3.3,0.01)
y=reg.coef_ *x + reg.intercept_
plt.plot(x,y,"g")

print("Coefficienti regressione | m:", reg.coef_, "| q:", reg.intercept_)


axs.set_xlim([1.4,3.3])

plt.rc('axes', unicode_minus=False)
plt.xlabel("$T$")
plt.ylabel("$R$")
plt.legend([ "Punti sperimentali", "Fit"])
plt.grid()

plt.show()
#fig2.savefig("lab1_c_2.eps",format="eps")
fig2.savefig("lab1_c_2.png",format="png")
