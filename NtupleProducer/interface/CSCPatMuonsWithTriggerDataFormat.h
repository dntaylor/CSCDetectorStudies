

#ifndef __CSCANALYSIS_CSCPATMUONSWITHTRIGGERDATAFORMAT_H__
#define __CSCANALYSIS_CSCPATMUONSWITHTRIGGERDATAFORMAT_H__

#include <TROOT.h>
#include <vector>
#include <iostream>

namespace CSCAnalysis
{
  struct CSCPatMuonsWithTriggerDataFormat
  {
    CSCPatMuonsWithTriggerDataFormat() {Reset();}
    ~CSCPatMuonsWithTriggerDataFormat() {}
 
    void Reset()
    {
       muonSize = 0;

       muPt.clear();
       muEta.clear();
       muPhi.clear();
       muCharge.clear();

       muL1pt.clear();
       muL1dr.clear();
       muL1q.clear();

       muCSCStation.clear();
       muCSCRing.clear();
    }

    int muonSize;
    
    // reco info
    std::vector<float> muPt;
    std::vector<float> muEta;
    std::vector<float> muPhi;
    std::vector<int> muCharge;

    // muon definitions
    std::vector<bool> muGlobalMuon;
    std::vector<bool> muTrackerMuon;
    std::vector<bool> muCaloMuon;
    std::vector<bool> muStandAloneMuon;
    std::vector<bool> muPFMuon;

    // chamber matching
    std::vector<int> muNumberOfMatchedStations;
    std::vector<int> muNumberOfChambers;
 
    // trigger info
    std::vector<float> muL1pt;
    std::vector<float> muL1dr;
    std::vector<int> muL1q;

    // track info
    std::vector<float> muOuterPt;
    std::vector<float> muOuterEta;
    std::vector<float> muOuterPhi;

    // hit pattern
    std::vector< std::vector<int> > muCSCStation;
    std::vector< std::vector<int> > muCSCRing;
  };
}


#endif
