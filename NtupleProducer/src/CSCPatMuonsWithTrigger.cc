#include "CSCDetectorStudies/NtupleProducer/interface/CSCPatMuonsWithTrigger.h"

#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/TrackReco/interface/HitPattern.h"

CSCAnalysis::CSCPatMuonsWithTrigger::CSCPatMuonsWithTrigger() 
{
}

CSCAnalysis::CSCPatMuonsWithTrigger::~CSCPatMuonsWithTrigger() 
{
}

void CSCAnalysis::CSCPatMuonsWithTrigger::Set(const edm::Event& e, const edm::InputTag& muons_) 
{
   using pat::Muon;

   edm::Handle<std::vector<Muon>> muons;
   e.getByLabel(muons_,muons);

   pmwt_.muonSize = muons->size();

   for(std::vector<Muon>::const_iterator mu1=muons->begin(); mu1!=muons->end(); ++mu1){
      // muon information
      pmwt_.muPt.push_back(mu1->pt());
      pmwt_.muEta.push_back(mu1->eta());
      pmwt_.muPhi.push_back(mu1->phi());
      pmwt_.muCharge.push_back(mu1->charge());

      // muon type
      pmwt_.muGlobalMuon.push_back(mu1->isGlobalMuon());
      pmwt_.muTrackerMuon.push_back(mu1->isTrackerMuon());
      pmwt_.muCaloMuon.push_back(mu1->isCaloMuon());
      pmwt_.muStandAloneMuon.push_back(mu1->isStandAloneMuon());
      pmwt_.muPFMuon.push_back(mu1->isPFMuon());

      // muon matched chambers
      pmwt_.muNumberOfMatchedStations.push_back(mu1->numberOfMatchedStations());
      pmwt_.muNumberOfChambers.push_back(mu1->numberOfChambers());

      // trigger information
      pmwt_.muL1pt.push_back((mu1->userCand("muonL1Info")).isNonnull() ? (mu1->userCand("muonL1Info"))->pt() : 0);
      pmwt_.muL1q.push_back(mu1->userInt("muonL1Info:quality"));
      pmwt_.muL1dr.push_back(mu1->userFloat("muonL1Info:deltaR"));

      if (!mu1->outerTrack().isNull()) {
         // track variables
         pmwt_.muOuterPt.push_back(mu1->outerTrack()->outerPt());
         pmwt_.muOuterEta.push_back(mu1->outerTrack()->outerEta());
         pmwt_.muOuterPhi.push_back(mu1->outerTrack()->outerPhi());

         // hitpattern information
         reco::HitPattern hp = mu1->outerTrack()->hitPattern();
         std::vector<int> cscStation, cscRing;
         for (int hit=0; hit<hp.numberOfValidHits(); hit++) {
            uint32_t p = hp.getHitPattern(hit);
            if (hp.muonCSCHitFilter(p)) {
               cscStation.push_back(hp.getMuonStation(p));
               cscRing.push_back(hp.getCSCRing(p));
            }
         }
         pmwt_.muCSCStation.push_back(cscStation);
         pmwt_.muCSCRing.push_back(cscRing);
      }
   }

}
