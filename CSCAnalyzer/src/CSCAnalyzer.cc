#include "CSCDetectorStudies/CSCAnalyzer/interface/CSCAnalyzer.h"

//
// constructors and destructor
//
CSCAnalyzer::CSCAnalyzer(const edm::ParameterSet& iConfig)

{
   //now do what ever initialization is needed
   stripDigiTag  = iConfig.getParameter<edm::InputTag>("stripDigiTag");
   wireDigiTag   = iConfig.getParameter<edm::InputTag>("wireDigiTag");
   compDigiTag   = iConfig.getParameter<edm::InputTag>("compDigiTag");
   alctDigiTag   = iConfig.getParameter<edm::InputTag>("alctDigiTag") ;
   clctDigiTag   = iConfig.getParameter<edm::InputTag>("clctDigiTag") ;
   corrlctDigiTag= iConfig.getParameter<edm::InputTag>("corrlctDigiTag") ;
   cscRecHitTag  = iConfig.getParameter<edm::InputTag>("cscRecHitTag");
   cscSegTag     = iConfig.getParameter<edm::InputTag>("cscSegTag");
   saMuonTag     = iConfig.getParameter<edm::InputTag>("saMuonTag");
   l1aTag        = iConfig.getParameter<edm::InputTag>("l1aTag");
   hltTag        = iConfig.getParameter<edm::InputTag>("hltTag");

}


CSCAnalyzer::~CSCAnalyzer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
CSCAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;

   // Get the Digis
   edm::Handle<CSCWireDigiCollection> wires;
   edm::Handle<CSCStripDigiCollection> strips;
   edm::Handle<CSCComparatorDigiCollection> compars;
   edm::Handle<CSCALCTDigiCollection> alcts;
   edm::Handle<CSCCLCTDigiCollection> clcts;
   edm::Handle<CSCCorrelatedLCTDigiCollection> correlatedlcts;
   iEvent.getByLabel(stripDigiTag,strips);
   iEvent.getByLabel(wireDigiTag,wires);
   iEvent.getByLabel(compDigiTag,compars);
   iEvent.getByLabel(alctDigiTag, alcts);
   iEvent.getByLabel(clctDigiTag, clcts);
   iEvent.getByLabel(corrlctDigiTag, correlatedlcts);

   // Get the CSC Geometry :
   ESHandle<CSCGeometry> cscGeom;
   iSetup.get<MuonGeometryRecord>().get(cscGeom);

   // Get the RecHits collection :
   Handle<CSCRecHit2DCollection> recHits;
   iEvent.getByLabel(cscRecHitTag,recHits);

   // get CSC segment collection
   Handle<CSCSegmentCollection> cscSegments;
   iEvent.getByLabel(cscSegTag, cscSegments);

   // get the trigger collection
   edm::Handle<L1MuGMTReadoutCollection> pCollection;
   iEvent.getByLabel(l1aTag,pCollection);

   edm::Handle<TriggerResults> hlt;
   iEvent.getByLabel(hltTag,hlt);

   // get the standalone muon collection
   Handle<reco::TrackCollection> saMuons;
   iEvent.getByLabel(saMuonTag,saMuons);
}


// ------------ method called once each job just before starting event loop  ------------
void 
CSCAnalyzer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
CSCAnalyzer::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
void 
CSCAnalyzer::beginRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a run  ------------
void 
CSCAnalyzer::endRun(edm::Run const&, edm::EventSetup const&)
{
}

// ------------ method called when starting to processes a luminosity block  ------------
void 
CSCAnalyzer::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method called when ending the processing of a luminosity block  ------------
void 
CSCAnalyzer::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
CSCAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(CSCAnalyzer);
