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

   TCanvas* cLooseEta = plot_single("eta","loose");
   TCanvas* cTightEta = plot_single("eta","tight");
   TCanvas* cLoosePhi = plot_single("phi","loose");
   TCanvas* cTightPhi = plot_single("Phi","tight");
   TCanvas* cLoosePt = plot_single("pt","loose");
   TCanvas* cTightPt = plot_single("pt","tight");

   Plots->WriteTObject(cLooseEta);
   Plots->WriteTObject(cTightEta);
   Plots->WriteTObject(cLoosePhi);
   Plots->WriteTObject(cTightPhi);
   Plots->WriteTObject(cLoosePt);
   Plots->WriteTObject(cTightPt);

   Plots->Close();
}

TCanvas* plot_single(TString var, TString type)
{
   switch (var) 
   {
   case "eta":
      TString ME42FileName = "ME42TagAndProbeTreeAnalysisME42Phi.root";
      TString NoME42FileName = "ME42TagAndProbeTreeAnalysisNoME42Phi.root";
      TString PlotName = "eta_PLOT";
      TString VarName = "#eta";
      switch (type)
      {
      case "loose":
         TString ME42DirName = "tagAndProbeTreeME42Phi/loose_eta/fit_eff_plots/";
         TString NoME42DirName = "tagAndProbeTreeNoME42Phi/loose_eta/fit_eff_plots/";
         TString cName = "cLooseEta";
         TString cTitle = "Loose #eta";
         TString rVar = "rLooseEta";
         break;
      case "tight":
         TString ME42DirName = "tagAndProbeTreeME42Phi/tight_eta/fit_eff_plots/";
         TString NoME42DirName = "tagAndProbeTreeNoME42Phi/tight_eta/fit_eff_plots/";
         TString cName = "cTightEta";
         TString cTitle = "Tight #eta";
         TString rVar = "rTightEta";
         break;
      default:
         break;
      }
      break;
   case "phi":
      TString ME42FileName = "ME42TagAndProbeTreeAnalysisME42Eta.root";
      TString NoME42FileName = "ME42TagAndProbeTreeAnalysisNoME42Eta.root";
      TString PlotName = "phi_PLOT";
      TString VarName = "#phi";
      switch (type)
      {
      case "loose":
         TString ME42DirName = "tagAndProbeTreeME42Eta/loose_phi/fit_eff_plots/";
         TString NoME42DirName = "tagAndProbeTreeNoME42Eta/loose_phi/fit_eff_plots/";
         TString cName = "cLoosePhi";
         TString cTitle = "Loose #phi";
         TString rVar = "rLoosePhi";
         break;
      case "tight":
         TString ME42DirName = "tagAndProbeTreeME42Eta/tight_phi/fit_eff_plots/";
         TString NoME42DirName = "tagAndProbeTreeNoME42Eta/tight_phi/fit_eff_plots/";
         TString cName = "cTightPhi";
         TString cTitle = "Tight #phi";
         TString rVar = "rTightPhi";
         break;
      default:
         break;
      }
      break;
   case "pt":
      TString ME42FileName = "ME42TagAndProbeTreeAnalysisME42.root";
      TString NoME42FileName = "ME42TagAndProbeTreeAnalysisNoME42.root";
      TString PlotName = "pt_PLOT";
      TString VarName = "p_{T}";
      switch (type)
      {
      case "loose":
         TString ME42DirName = "tagAndProbeTreeME42/loose_pt/fit_eff_plots/";
         TString NoME42DirName = "tagAndProbeTreeNoME42/loose_pt/fit_eff_plots/";
         TString cName = "cLoosePt";
         TString cTitle = "Loose p_{T}";
         TString rVar = "rLoosePt";
         break;
      case "tight":
         TString ME42DirName = "tagAndProbeTreeME42/tight_pt/fit_eff_plots/";
         TString NoME42DirName = "tagAndProbeTreeNoME42/tight_pt/fit_eff_plots/";
         TString cName = "cTightPt";
         TString cTitle = "Tight p_{T}";
         TString rVar = "rTightPt";
         break;
      default:
         break;
      }
      break;
   default:
      break;
   }


   TFile* ME42 = TFile::Open(ME42FileName);
   TFile* NoME42 = TFile::Open(NoME42FileName);

   TDirectory* ME42Dir = ME42->GetDirectory(ME42DirName);
   TDirectory* NoME42Dir = NoME42->GetDirectory(NoME42DirName);

   TCanvas* cME42 = (TCanvas*)ME42Dir->Get(PlotName);
   TCanvas* cNoME42 = (TCanvas*)NoME42Dir->Get(PlotName);

   RooHist* rhME42 = (RooHist*)cME42->GetPrimitive("hxy_fit_eff");
   RooHist* rhNoME42 = (RooHist*)cNoME42->GetPrimitive("hxy_fit_eff");
   
   //Plots->cd();
   TCanvas* c = new TCanvas(cName,cTitle,800,600);

   RooRealVar x(rVar,VarName,rhME42->GetXaxis()->GetXmin(),rhME42->GetXaxis()->GetXmax());
   RooPlot* frame = x.frame();

   rhME42->SetLineColor(kRed);
   rhNoME42->SetLineColor(kBlue);

   frame->addPlotable(rhME42,"P");
   frame->addPlotable(rhNoME42,"P");
   frame->Draw();
   c->Update();
   //c->Write();
   return c
}
