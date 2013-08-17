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
   hists["hitPatternME42"] = fileService->make<TH1F>("hitPatternME42","Station Hit Pattern in ME4/2 Region",31,.5,31.5);
   hists["hitPatternNonME42"] = fileService->make<TH1F>("hitPatternNonME42","Station Hit Pattern in Non-ME4/2 Region",31,.5,31.5);
   hists["ptME42"] = fileService->make<TH1F>("ptME42","p_{T} in ME4/2 Region",50,0,200);
   hists["ptNonME42"] = fileService->make<TH1F>("ptNonME42","p_{T} in Non-ME4/2 Region",50,0,200);
}


CSCPerformance::~CSCPerformance()
{
   // station hit pattern labels
   const int numLabels = 31;
   const char *hitPatternLabel[numLabels] = {"None","","ME1","","ME2","","ME3","","ME4","","ME1/ME2","","ME1/ME3","","ME1/ME4","","ME2/ME3","","ME2/ME4","","ME3/ME4","","ME1/ME2/ME3","","ME1/ME2/ME4","","ME1/ME3/ME4","","ME2/ME3/ME4","","ME1/ME2/ME3/ME4"};
   for (int i=1;i<=numLabels;i++) hists["hitPatternME42"]->GetXaxis()->SetBinLabel(i,hitPatternLabel[i-1]);
   for (int i=1;i<=numLabels;i++) hists["hitPatternNonME42"]->GetXaxis()->SetBinLabel(i,hitPatternLabel[i-1]);

   hists["numChambersME42"]->GetXaxis()->SetTitle("Number of stations in track");
   hists["numChambersNonME42"]->GetXaxis()->SetTitle("Number of stations in track");
   hists["ptME42"]->GetXaxis()->SetTitle("p_{T} (GeV/c)");
   hists["ptNonME42"]->GetXaxis()->SetTitle("p_{T} (GeV/c)");
}


//
// member functions
//

// ------------ method called for each event  ------------
void
CSCPerformance::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;

   // get event parameters
   Handle<CSCRecHit2DCollection> recHits;
   Handle<CSCSegmentCollection> cscSegments;
   Handle<reco::TrackCollection> saMuons;
   Handle<reco::MuonCollection> allMuons;
   iEvent.getByLabel(cscRecHitTag,recHits);
   iEvent.getByLabel(cscSegmentTag, cscSegments);
   iEvent.getByLabel(saMuonTag,saMuons);
   iEvent.getByLabel(allMuonsTag,allMuons);

   // get setup parameters
//   ESHandle<CSCGeometry> theGeometry;
//   iSetup.get<MuonGeometryRecord>().get(theGeometry);  

   // plot number of chambers in each muon for ME4/2 region
   plotMatchedChambers(allMuons);//,theGeometry); 
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
CSCPerformance::plotMatchedChambers(edm::Handle<reco::MuonCollection> muons)//, edm::ESHandle<CSCGeometry> geometry)
{
   // ME+4/2 region
   // eta = [1.2,1.8], phi = [1.396,2.269]
   double etaMin = 1.2;
   double etaMax = 1.7;
   double phiMin = 1.4;
   double phiMax = 2.25;
   double outPhiMin = 1.2;
   double outPhiMax = 2.45;

   // Get list of detector ids for ME42
//   std::vector<int> ME42DetId;
//   std::vector<GlobalPoint> ME42CenterGlobalPoint;
//   CSCGeometry::DetUnitContainer theDetUnits = geometry->detUnits();
//   for (CSCGeometry::DetUnitContainer::const_iterator geomUnit = theDetUnits.begin(); geomUnit != theDetUnits.end(); ++geomUnit)
//   {
//      CSCLayer* layer = dynamic_cast<CSCLayer*>(*geomUnit);
//      if (layer) {
//         DetId detId = layer->geographicalId();
//         int id = detId();
//         // check to see if we have a ME42
//         if (CSCDetId::endcap(id)==2 && CSCDetId::station(id)==4 && CSCDetId::ring(id)==2 && CSCDetId::layer(id)==0) { 
//            std::cout << "The ME42 detectors are: " << std::endl;
//            outputDetID(detId);
//            ME42DetId.push_back(id);
//            LocalPoint localCenter(0.,0.,0.);
//            ME42CenterGlobalPoint.push_back(layer->toGlobal(localCenter));
//         }
//      }
//   }
//
   for (reco::MuonCollection::const_iterator muon = muons->begin(); muon != muons->end(); ++muon)
   {
      if (muon->isGlobalMuon()) {
         reco::TrackRef track = muon->outerTrack();

         // Get track hit pattern global point
//         GlobalPoint outerTrackHit(track->outerX(),track->outerY(),track->outerZ());
         // Get global point for ME42
         // convert track global point to having same x coordinate
         // iterate over chambers and get local point for each chamber from modified global point
         // if in any chamber, ME42=true
         // perform cut in outerEta and outerPhi
         // make histograms

         bool ME42 = (track->outerEta()>etaMin && track->outerEta()<etaMax && track->outerPhi()>phiMin && track->outerPhi()<phiMax);
         bool nonME42 = (TMath::Abs(track->outerEta())>etaMin && TMath::Abs(track->outerEta())<etaMax && (track->outerPhi()<outPhiMin || track->outerPhi()>outPhiMax));
         if (ME42) {
            hists["numChambersME42"]->Fill(numberOfMatchedCSCStations(*muon));
            hists["hitPatternME42"]->Fill(getHitPattern(*muon));
            hists["ptME42"]->Fill(muon->pt());
         }
         else if (nonME42) {
            hists["numChambersNonME42"]->Fill(numberOfMatchedCSCStations(*muon));
            hists["hitPatternNonME42"]->Fill(getHitPattern(*muon));
            hists["ptNonME42"]->Fill(muon->pt());
            if (numberOfMatchedCSCStations(*muon)==4) {
               std::cout << "4 in non-ME4/2" << std::endl;
               outputDetID(*muon);
               std::cout << "outer DetId: ";
               outputDetID(track->outerDetId());
               std::cout << "phi: " << track->outerPhi() << " eta: " << track->outerEta() << std::endl;
            }
         } 
      }
   }   
}

// Method to output muon detector ID for all segments in a muon track
void
CSCPerformance::outputDetID(reco::Muon muon)
{
   for (std::vector<reco::MuonChamberMatch>::const_iterator chamber = muon.matches().begin(); chamber != muon.matches().end(); ++chamber)
   {
        outputDetID(chamber->id);
   }
}

// method to output the subdetector id for a given DetId
void
CSCPerformance::outputDetID(DetId id)
{
   DetId::Detector det = id.det();
   int subdet = id.subdetId();
   if (det==2 && subdet==1) {
      std::cout << (DTChamberId)id << std::endl;
   }
   else if (det==2 && subdet==2) {
      std::cout << (CSCDetId)id << std::endl;
   }
   else if (det==2 && subdet==3) {
      std::cout << (RPCDetId)id << std::endl;
   }
}

// Method to see if the track has a chamber in the station
bool
CSCPerformance::hasChamber(reco::Muon muon, int station)
{
   for (std::vector<reco::MuonChamberMatch>::const_iterator chamber = muon.matches().begin(); chamber != muon.matches().end(); ++chamber)
   {
        DetId::Detector det = chamber->id.det();
        int subdet = chamber->id.subdetId();
        if (det==2 && subdet==2) {
           if (((CSCDetId)(chamber->id)).station() == station) {
              return true;
           }
        }
   }
   return false;
}

// method to find the number of matched CSC stations (like numberOfMatchedStations() but excluding DT)
int
CSCPerformance::numberOfMatchedCSCStations(reco::Muon muon)
{
   int num = 0;
   if (hasChamber(muon,1)) { num += 1; }
   if (hasChamber(muon,2)) { num += 1; }
   if (hasChamber(muon,3)) { num += 1; }
   if (hasChamber(muon,4)) { num += 1; }
   return num;
}

// method to extra an integer value for plotting chamber hit pattern (numbers are odd)
int
CSCPerformance::getHitPattern(reco::Muon muon)
{
   if (numberOfMatchedCSCStations(muon)==0) { return 1; }
   if (numberOfMatchedCSCStations(muon)==1) {
      if (hasChamber(muon,1)) { return 3; }
      if (hasChamber(muon,2)) { return 5; }
      if (hasChamber(muon,3)) { return 7; }
      if (hasChamber(muon,4)) { return 9; }
   }
   if (numberOfMatchedCSCStations(muon)==2) {
      if (hasChamber(muon,1) && hasChamber(muon,2)) { return 11; }
      if (hasChamber(muon,1) && hasChamber(muon,3)) { return 13; }
      if (hasChamber(muon,1) && hasChamber(muon,4)) { return 15; }
      if (hasChamber(muon,2) && hasChamber(muon,3)) { return 17; }
      if (hasChamber(muon,2) && hasChamber(muon,4)) { return 19; }
      if (hasChamber(muon,3) && hasChamber(muon,4)) { return 21; }
   }
   if (numberOfMatchedCSCStations(muon)==3) {
      if (!hasChamber(muon,4)) { return 23; }
      if (!hasChamber(muon,3)) { return 25; }
      if (!hasChamber(muon,2)) { return 27; }
      if (!hasChamber(muon,1)) { return 29; }
   }
   if (numberOfMatchedCSCStations(muon)==4) { return 31; }
   return -1;
}

bool
CSCPerformance::isME42Region(L1CSCTrack track)
{
   return 0;
}

//define this as a plug-in
DEFINE_FWK_MODULE(CSCPerformance);
