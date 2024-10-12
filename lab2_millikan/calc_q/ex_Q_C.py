import matplotlib.pyplot as plt
import numpy as np
import os
import subprocess
import time 

tm= os.path.getmtime("Q.C")
te=os.path.getmtime("ex.py")

isthere=os.path.isfile("Q.x")
if tm > te or isthere==False:
    os.system('g++ Q.C -o Q.x')
else:
    print("Using .x compiled at last execution")

subprocess.run(["./Q.x"])

q=np.loadtxt("q.dat")
S=np.loadtxt("s_q.dat")


plt.plot(q,S,".")
plt.show()
