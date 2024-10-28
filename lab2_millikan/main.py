import pandas as pd
import numpy as np 
import math
import sys
import os
import random as rn
import matplotlib.pyplot as plt 
import matplotlib



font = {'family' : 'serif',
         'size'   : 15,
         'serif':  'cmr10'
         }

matplotlib.rc('font', **font)
matplotlib.rcParams["mathtext.fontset"]="cm"



# SETTING OF CONSTANTS
b=8.2*pow(10,-3) #parametro
p=1.1*10**5  #pressione atmosferica (Pa)
g=9.806 #accelerazione di gravità
d_o=860 # densita olio (kg/m^3)
d_a=1.293 #densità aria (kg/m^3)
Dz=0.5*10**(-3) #base di volo 

d=7.59*10**(-3)#distanza fra le armature !! VA MISURATA 
N=1000 #how many points in interval

def vis_coef (T): #coefficiente di viscosità al variare della temperatura (°C)
        return round((1.800 + 4.765*pow(10,-3)*(T-15)),3)*pow(10,-5)

def r(v_r,vis): #raggio della particella calcolato a partire da v_r 
    r=math.sqrt(pow((b/(2*p)),2)+9*vis*v_r/(2*g*(d_o-d_a)))- b/(2*p)
    return r

def calcr(data0,vis): #aggiunge raggio particella a dataframe
    data0["r[um]"]=np.zeros(len(data0["t[s]"]))
    for i in range(0,5):
        data0.loc[i, "r[um]"]=round((r((data0.loc[i,"v[um/s]"]*pow(10,-6)),vis))*10**6,3)
"""
def v(data): # velocità particella
    data["v[um/s]"]=np.zeros(len(data["t[s]"]))
    data.iloc[0, 1]= round((Dz/data.iloc[0,0])*10**6,1)
    for i in range(1,5):
        data.iloc[i, 1]= round( (Dz/(data.iloc[i,0]-data.iloc[(i-1),0]))*10**6,1)
"""
def v(data): # velocità particella
    data["v[um/s]"]=np.zeros(len(data["t[s]"]))
    for i in range(0,5):
        data.iloc[i, 1]= round((Dz/(data.iloc[i,0]))*10**6,1)

def q(data_Vp,data_Vn,data0,DV): #carica
    E=DV/d
    r_0=round(data0.iloc[:,2].mean(),3)*10**(-6)
    v_r=round(data0.iloc[:,1].mean(),3)
    print(" \n r_0: " ,'%.3f' % ( r_0*10**7), "e-7 m \n",sep="")
    data_Vp["q[C] (e-19)"]=round((-4/3*math.pi*r_0**3*(d_o-d_a)*(g/E)*(1-data_Vp["v[um/s]"]/v_r))*10**19,3)
    data_Vn["q[C] (e-19)"]=round((-4/3*math.pi*r_0**3*(d_o-d_a)*(g/(-E))*(1+data_Vn["v[um/s]"]/v_r))*10**19,3)

def calc_q_drop(dn):


    #STARTUP 
    print(dn)
    T=float(input("Temperatura (°C): "))
    #vis=1.83*10**(-5) 
    vis=vis_coef(T) #setta il coefficiente di viscosità per la temperatura data
    print("Coefficiente di viscosità: ",'%.2f' % (vis*10**5),"e-5 Ns/m^2","\n",sep="")

    
    times="times/"+ dn + ".csv"
    output="output/" +dn + ".csv"

    if os.path.isfile(output):
        command="rm " + output
        os.system(command)


    #MODULO 1: RAGGIO (DV=0)

    data0=pd.DataFrame(index=[0,1,2,3,4])
    #data0["t[s]"]=pd.read_excel("times.xlsx", sheet_name=dn,usecols="A")
    data0["t[s]"]=pd.read_csv(times,usecols=["t0[s]"])
   
    
    v(data0) #calcola velocità e la salva nel dataframe
    calcr(data0,vis)#calcola il raggio e lo salva nel dataframe

    print("\n DV=0")
    print(data0)


    #MODULO 2: CARICA 

    DV=float(input("Differenza di potenziale: (V) "))
    while DV<=0 :
        DV=float(input("DV>0: "))

    data_Vp=pd.DataFrame(index=[0,1,2,3,4])
    data_Vn=pd.DataFrame(index=[0,1,2,3,4])
    #data_Vp["t[s]"]=pd.read_excel("times.xlsx",usecols="B")
    #data_Vn["t[s]"]=pd.read_excel("times.xlsx",usecols="C")
    data_Vp["t[s]"]=pd.read_csv(times,usecols=["tVp[s]"])
    data_Vn["t[s]"]=pd.read_csv(times,usecols=["tVn[s]"])
    v(data_Vp) #calcola le velocità
    v(data_Vn)


    q(data_Vp,data_Vn,data0,DV) #calcolo carica

    print("\n DV=", DV, " V")
    print(data_Vp)
    print("\n DV=", -DV, " V")
    print(data_Vn)

    print("\n")


    data=pd.concat([data0,data_Vp,data_Vn],axis=1)

    print(data)

    data.to_csv(output,index=False,mode='a')

    data_Vp["q[C] (e-19)"].to_csv("Q.dat",index=False, header=False, mode = 'a') #prints out Q in orderly fashion
    data_Vn["q[C] (e-19)"].to_csv("Q.dat",index=False, header=False,mode = 'a') #prints out Q in orderly fashion

    #qp=data_Vp["q[C] (e-19)"].to_numpy()
    #qn=data_Vn["q[C] (e-19)"].to_numpy()


    #Q=np.hstack((qn,qp))

    print("\n")
    

    return 

def S(Q,q): 
    sum=0
    for Qi in Q: 
        k=math.floor(Qi/q+0.5)
        sum= sum + pow((Qi/k - q),2)

    return sum 



#MAIN



if len(sys.argv)!=3: 
    print("Syntax of ", sys.argv[0], " <how many drops>  <mode> \n mode= f -fresh start \n mode=a -add drop" )
    exit()




if(sys.argv[2]=="f"): 
    if os.path.isfile("Q.dat"):
        os.system("rm Q.dat")

    if os.path.isfile("output/check.txt")==False:
        os.system("mkdir output")
        os.system("> output/check.txt")

    for i in range(1,11):
        dn="drop"+str(i)
        calc_q_drop(dn)

elif(sys.argv[2]=="a"): 
    d=int(sys.argv[1])
    for i in range(d,(d+1)):
        dn="drop"+str(i)
        calc_q_drop(dn)
elif(sys.argv[2]=="q"): 
    print("Graphing from file <Q.dat>")

Q=np.loadtxt("Q.dat")

#q=np.arange(1.4,1.8,0.002)
q=np.zeros(N)
S_q=np.zeros(len(q))

for a in range(0,len(q)): 
    q[a]=round(rn.uniform(1.4,1.8),3)
    S_q[a]=S(Q,q[a])


plt.plot(q,S_q, ".")
plt.xlabel(r"$q_{\omega} \;  [\mathrm{C}]$")
plt.ylabel(r"$\sum_{i=1}^N \left( \frac{Q_i}{k_i(q_{\alpha})} - q_{\alpha}\right)^2$")
plt.show()
plt.savefig("plot.png",format='png')



exit()





