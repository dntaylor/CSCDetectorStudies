#include "L1Ntuple.h"
#include "hist.C"
#include "Style.C"

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TTree.h>
#include <TFriendElement.h>
#include <TList.h>
//#include <TGraph.h>
#include <TGraphAsymmErrors.h>
#include <TLine.h>
#include <stdio.h>
#include <math.h>
#include <iostream>
#include <fstream>

#include "TInterpreter.h"
#include "modifiedStyle.C"
#include "TColor.h"
#include "TF1.h"
#include "TMath.h"

using namespace std;

class L1CSCTFAnalysis : public L1Ntuple
{
public :

  //constructor    
  L1CSCTFAnalysis() {}
  L1CSCTFAnalysis(std::string filename) : L1Ntuple(filename) {}
  
  //main function macro : arguments can be adpated to your need
  void run(Long64_t nevents);
  void bookhistos();     // to book histograms

private : 
  
  TH1F* hPtMuons;
  
};


// --------------------------------------------------------------------
//                             run function 
// --------------------------------------------------------------------
void L1CSCTFAnalysis::run(Long64_t nevents)
{

  // output file
  TFile *theFile    =new TFile("L1CSCTFAnalysis.root", "RECREATE");
  theFile->cd();

  // ------------------------------------------------------------------------------
  // variables
  // ------------------------------------------------------------------------------

  //number of events to process
  if (nevents==-1 || nevents>GetEntries()) nevents=GetEntries();

  bookhistos();

  //loop over the events
  for (Long64_t i=0; i<nevents; i++)
    {
      //load the i-th event 
      Long64_t ientry = LoadTree(i); if (ientry < 0) break;
      GetEntry(i);

    } //end loop on events

  //////////////////////////////// 
  //////////////////////////////// 
  // write histo to fil]
  theFile->Write();
  theFile->Close();
}

void L1CSCTFAnalysis::bookhistos(){

  hPtMuons = new TH1F("hPtMuons", "p_{T}(#mu)", 200,  0., 200.);
}
