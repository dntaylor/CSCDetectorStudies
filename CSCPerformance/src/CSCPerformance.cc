#include "CSCDetectorStudies/CSCPerformance/interface/CSCPerformance.h"

//
// static data member definitions
//

//
// constructors and destructor
//
CSCPerformance::CSCPerformance(const edm::ParameterSet& iConfig)

{
   // get input tags
   cscRecHitTag  = iConfig.getParameter<edm::InputTag>("cscRecHitTag");
   cscSegmentTag = iConfig.getParameter<edm::InputTag>("cscSegmentTag");
   saMuonTag     = iConfig.getParameter<edm::InputTag>("saMuonTag");
   allMuonsTag   = iConfig.getParameter<edm::InputTag>("allMuonsTag");
   
   edm::Service<TFileService> fileService;

   hists["numChambersME42"] = fileService->make<TH1F>("numChambersME42","Number of Matched Stations in ME4/2 Region",6,-0.5,5.5);
   hists["numChambersNonME42"] = fileService->make<TH1F>("numChambersNonME42","Number of Matched Stations in Non-ME4/2 Region",6,-0.5,5.5);
}


CSCPerformance::~CSCPerformance()
{
   // normalize histograms
   hists["numChambersME42"]->Scale(1.0/hists["numChambersME42"]->Integral());
   hists["numChambersNonME42"]->Scale(1.0/hists["numChambersNonME42"]->Integral());

}


//
// member functions
//

// ------------ method called for each event  ------------
void
CSCPerformance::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;

   // get parameters
   Handle<CSCRecHit2DCollection> recHits;
   Handle<CSCSegmentCollection> cscSegments;
   Handle<reco::TrackCollection> saMuons;
   Handle<reco::MuonCollection> allMuons;
   iEvent.getByLabel(cscRecHitTag,recHits);
   iEvent.getByLabel(cscSegmentTag, cscSegments);
   iEvent.getByLabel(saMuonTag,saMuons);
   iEvent.getByLabel(allMuonsTag,allMuons);

   // plot number of chambers in each muon for ME4/2 region
   plotMatchedChambers(allMuons); 
}


// ------------ method called once each job just before starting event loop  ------------
void 
CSCPerformance::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
CSCPerformance::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
void 
CSCPerformance::beginRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
CSCPerformance::endRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
CSCPerformance::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
CSCPerformance::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
CSCPerformance::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

// method to plot number of muons v number of matched chambers in a given region
void
CSCPerformance::plotMatchedChambers(edm::Handle<reco::MuonCollection> muons)
{
   // ME+4/2 region
   // eta = [1.2,1.8], phi = [1.396,2.269]
   
   for (reco::MuonCollection::const_iterator muon = muons->begin(); muon != muons->end(); ++muon)
   {
      // select ME4/2 region
      if (muon->eta()>1.2 && muon->eta()< 1.8 && muon->phi()>1.396 && muon->phi()<2.269) {
         hists["numChambersME42"]->Fill(muon->numberOfMatchedStations());
         if (muon->numberOfMatchedStations()==5) {
            std::cout << "5 matched stations in ME4/2 region" << std::endl;
            outputDetID(*muon);
         }
      }
      else if (TMath::Abs(muon->eta())>1.2 && TMath::Abs(muon->eta())<1.8) {
         hists["numChambersNonME42"]->Fill(muon->numberOfMatchedStations());
         if (muon->numberOfMatchedStations()==4) {
            std::cout << "4 matched stations in non-ME4/2 region" << std::endl;
            outputDetID(*muon);
         }
      }
   }   
}

// Method to output csc detector ID for all segments in a muon track
void
CSCPerformance::outputDetID(reco::Muon muon)
{
   for (std::vector<reco::MuonChamberMatch>::const_iterator chamber = muon.matches().begin(); chamber != muon.matches().end(); ++chamber)
   {
      std::cout << "   " << chamber->detector() << " " << chamber->station() << std::endl;
   }
}


//define this as a plug-in
DEFINE_FWK_MODULE(CSCPerformance);
