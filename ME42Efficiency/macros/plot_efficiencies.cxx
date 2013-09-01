void plot()
{
   TFile* Plots = new TFile("plots.root","RECREATE");

   TFile* ME42Phi = TFile::Open("ME42TagAndProbeTreeAnalysisME42Phi.root");
   TFile* NoME42Phi = TFile::Open("ME42TagAndProbeTreeAnalysisNoME42Phi.root");

   TDirectory* ME42PhiLooseEtaDir = ME42Phi->GetDirectory("tagAndProbeTreeME42Phi/loose_eta/fit_eff_plots/");
   TDirectory* NoME42PhiLooseEtaDir = NoME42Phi->GetDirectory("tagAndProbeTreeNoME42Phi/loose_eta/fit_eff_plotsi/");

   TCanvas* cME42LooseEta = (TCanvas*)ME42PhiLooseEtaDir->Get("eta_PLOT");
   TCanvas* cNoME42LooseEta = (TCanvas*)NoME42PhiLooseEtaDir->Get("eta_PLOT");

   RooHist* rhME42LooseEta = (RooHist*)cME42LooseEta->GetPrimitive("hxy_fit_eff");
   RooHist* rhNoME42LooseEta = (RooHist*)cNoME42LooseEta->GetPrimitive("hxy_fit_eff");

   TH1F* hME42LooseEta = (TH1F*)rhME42LooseEta->GetHistogram();
   TH1F* hNoME42LooseEta = (TH1F*)rhNoME42LooseEta->GetHistogram();

   hME42EtaLoose->Draw();
   hNoME42EtaLoose->Draw("same");
   hME42EtaLoose->SetLineColor(2);
   hNoME42EtaLoose->SetLineColor(3);
   c1->Update()
   Plots->Write();
}

