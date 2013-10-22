#include "CSCDetectorStudies/L1CSCTFMethods/interface/L1CSCTFMethods.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

#include "TROOT.h"
#include "TTree.h"
#include "TFile.h"


//
// constructors and destructor
//
L1CSCTFMethods::L1CSCTFMethods(const edm::ParameterSet& pset, TFileDirectory& fs): 
  edm::BasicAnalyzer::BasicAnalyzer(pset, fs),
  muons_(pset.getParameter<edm::InputTag>("muons"))
{
   //now do what ever initialization is needed

   hists_["pt"]     = fs.make<TH1F>("muonPt","pt",100,0,300);
   hists_["eta"]    = fs.make<TH1F>("muonEta","eta",100,-2.5,2.5);
   hists_["phi"]    = fs.make<TH1F>("muonPhi","phi",100,-4,4);
   hists_["charge"] = fs.make<TH1F>("muonCharge","charge",100,-2,2);
   hists_["l1pt"]   = fs.make<TH1F>("muonL1pt","l1pt",100,0,150);
   hists_["l1q"]    = fs.make<TH1F>("muonL1q","l1q",100,0,10);
   hists_["lidr"]   = fs.make<TH1F>("muonL1dr","l1dr",100,0,10);
   
}


L1CSCTFMethods::~L1CSCTFMethods()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
L1CSCTFMethods::analyze(const edm::Event& event)
{
   using namespace edm;

   using pat::Muon;

   edm::Handle<std::vector<Muon>> muons;
   event.getByLabel(muons_, muons);

   for(std::vector<Muon>::const_iterator mu1=muons->begin(); mu1!=muons->end(); ++mu1){
      hists_["pt"]->Fill(mu1->pt());
      hists_["eta"]->Fill(mu1->eta());
      hists_["phi"]->Fill(mu1->phi());
      hists_["charge"]->Fill(mu1->charge());
      hists_["l1pt"]->Fill((mu1->userCand("muonL1Info"))->pt()); 
      hists_["l1q"]->Fill(mu1->userInt("muonL1Info:quality"));
      hists_["l1dr"]->Fill(mu1->userFloat("muonL1Info:deltaR"));
   }
}


// ------------ method called once each job just before starting event loop  ------------
void 
L1CSCTFMethods::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
L1CSCTFMethods::endJob() 
{
}

