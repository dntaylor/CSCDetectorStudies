void plot()
{
   TFile* Plots = new TFile("plots.root","RECREATE");
   TFile ME42("ME42TagAndProbeTreeAnalysisME42.root");
   TFile NoME42("ME42TagAndProbeTreeAnalysisNoME42.root");
   TFile ME42Eta("ME42TagAndProbeTreeAnalysisME42Eta.root");
   TFile NoME42Eta("ME42TagAndProbeTreeAnalysisNoME42Eta.root");
   TFile ME42Phi("ME42TagAndProbeTreeAnalysisME42Phi.root");
   TFile NoME42Phi("ME42TagAndProbeTreeAnalysisNoME42Phi.root");

   TH1F* hME42EtaLoose = (TH1F*)ME42Phi.Get("loose_eta.fit_eff_plots.eta_PLOT");
   TH1F* hME42EtaTight = (TH1F*)ME42Phi.Get("tight_eta.fit_eff_plots.eta_PLOT");
   TH1F* hNoME42EtaLoose = (TH1F*)NoME42Phi.Get("loose_eta.fit_eff_plots.eta_PLOT");
   TH1F* hNoME42EtaTight = (TH1F*)NoME42Phi.Get("tight_eta.fit_eff_plots.eta_PLOT");

   plot(hME42EtaLoose,hNoME42EtaLoose,Plots,"LooseEta","Loose #eta");
   plot(hME42EtaTight,hNoME42EtaTight,Plots,"TightEta","Tight #eta");
}

void plot(TH1F* hME42, TH1F* hNoME42, TFile* file, string name, string title)
{
   //hME42->SetLineColor(2);
   //hNoME42->SetLineColor(3);
   //hME42->Draw();
   //hNoME42->Draw("same");
   //file->Write();
}

