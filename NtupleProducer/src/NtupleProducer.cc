

#include "CSCDetectorStudies/NtupleProducer/interface/NtupleProducer.h"

#include <iostream>
#include <iomanip>
#include <vector>
#include <cmath>

#include "TROOT.h"
#include "TTree.h"
#include "TFile.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Framework/interface/MakerMacros.h"

// Constructor
NtupleProducer::NtupleProducer(const edm::ParameterSet& ps) : tree_(0) {

   muons_ = ps.getParameter<edm::InputTag>("muons");

   cscPMWT = new CSCAnalysis::CSCPatMuonsWithTrigger();
   cscPMWT_data = cscPMWT->getData();

   tree_ = tfs_->make<TTree>("RecoTree", "RecoTree");
   tree_->Branch("PatMuonsWithTrigger", "CSCAnalysis::CSCPatMuonsWithTriggerDataFormat", &cscPMWT_data, 32000, 3);

}

NtupleProducer::~NtupleProducer() {
   
   delete cscPMWT;

}

void NtupleProducer::beginJob(void) {
}

void NtupleProducer::endJob() {
}

void NtupleProducer::analyze(const edm::Event& e, const edm::EventSetup& es) {

   cscPMWT->Reset();
   cscPMWT->Set(e,muons_); 
   tree_->Fill();

}

DEFINE_FWK_MODULE( NtupleProducer );
