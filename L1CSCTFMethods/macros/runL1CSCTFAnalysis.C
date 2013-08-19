{
gROOT->ProcessLine(".x UserCode/L1TriggerDPG/macros/initL1Analysis.C");
gROOT->ProcessLine(".L UserCode/L1TriggerDPG/macros/Style.C");
gROOT->ProcessLine("setTDRStyle()");
gROOT->ProcessLine("gROOT->ForceStyle()");
gROOT->ProcessLine(".L CSCDetectorStudies/L1CSCTFMethods/macros/L1CSCTFAnalysis.C+");

L1CSCTFAnalysis t;
t.OpenWithList("CSCDetectorStudies/L1CSCTFMethods/macros/listOfFiles.txt");

// run over a 1000 events
t.run(10000);

// to run over all events
//t.run(-1);

}

