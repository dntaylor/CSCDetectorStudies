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
  bool isME42Region(int endcap, int sector, int eta, int phi);
  void doChamberOccupancy(int ME1, int ME2, int ME3, int ME4, bool isME42);
  void outputLCTProperties(int endcap, int sector, int subsector, int station, int ring, int chamber, int CSCID, int eta, int phi, int strip, int wire);
  void doTrackLCTRatePlots(int size, bool isME42);
  void doTrackPtRatePlots(double pt, bool isME42);
  void doTrackPhiRatePlots(double phi, int endcap);
  void ratePlotHelper(TH1* hist, int nBins, double min, double max, double val);
  void end();

private : 
  
  TH1F* hChamberOccupancyME42;
  TH1F* hChamberOccupancyNonME42;
  TH1F* hTrackLCTRateME42;
  TH1F* hTrackLCTRateNonME42;
  TH1F* hTrackPtRateME42;
  TH1F* hTrackPtRateNonME42;
  TH1F* hTrackPhiRatePlusEndcap;
  TH1F* hTrackPhiRateMinusEndcap;
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
  std::cout << "loaded " << nevents << " events" << std::endl;

  bookhistos();

  //loop over the events
  for (Long64_t i=0; i<nevents; i++)
    {
      //load the i-th event 
      Long64_t ientry = LoadTree(i); if (ientry < 0) break;
      GetEntry(i);

      // status
      if(i!=0 && (i%1000)==0) { std::cout << "- processing event " << i << std::endl; } 

      // loop over tracks
      int trackSize = csctf_->trSize;
      for (int trk = 0; trk<trackSize; trk++) {
         int lctSize = csctf_->trNumLCTs[trk];
         // check if track crosses ME42 region
         int eta = csctf_->trLctglobalEta[trk][lctSize-1];   // goes from 0-125 within endcap
         int phi = csctf_->trLctglobalPhi[trk][lctSize-1];   // goes from ~50-4050 within sector
         int endcap = csctf_->trLctEndcap[trk][lctSize-1];   // 1 or -1
         int sector = csctf_->trLctSector[trk][lctSize-1];   // 1-6 in + 7-12 in - (starts at 15 deg)
         //int subsector = csctf_->trLctSubSector[trk][lctSize-1]; // ?? most 0 (some 1 or 2)
         //int station = csctf_->trLctStation[trk][lctSize-1]; // 1-4
         //int ring = csctf_->trLctRing[trk][lctSize-1];       // 1-3 in station 1, 1-2 in 2-4
         //int chamber = csctf_->trLctChamber[trk][lctSize-1]; // 1-18 or 1-36 (dependent on geom)
         //int strip = csctf_->trLctstripNum[trk][lctSize-1];  //
         //int wire = csctf_->trLctwireGroup[trk][lctSize-1];  //
         //int CSCID = csctf_->trLctTriggerCSCID[trk][lctSize-1]; //
         bool isME42 = isME42Region(endcap,sector,eta,phi);
         if (eta<23 || eta>72) { break; } // break out if track is outside ME4/2 eta region
         //if (station == 3 && ring == 2) {
         //   outputLCTProperties(endcap,sector,subsector,station,ring,chamber,CSCID,eta,phi,strip,wire);
         //}


         // track chamber occupancy
         int ME1 = csctf_->trME1ID[trk];
         int ME2 = csctf_->trME2ID[trk];
         int ME3 = csctf_->trME3ID[trk];
         int ME4 = csctf_->trME4ID[trk];
         //std::cout << " " << ME1 << " " << ME2 << " " << ME3 << " " << ME4 << " " << isME42 << std::endl;
         doChamberOccupancy(ME1,ME2,ME3,ME4,isME42);
         doTrackLCTRatePlots(lctSize,isME42);
         doTrackPtRatePlots(csctf_->trPt[trk],isME42);
         doTrackPhiRatePlots(csctf_->trPhi_02PI[trk],csctf_->trEndcap[trk]);
      }

    } //end loop on events

  //////////////////////////////// 
  //////////////////////////////// 
  // write histo to fil]
  end();
  theFile->Write();
  theFile->Close();
}

void L1CSCTFAnalysis::bookhistos(){

   hChamberOccupancyME42 = new TH1F("hChamberOccupancyME42","Chamber Occupancy: ME4/2 Region",16,-.5,15.5);
   hChamberOccupancyNonME42 = new TH1F("hChamberOccupancyNonME42","Chamber Occupancy: Non-ME4/2 Region",16,-.5,15.5);

   // station hit pattern labels
   const int n = 16;
   const char *hitPatternLabel[n] = {"None","ME1","ME2","ME3","ME4","ME1+2","ME1+3","ME1+4","ME2+3","ME2+4","ME3+4","ME1+2+3","ME1+2+4","ME1+3+4","ME2+3+4","ME1+2+3+4"};
   for (int i=1;i<=n;i++) hChamberOccupancyME42->GetXaxis()->SetBinLabel(i,hitPatternLabel[i-1]);
   for (int i=1;i<=n;i++) hChamberOccupancyNonME42->GetXaxis()->SetBinLabel(i,hitPatternLabel[i-1]);

   hTrackLCTRateME42 = new TH1F("hTrackLCTRateME42","LCT Rate: ME4/2 Region",5,-.5,4.5);
   hTrackLCTRateNonME42 = new TH1F("hTrackLCTRateNonME42","LCT Rate: Non-ME4/2 Region",5,-.5,4.5);
   hTrackPtRateME42 = new TH1F("hTrackPtRateME42","CSCTF p_{T} Rate: ME4/2 Region",10,-10,190);
   hTrackPtRateNonME42 = new TH1F("hTrackPtRateNonME42","CSCTF p_{T} Rate: Non-ME4/2 Region",10,-10,190);
   hTrackPhiRatePlusEndcap = new TH1F("hTrackPhiRatePlusEndcap","CSCTF #phi: Plus Endcap",6,0,2*TMath::Pi());
   hTrackPhiRateMinusEndcap = new TH1F("hTrackPhiRateMinusEndcap","CSCTF #phi: Minus Endcap",6,0,2*TMath::Pi());
}

void L1CSCTFAnalysis::end() {
   // things to do after run
   
   // normalize rate plots to first bin
   hTrackLCTRateME42->Scale(1./hTrackLCTRateME42->GetBinContent(1));
   hTrackLCTRateNonME42->Scale(1./hTrackLCTRateNonME42->GetBinContent(1));
   hTrackPtRateME42->Scale(1./hTrackPtRateME42->GetBinContent(1));
   hTrackPtRateNonME42->Scale(1./hTrackPtRateNonME42->GetBinContent(1));
}

bool L1CSCTFAnalysis::isME42Region(int endcap, int sector, int eta, int phi) {
   // ME 42 chambers 9-13 in CSCTF coordinates
   // eta: 23-72
   // phi: 49-3387 in sector 2 of endcap 1
   // method currently just looks at outermost LCT eta and phi
   // (should really look at the local eta and phi value in the 4th station
   // even if there is no LCT in the 4th station)
   return (eta>=23 && eta<=72 && endcap==1 && sector==2 && phi>=49 && phi<=3387);
}

void L1CSCTFAnalysis::doChamberOccupancy(int ME1, int ME2, int ME3, int ME4, bool isME42) {
   // pattern:
   // 0 stations: 0
   // 1 stations: 1 = 1, 2 = 2, 3 = 3, 4 = 4
   // 2 stations: 12 = 5, 13 = 6, 14 = 7, 23 = 8, 24 = 9, 34 = 10
   // 3 stations: 123 = 11, 124 = 12, 134 = 13, 234 = 14
   // 4 stations: 1234 = 15
   int val = 0;
   if (!ME1 && !ME2 && !ME3 && !ME4) { val = 0; }
   if (ME1 && !ME2 && !ME3 && !ME4) { val = 1; }
   if (!ME1 && ME2 && !ME3 && !ME4) { val = 2; }
   if (!ME1 && !ME2 && ME3 && !ME4) { val = 3; }
   if (!ME1 && !ME2 && !ME3 && ME4) { val = 4; }
   if (ME1 && ME2 && !ME3 && !ME4) { val = 5; }
   if (ME1 && !ME2 && ME3 && !ME4) { val = 6; }
   if (ME1 && !ME2 && !ME3 && ME4) { val = 7; }
   if (!ME1 && ME2 && ME3 && !ME4) { val = 8; }
   if (!ME1 && ME2 && !ME3 && ME4) { val = 9; }
   if (!ME1 && !ME2 && ME3 && ME4) { val = 10; }
   if (ME1 && ME2 && ME3 && !ME4) { val = 11; }
   if (ME1 && ME2 && !ME3 && ME4) { val = 12; }
   if (ME1 && !ME2 && ME3 && ME4) { val = 13; }
   if (!ME1 && ME2 && ME3 && ME4) { val = 14; }
   if (ME1 && ME2 && ME3 && ME4) { val = 15; }
   if (isME42) { hChamberOccupancyME42->Fill(val); }
   if (!isME42) { hChamberOccupancyNonME42->Fill(val); }
}

void L1CSCTFAnalysis::outputLCTProperties(int endcap, int sector, int subsector, int station, int ring, int chamber, int CSCID, int eta, int phi, int strip, int wire) {
   std::cout << "CSC LCT Properties:" << std::endl;
   std::cout << " E: " << endcap << " S: " << station << " R: " << ring << " C: " << chamber << std::endl;
   std::cout << " sector: " << sector << " subsector: " << subsector << std::endl;
   std::cout << " CSCID: " << CSCID << std::endl;
   std::cout << " st: " << strip << " w: " << wire << std::endl;
   std::cout << " eta: " << eta << " phi: " << phi << std::endl;
}

void L1CSCTFAnalysis::doTrackLCTRatePlots(int size, bool isME42) {
   if (isME42) { ratePlotHelper(hTrackLCTRateME42,5,0,4,size); }
   else { ratePlotHelper(hTrackLCTRateNonME42,5,0,4,size); }
}

void L1CSCTFAnalysis::doTrackPtRatePlots(double pt, bool isME42) {
   if (isME42) { ratePlotHelper(hTrackPtRateME42,10,0,180,pt); }
   else { ratePlotHelper(hTrackPtRateNonME42,10,0,180,pt); }
}

void L1CSCTFAnalysis::ratePlotHelper(TH1* hist, int nBins, double min, double max, double val) {
   double binWidth = (max-min)/(nBins-1);
   for (int n=0; n<nBins; n++) {
      if (val>=(min+n*binWidth)) { hist->Fill(min+n*binWidth); }
   }
}

void L1CSCTFAnalysis::doTrackPhiRatePlots(double phi, int endcap) {
   if (endcap==1) { hTrackPhiRatePlusEndcap->Fill(phi); }
   else { hTrackPhiRateMinusEndcap->Fill(phi); }
}
