import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np 
import math
import random as rn

N=1000

def S(Q,q): 
    sum=0
    for Qi in Q: 
        k=math.floor(Qi/q+0.5)
        sum= sum + pow((Qi/k - q),2)

    return sum 



Q=np.loadtxt("Q.dat")

#q=np.arange(1.4,1.8,0.002)
q=np.zeros(N)
S_q=np.zeros(len(q))

for a in range(0,len(q)): 
    q[a]=round(rn.uniform(1.4,1.8),3)
    S_q[a]=S(Q,q[a])


plt.plot(q,S_q, ".")
plt.show()
plt.savefig("plot.eps",format='eps')

exit()


