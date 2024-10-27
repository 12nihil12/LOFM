#include <iostream> 
#include <cmath>
#include <fstream> 
#include "TH1F.h"
#include "TGraph.h"
#include "TApplication.h"
#include "TCanvas.h"


using namespace std; 

double S(double * Q, double q); 

int main(){

    cout << "Hi"; 


    ifstream in; 
    in.open("Q.dat"); 
    if(in.fail()){
        return 0; 
    }

    cout << "Hi"; 

    double Q[90]; 

    for (int i=0; i < 90; i++){
        in >> Q[i]; 
    }

    cout << "Hi"; 

    double q[200]; 

    int a=0; 
    q[0]=1.4; 

    while(q[a] <=1.8 && a<200){
        a=a+1;
        q[a]=q[a-1]+0.002; 
    }

     


    ofstream out1,out2; 
    out1.open("q.dat");
    out2.open("s_q.dat");
    
    double S_q[200];

    for(int a=0; a < 200; a++){
        out1 << q[a] << endl; 
        S_q[a]=S(Q,q[a]);
        out2<< S_q[a] << endl; 

    }

    TCanvas c;

    auto g= new TGraph(200,q,S_q);
    g->Draw("AC*"); 

    
    c.SaveAs("plot.pdf");

    

}

double S(double *Q, double q){
    double sum=0; 
    for(int i=0; i < 80; i++){
        int k= int(Q[i]/q+0.5); 
        sum= sum + pow(Q[i]/k-q,2); 
    }
    return sum; 
}