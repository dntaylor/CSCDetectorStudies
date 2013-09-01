void plot()
{
   TFile* Plots = new TFile("plots.root","RECREATE");

   TFile* ME42Phi = TFile::Open("ME42TagAndProbeTreeAnalysisME42Phi.root");
   TFile* NoME42Phi = TFile::Open("ME42TagAndProbeTreeAnalysisNoME42Phi.root");

   TDirectory* ME42PhiLooseEtaDir = ME42Phi->GetDirectory("tagAndProbeTreeME42Phi/loose_eta/fit_eff_plots/");
   TDirectory* NoME42PhiLooseEtaDir = NoME42Phi->GetDirectory("tagAndProbeTreeNoME42Phi/loose_eta/fit_eff_plots/");

   TCanvas* cME42LooseEta = (TCanvas*)ME42PhiLooseEtaDir->Get("eta_PLOT");
   TCanvas* cNoME42LooseEta = (TCanvas*)NoME42PhiLooseEtaDir->Get("eta_PLOT");

   RooHist* rhME42LooseEta = (RooHist*)cME42LooseEta->GetPrimitive("hxy_fit_eff");
   RooHist* rhNoME42LooseEta = (RooHist*)cNoME42LooseEta->GetPrimitive("hxy_fit_eff");

   TH1F* hME42LooseEta = (TH1F*)rhME42LooseEta->GetHistogram();
   TH1F* hNoME42LooseEta = (TH1F*)rhNoME42LooseEta->GetHistogram();

   TCanvas* cLooseEta = new TCanvas("cLooseEta","Loose #eta",600,600);
   cLooseEta->cd();

   hME42LooseEta->Draw();
   hNoME42LooseEta->Draw("same");
   hME42LooseEta->SetLineColor(2);
   hNoME42LooseEta->SetLineColor(4);
   cLooseEta->Update();
   Plots->Write();
}

void plot_all()
{
   TFile* Plots = new TFile("plots.root","RECREATE");

   plot_single(Plots,"ME42TagAndProbeTreeAnalysisME42Phi.root","ME42TagAndProbeTreeAnalysisNoME42Phi.root","tagAndProbeTreeME42Phi/loose_eta/fit_eff_plots/","tagAndProbeTreeNoME42Phi/loose_eta/fit_eff_plots/","eta_PLOT","cLooseEta","Loose #eta");
   plot_single(Plots,"ME42TagAndProbeTreeAnalysisME42Phi.root","ME42TagAndProbeTreeAnalysisNoME42Phi.root","tagAndProbeTreeME42Phi/tight_eta/fit_eff_plots/","tagAndProbeTreeNoME42Phi/tight_eta/fit_eff_plots/","eta_PLOT","cTightEta","Tight #eta");

}

void plot_single(TFile* Plots, TString ME42FileName, TString NoME42FileName, TString ME42DirName, TString NoME42DirName, TString PlotName, TString cName, TString cTitle)
{
   TFile* ME42 = TFile::Open(ME42FileName);
   TFile* NoME42 = TFile::Open(NoME42FileName);

   TDirectory* ME42Dir = ME42->GetDirectory(ME42DirName);
   TDirectory* NoME42Dir = NoME42->GetDirectory(NoME42DirName);

   TCanvas* cME42 = (TCanvas*)ME42Dir->Get(PlotName);
   TCanvas* cNoME42 = (TCanvas*)NoME42Dir->Get(PlotName);

   RooHist* rhME42 = (RooHist*)cME42->GetPrimitive("hxy_fit_eff");
   RooHist* rhNoME42 = (RooHist*)cNoME42->GetPrimitive("hxy_fit_eff");

   TH1F* hME42 = (TH1F*)rhME42->GetHistogram();
   TH1F* hNoME42 = (TH1F*)rhNoME42->GetHistogram();

   TCanvas* c = new TCanvas(cName,cTitle,600,600);
   c->cd();

   hME42->Draw();
   hNoME42->Draw("same");
   hME42->SetLineColor(2);
   hNoME42->SetLineColor(4);
   c->Update();
   Plots->Write();
}
