#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>
#include <iomanip>

#include "TH1F.h"
#include "TApplication.h"
#include "TGraph.h"
#include "TCanvas.h"
#include "TF1.h"
#include "TAxis.h"

using namespace std;

// ===========================================================
// Read data from file and store them in a vector
// ===========================================================

vector<double> ParseFile( string filename ) {

  ifstream fin(filename.c_str());

  vector<double> v;
  double val;

  if ( !fin ) {
    cout << "Cannot open file " << filename << endl;
    exit(11);
  };

  while ( fin >> val ) v.push_back(val*pow(10,-19));

  fin.close();
  return v;
}

// ===========================================================                                                                                                                                              
// Compute S(q)                                                                                                                                                             
// ===========================================================     

double fun ( double q , vector<double> params ) {
  double sum = 0;
  for ( int k = 0 ; k < params.size() ; k++ ) sum+= pow (  q - params[k]/(round(params[k]/q)) , 2 ) ;
  return sum;
}

// ===========================================================                                                                                                                                                
// Compute qmin                                                                                                                                                                                        
// ===========================================================           

double deriv ( double qmin , vector<double> params) {
  double sum = 0;
  for ( int k = 0 ; k < params.size() ; k++ ) sum+= (  params[k]/ round(params[k]/qmin) );  
  return sum/params.size() ;
}

// ===========================================================                                                                                                                                                      
// This can be used to actually minimse S(q)                                                                                                                                                                    
// ===========================================================        

/*
double funROOT ( double* q , double * params ) { 
  double sum = 0;
  for ( int k = 0 ; k < 64 ; k++ ) sum+= pow (  q[0] - params[k] / (round(params[k]/q[0])), 2 ) ;
  return sum;
}
*/

// ===========================================================                                                                                                                                                      
// This code estimates the best value of qe from a set of 
// measurements (drop charges)                                                                                                                                                                       
// ===========================================================      

int main() {


  // read charges from file

  vector<double> charges = ParseFile("Q.dat");

  for(int i=0; i< charges.size(); i++){
    cout << charges[i] << endl; 
  }

  

  // show charges distribution

  TCanvas can1 ;
  can1.cd();
  TH1F histo("cariche","Charges distribution", 100, 0 , 20E-19);
  for ( auto i = 0; i < charges.size() ; i++ ) histo.Fill(charges[i]);
  histo.Draw();  
  histo.GetXaxis()->SetTitle("Charge [C]");

  TGraph g ;
  int counter = 0;
  double qmin = 0;
  double sqmin = DBL_MAX;

  

  for ( double value = 1.55e-19 ; value < 1.8E-19 ; value+=0.001E-19 ) {
    g.SetPoint(counter, value,fun( value , charges ) );
    if ( fun( value , charges )  < sqmin ) { sqmin =  fun( value , charges ) ; qmin = value ; }  ;
    counter++;
  }

    
  can1.SaveAs("plot.pdf");

  cout << "Found approximate minimum at q = " << qmin << endl;


  TCanvas can2;
  can2.cd();
  g.Draw("ALP");
  g.SetMarkerStyle(20);
  g.SetMarkerSize(0.5);
  g.SetTitle("Best charge value");
  g.GetXaxis()->SetTitle("Charge (C)") ;
  g.GetYaxis()->SetTitle("S(q) (C^{2})") ;

  can2.SaveAs("plot1.pdf");

  /*
  TF1 myfun( "charge",funROOT,1.5e-19 , 1.7E-19, 64); 
  for ( int k = 0 ; k < 64; k++ ) myfun.SetParameter(k, charges[k]); 
  cout << myfun.GetMinimumX() << endl ;
  */

  double mycharge = deriv(qmin, charges ) ;
  double uncer = sqrt(  fun(mycharge, charges) / ( charges.size() * (charges.size()-1))   ); 
  cout << "Measured charge = " << mycharge << " +/- " << uncer << "(stat only)" << endl;


  

}
