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
   void doTrackLCTRatePlots(int size, bool isME42, int lctSize);
   void doTrackPhiRatePlots(double phi, int endcap, int lctSize, bool isME42);
   void doTrackPtPlots(double pt, bool isME42, int lctSize);
   void ratePlotHelper(TH1* hist, int nBins, double min, double max, double val);
   void do2Lct3LctEfficiency(double eta, double phi, double pt, int lctSize, int ME4, bool isME42);
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
   TH1F* hTrackPtME42;
   TH1F* hTrackPtNonME42;

   TH1F* hTrackLCTRateME42_3of4;
   TH1F* hTrackPtRateME42_3of4;
   TH1F* hTrackPhiRatePlusEndcap_3of4;
   TH1F* hTrackPhiRateMinusEndcap_3of4;
   TH1F* hTrackPtME42_3of4;

   TH1F* h2Lct3LctEtaDenominator;
   TH1F* h2Lct3LctPhiDenominator;
   TH1F* h2Lct3LctPtDenominator;
   TH1F* h2Lct3LctEtaNumerator;
   TH1F* h2Lct3LctPhiNumerator;
   TH1F* h2Lct3LctPtNumerator;
   TH1F* h2Lct3LctEtaEfficiency;
   TH1F* h2Lct3LctPhiEfficiency;
   TH1F* h2Lct3LctPtEfficiency;
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
         if (lctSize==0) { break; }
         double trackEta = csctf_->trEta[trk];
         double trackPhi = csctf_->trPhi_02PI[trk];
         double trackPt = csctf_->trPt[trk];
         int trackEndcap = csctf_->trEndcap[trk];

         // check if track crosses ME42 region
         int outerLctEta = csctf_->trLctglobalEta[trk][lctSize-1];   // goes from 0-125 within endcap
         int outerLctPhi = csctf_->trLctglobalPhi[trk][lctSize-1];   // goes from ~50-4050 in sector
         int outerLctEndcap = csctf_->trLctEndcap[trk][lctSize-1];   // 1 or -1
         int outerLctSector = csctf_->trLctSector[trk][lctSize-1];   // 1-6 in + 7-12 in - (starts at 15 deg)
         //int outerLctSubsector = csctf_->trLctSubSector[trk][lctSize-1]; // ?? most 0 (some 1 or 2)
         //int outerLctStation = csctf_->trLctStation[trk][lctSize-1]; // 1-4
         //int outerLctRing = csctf_->trLctRing[trk][lctSize-1];       // 1-3 in station 1, 1-2 in 2-4
         //int outerLctChamber = csctf_->trLctChamber[trk][lctSize-1]; // 1-18 or 1-36 (dependent on geom)
         //int outerLctStrip = csctf_->trLctstripNum[trk][lctSize-1];  //
         //int outerLctWire = csctf_->trLctwireGroup[trk][lctSize-1];  //
         //int outerLctCSCID = csctf_->trLctTriggerCSCID[trk][lctSize-1]; //
         bool isME42 = isME42Region(outerLctEndcap,outerLctSector,outerLctEta,outerLctPhi);
         if (outerLctEta>=23 && outerLctEta<=72) {   // ME42 eta region in CSCTF coordinates
            // track chamber occupancy
            int ME1 = csctf_->trME1ID[trk];
            int ME2 = csctf_->trME2ID[trk];
            int ME3 = csctf_->trME3ID[trk];
            int ME4 = csctf_->trME4ID[trk];
            doChamberOccupancy(ME1,ME2,ME3,ME4,isME42);
            doTrackLCTRatePlots(lctSize,isME42,lctSize);
            doTrackPtPlots(trackPt,isME42,lctSize);
            doTrackPhiRatePlots(trackPhi,trackEndcap,lctSize,isME42);
            do2Lct3LctEfficiency(trackEta,trackPhi,trackPt,lctSize,ME4,isME42);
         }
      }

    } //end loop on events

   // write histo to fill
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
   hTrackPtRateME42 = new TH1F("hTrackPtRateME42","CSCTF p_{T} Rate: ME4/2 Region",8,-10,150);
   hTrackPtRateNonME42 = new TH1F("hTrackPtRateNonME42","CSCTF p_{T} Rate: Non-ME4/2 Region",8,-10,150);
   hTrackPtME42 = new TH1F("hTrackPtME42","CSCTF p_{T}: ME4/2 Region",15,0,150);
   hTrackPtNonME42 = new TH1F("hTrackPtNonME42","CSCTF p_{T}: Non-ME4/2 Region",15,0,150);
   hTrackPhiRatePlusEndcap = new TH1F("hTrackPhiRatePlusEndcap","CSCTF #phi: Plus Endcap",6,0,2*TMath::Pi());
   hTrackPhiRateMinusEndcap = new TH1F("hTrackPhiRateMinusEndcap","CSCTF #phi: Minus Endcap",6,0,2*TMath::Pi());


   hTrackLCTRateME42_3of4 = new TH1F("hTrackLCTRateME42_3of4","LCT Rate: ME4/2 Region (3 of 4 LCTs)",5,-.5,4.5);
   hTrackPtRateME42_3of4 = new TH1F("hTrackPtRateME42_3of4","CSCTF p_{T} Rate: ME4/2 Region (3 of 4 LCTs)",8,-10,150);
   hTrackPtME42_3of4 = new TH1F("hTrackPtME42_3of4","CSCTF p_{T}: ME4/2 Region (3 of 4 LCTs)",15,0,150);
   hTrackPhiRatePlusEndcap_3of4 = new TH1F("hTrackPhiRatePlusEndcap_3of4","CSCTF #phi: Plus Endcap (3 of 4 LCTs)",6,0,2*TMath::Pi());
   hTrackPhiRateMinusEndcap_3of4 = new TH1F("hTrackPhiRateMinusEndcap_3of4","CSCTF #phi: Minus Endcap (3 of 4 LCTs)",6,0,2*TMath::Pi());

   h2Lct3LctEtaNumerator = new TH1F("h2Lct3LctEtaNumerator","",10,-2.5,2.5);
   h2Lct3LctEtaDenominator = new TH1F("h2Lct3LctEtaDenominator","",10,-2.5,2.5);
   h2Lct3LctPhiNumerator = new TH1F("h2Lct3LctPhiNumerator","",6,0,2*TMath::Pi());
   h2Lct3LctPhiDenominator = new TH1F("h2Lct3LctPhiDenominator","",6,0,2*TMath::Pi());
   h2Lct3LctPtNumerator = new TH1F("h2Lct3LctPtNumerator","",15,0,150);
   h2Lct3LctPtDenominator = new TH1F("h2Lct3LctPtDenominator","",15,0,150);

   hTrackLCTRateME42->GetXaxis()->SetTitle("Matched Stations");
   hTrackLCTRateME42->GetYaxis()->SetTitle("Tracks");
   hTrackLCTRateME42->SetMinimum(0);
   hTrackLCTRateME42_3of4->GetXaxis()->SetTitle("Matched Stations");
   hTrackLCTRateME42_3of4->GetYaxis()->SetTitle("Tracks");
   hTrackLCTRateME42_3of4->SetMinimum(0);
   hTrackLCTRateNonME42->GetXaxis()->SetTitle("Matched Stations");
   hTrackLCTRateNonME42->GetXaxis()->SetTitle("Matched Stations");
   hTrackLCTRateNonME42->GetYaxis()->SetTitle("Tracks");
   hTrackLCTRateNonME42->SetMinimum(0);

   hTrackPtRateME42->GetXaxis()->SetTitle("p_{T} (GeV/c)");
   hTrackPtRateME42->GetYaxis()->SetTitle("Tracks");
   hTrackPtRateME42_3of4->GetXaxis()->SetTitle("p_{T} (GeV/c)");
   hTrackPtRateME42_3of4->GetYaxis()->SetTitle("Tracks");
   hTrackPtRateNonME42->GetXaxis()->SetTitle("p_{T} (GeV/c)");
   hTrackPtRateNonME42->GetXaxis()->SetTitle("p_{T} (GeV/c)");
   hTrackPtRateNonME42->GetYaxis()->SetTitle("Tracks");

   hTrackPtME42->GetXaxis()->SetTitle("p_{T} (GeV/c)");
   hTrackPtME42->GetYaxis()->SetTitle("Tracks");
   hTrackPtME42_3of4->GetXaxis()->SetTitle("p_{T} (GeV/c)");
   hTrackPtME42_3of4->GetYaxis()->SetTitle("Tracks");
   hTrackPtNonME42->GetXaxis()->SetTitle("p_{T} (GeV/c)");
   hTrackPtNonME42->GetXaxis()->SetTitle("p_{T} (GeV/c)");
   hTrackPtNonME42->GetYaxis()->SetTitle("Tracks");

   hTrackPhiRatePlusEndcap->GetXaxis()->SetTitle("#phi (rad)");
   hTrackPhiRatePlusEndcap->GetYaxis()->SetTitle("Tracks");
   hTrackPhiRatePlusEndcap->SetMinimum(0);
   hTrackPhiRateMinusEndcap->GetXaxis()->SetTitle("#phi (rad)");
   hTrackPhiRateMinusEndcap->GetYaxis()->SetTitle("Tracks");
   hTrackPhiRateMinusEndcap->SetMinimum(0);
   hTrackPhiRatePlusEndcap_3of4->GetXaxis()->SetTitle("#phi (rad)");
   hTrackPhiRatePlusEndcap_3of4->GetYaxis()->SetTitle("Tracks");
   hTrackPhiRatePlusEndcap_3of4->SetMinimum(0);
   hTrackPhiRateMinusEndcap_3of4->GetXaxis()->SetTitle("#phi (rad)");
   hTrackPhiRateMinusEndcap_3of4->GetYaxis()->SetTitle("Tracks");
   hTrackPhiRateMinusEndcap_3of4->SetMinimum(0);
}

void L1CSCTFAnalysis::end() {
   // things to do after run
   
   // normalize rate plots to first bin
   //hTrackLCTRateME42->Scale(1./hTrackLCTRateME42->GetBinContent(1));
   //hTrackLCTRateNonME42->Scale(1./hTrackLCTRateNonME42->GetBinContent(1));
   //hTrackPtRateME42->Scale(1./hTrackPtRateME42->GetBinContent(1));
   //hTrackPtRateNonME42->Scale(1./hTrackPtRateNonME42->GetBinContent(1));

   // make efficiencies
   h2Lct3LctEtaEfficiency = (TH1F*)h2Lct3LctEtaNumerator->Clone("h2Lct3LctEtaEfficiency");
   h2Lct3LctPhiEfficiency = (TH1F*)h2Lct3LctPhiNumerator->Clone("h2Lct3LctPhiEfficiency");
   h2Lct3LctPtEfficiency = (TH1F*)h2Lct3LctPtNumerator->Clone("h2Lct3LctPtEfficiency");
   h2Lct3LctEtaEfficiency->Divide(h2Lct3LctEtaDenominator);
   h2Lct3LctPhiEfficiency->Divide(h2Lct3LctPhiDenominator);
   h2Lct3LctPtEfficiency->Divide(h2Lct3LctPtDenominator);
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

void L1CSCTFAnalysis::doTrackLCTRatePlots(int size, bool isME42, int lctSize) {
   if (isME42) { 
      ratePlotHelper(hTrackLCTRateME42,5,0,4,size); 
      if (lctSize>=3) { ratePlotHelper(hTrackLCTRateME42_3of4,5,0,4,size); } 
   }
   else { ratePlotHelper(hTrackLCTRateNonME42,5,0,4,size); }
}

void L1CSCTFAnalysis::doTrackPtPlots(double pt, bool isME42, int lctSize) {
   if (isME42) { 
      hTrackPtME42->Fill(pt);
      ratePlotHelper(hTrackPtRateME42,8,0,140,pt); 
      if (lctSize>=3) {
         hTrackPtME42_3of4->Fill(pt);
         ratePlotHelper(hTrackPtRateME42_3of4,8,0,140,pt); 
      }
   }
   else { 
      hTrackPtNonME42->Fill(pt);
      ratePlotHelper(hTrackPtRateNonME42,8,0,140,pt); 
   }
}

void L1CSCTFAnalysis::ratePlotHelper(TH1* hist, int nBins, double min, double max, double val) {
   double binWidth = (max-min)/(nBins-1);
   for (int n=0; n<nBins; n++) {
      if (val>=(min+n*binWidth)) { hist->Fill(min+n*binWidth); }
   }
}

void L1CSCTFAnalysis::doTrackPhiRatePlots(double phi, int endcap, int lctSize, bool isME42) {
   if (endcap==1) { 
      hTrackPhiRatePlusEndcap->Fill(phi); 
      if (lctSize>=3 && isME42) { hTrackPhiRatePlusEndcap_3of4->Fill(phi); }
      else if (!isME42) { hTrackPhiRatePlusEndcap_3of4->Fill(phi); }
   }
   else { 
      hTrackPhiRateMinusEndcap->Fill(phi);
      hTrackPhiRateMinusEndcap_3of4->Fill(phi); 
   }
}

void L1CSCTFAnalysis::do2Lct3LctEfficiency(double eta, double phi, double pt, int lctSize, int ME4, bool isME42) {
   int oldLctSize = lctSize;
   if (ME4) { oldLctSize--; }
   if (isME42 && oldLctSize >= 2) { 
      h2Lct3LctPhiDenominator->Fill(phi);
      h2Lct3LctEtaDenominator->Fill(eta);
      h2Lct3LctPtDenominator->Fill(pt);
      if (lctSize >= 3) {
         h2Lct3LctPhiNumerator->Fill(phi);
         h2Lct3LctEtaNumerator->Fill(eta);
         h2Lct3LctPtNumerator->Fill(pt);
      }      
   }
}
