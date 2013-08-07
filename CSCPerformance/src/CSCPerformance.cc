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
}


CSCPerformance::~CSCPerformance()
{
   // normalize histograms
   hists["numChambersME42"]->Scale(1.0/hists["numChambersME42"]->Integral());
   hists["numChambersNonME42"]->Scale(1.0/hists["numChambersNonME42"]->Integral());

   // station hit pattern labels
   const int numLabels = 31;
   const char *hitPatternLabel[numLabels] = {"None","","ME1","","ME2","","ME3","","ME4","","ME1/ME2","","ME1/ME3","","ME1/ME4","","ME2/ME3","","ME2/ME4","","ME3/ME4","","ME1/ME2/ME3","","ME1/ME2/ME4","","ME1/ME3/ME4","","ME2/ME3/ME4","","ME1/ME2/ME3/ME4"};
   for (int i=1;i<=numLabels;i++) hists["hitPatternME42"]->GetXaxis()->SetBinLabel(i,hitPatternLabel[i-1]);
   for (int i=1;i<=numLabels;i++) hists["hitPatternNonME42"]->GetXaxis()->SetBinLabel(i,hitPatternLabel[i-1]);
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
   plotMatchedChambers(allMuons,saMuons); 
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
CSCPerformance::plotMatchedChambers(edm::Handle<reco::MuonCollection> muons, edm::Handle<reco::TrackCollection> tracks)
{
   // ME+4/2 region
   // eta = [1.2,1.8], phi = [1.396,2.269]
   double etaMin = 1.2;
   double etaMax = 1.6;
   double phiMin = 1.4;
   double phiMax = 2.25;
   double outPhiMin = 1.2;
   double outPhiMax = 2.5;

   for (reco::MuonCollection::const_iterator muon = muons->begin(); muon != muons->end(); ++muon)
   {
      bool ME42 = (muon->eta()>etaMin && muon->eta()<etaMax && muon->phi()>phiMin && muon->phi()<phiMax);
      bool nonME42 = (TMath::Abs(muon->eta())>etaMin && TMath::Abs(muon->eta())<etaMax && (muon->phi()<outPhiMin || muon->phi()>outPhiMax));
      // select ME4/2 region
      if (ME42) {
         hists["numChambersME42"]->Fill(numberOfMatchedCSCStations(*muon));
         hists["hitPatternME42"]->Fill(getHitPattern(*muon));
      }
      else if (nonME42) {
         hists["numChambersNonME42"]->Fill(numberOfMatchedCSCStations(*muon));
         hists["hitPatternNonME42"]->Fill(getHitPattern(*muon));
//         if (numberOfMatchedCSCStations(*muon)==4) {
//            std::cout << "---------------" << std::endl << "4 in non-ME42" << std::endl;
//            outputDetID(*muon);
//            std::cout << "phi: " << muon->phi() << " eta: " << muon->eta() << std::endl;
//         }
      } 
   }   
   for (reco::TrackCollection::const_iterator track = tracks->begin(); track != tracks->end(); ++track)
   {
      bool ME42 = (track->outerEta()>etaMin && track->outerEta()<etaMax && track->outerPhi()>phiMin && track->outerPhi()<phiMax);
      bool nonME42 = (TMath::Abs(track->outerEta())>etaMin && TMath::Abs(track->outerEta())<etaMax && (track->outerPhi()<outPhiMin || track->outerPhi()>outPhiMax));
      if (ME42) {
         std::cout << "---------------" << std::endl;
         DetId theId = new DetId(track->outerDetId());
         std::cout << "DetID: " << (CSCDetId)(theId.id) << std::endl;
         std::cout << "outerPhi: " << track->outerPhi() << " outerEta: " << track->outerEta() << std::endl;
      }
      else if (nonME42) {

      }
   }
}

// Method to output csc detector ID for all segments in a muon track
void
CSCPerformance::outputDetID(reco::Muon muon)
{
   for (std::vector<reco::MuonChamberMatch>::const_iterator chamber = muon.matches().begin(); chamber != muon.matches().end(); ++chamber)
   {
        DetId::Detector det = chamber->id.det();
        int subdet = chamber->id.subdetId();
        if (det==2 && subdet==1) {
           std::cout << (DTChamberId)(chamber->id) << std::endl;
        }
        else if (det==2 && subdet==2) {
           std::cout << (CSCDetId)(chamber->id) << std::endl;
        }
        else if (det==2 && subdet==3) {
//           std::cout << (RPCDetId)(chamber->id) << std::endl;
        }
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

//define this as a plug-in
DEFINE_FWK_MODULE(CSCPerformance);
