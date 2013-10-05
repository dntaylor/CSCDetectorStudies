void plot_all()
{
   TFile* Plots = new TFile("plots.root","RECREATE");

//   TCanvas* cLooseEta = plot_single("eta","loose");
//   TCanvas* cTightEta = plot_single("eta","tight");
//   TCanvas* cLoosePhi = plot_single("phi","loose");
//   TCanvas* cTightPhi = plot_single("phi","tight");
//   TCanvas* cLoosePt = plot_single("pt","loose");
//   TCanvas* cTightPt = plot_single("pt","tight");
//
//   Plots->WriteTObject(cLooseEta);
//   Plots->WriteTObject(cTightEta);
//   Plots->WriteTObject(cLoosePhi);
//   Plots->WriteTObject(cTightPhi);
//   Plots->WriteTObject(cLoosePt);
//   Plots->WriteTObject(cTightPt);

//   TCanvas* cLooseME42 = plot_single2("ME42","loose");
   TCanvas* cME42 = plot_single2("ME42","match");
//   TCanvas* cTightME42 = plot_single2("ME42","tight");
//   TCanvas* cLoosePt = plot_single2("pt","loose");
   TCanvas* cPt = plot_single2("pt","match");
//   TCanvas* cTightPt = plot_single2("pt","tight");
//   TCanvas* cLooseSta = plot_single2("sta","loose");
//   TCanvas* cTightSta = plot_single2("sta","tight");

   Plots->Close();
}

TCanvas* plot_single2(string var, string type)
{
   if (var=="ME42") {
      TString ME42FileName = "ME42TagAndProbeTreeAnalysisEta.root";
      TString PlotName = "isME42_PLOT";
      TString VarName = "";
      if (type=="loose") {
         TString ME42DirName = "tagAndProbeTreeEta/loose_ME42/fit_eff_plots/";
         TString cName = "cLooseME42";
         TString cTitle = "Loose #mu";
         TString rVar = "rLooseME42";
      }
      if (type=="tight") {
         TString ME42DirName = "tagAndProbeTreeEta/tight_ME42/fit_eff_plots/";
         TString cName = "cTightME42";
         TString cTitle = "Tight #mu";
         TString rVar = "rTightME42";
      }
      if (type=="match") {
         TString ME42DirName = "tagAndProbeTreeEta/ME42/fit_eff_plots/";
         TString cName = "cME42";
         TString cTitle = "Track Passing Standalone";
         TString rVar = "rME42";
      }
   }
   if (var=="pt") {
      TString ME42FileName = "ME42TagAndProbeTreeAnalysisME42.root";
      TString NoME42FileName = "ME42TagAndProbeTreeAnalysisEtaNoME42.root";
      TString PlotName = "pt_PLOT";
      TString VarName = "p_{T}";
      if (type=="loose") {
         TString ME42DirName = "tagAndProbeTreeME42/loose_pt/fit_eff_plots/";
         TString NoME42DirName = "tagAndProbeTreeNoME42Eta/loose_pt/fit_eff_plots/";
         TString cName = "cLoosePt";
         TString cTitle = "Loose #mu";
         TString rVar = "rLoosePt";
      }
      if (type=="tight") {
         TString ME42DirName = "tagAndProbeTreeME42/tight_pt/fit_eff_plots/";
         TString NoME42DirName = "tagAndProbeTreeNoME42Eta/tight_pt/fit_eff_plots/";
         TString cName = "cTightPt";
         TString cTitle = "Tight #mu";
         TString rVar = "rTightPt";
      }
      if (type=="match") {
         TString ME42DirName = "tagAndProbeTreeME42/pt/fit_eff_plots/";
         TString NoME42DirName = "tagAndProbeTreeEtaNoME42/pt/fit_eff_plots/";
         TString cName = "cPt";
         TString cTitle = "Track Passing Standalone";
         TString rVar = "rPt";
      }
   }
   if (var=="sta") {
      TString ME42FileName = "ME42TagAndProbeTreeAnalysisME42.root";
      TString NoME42FileName = "ME42TagAndProbeTreeAnalysisNoME42Eta.root";
      TString PlotName = "numMatchedStations_PLOT";
      TString VarName = "Number of Matched Stations";
      if (type=="loose") {
         TString ME42DirName = "tagAndProbeTreeME42/loose_matchedStations/fit_eff_plots/";
         TString NoME42DirName = "tagAndProbeTreeNoME42Eta/loose_matchedStations/fit_eff_plots/";
         TString cName = "cLooseSta";
         TString cTitle = "Loose #mu";
         TString rVar = "rLooseSta";
      }
      if (type=="tight") {
         TString ME42DirName = "tagAndProbeTreeME42/tight_matchedStations/fit_eff_plots/";
         TString NoME42DirName = "tagAndProbeTreeNoME42Eta/tight_matchedStations/fit_eff_plots/";
         TString cName = "cTightSta";
         TString cTitle = "Tight #mu";
         TString rVar = "rTightSta";
      }
   }

   TFile* ME42 = TFile::Open(ME42FileName);
   TDirectory* ME42Dir = ME42->GetDirectory(ME42DirName);
   TCanvas* cME42 = (TCanvas*)ME42Dir->Get(PlotName);
   RooHist* rhME42 = (RooHist*)cME42->GetPrimitive("hxy_fit_eff");

   if (var=="pt" || var=="sta") {
      TFile* NoME42 = TFile::Open(NoME42FileName);
      TDirectory* NoME42Dir = NoME42->GetDirectory(NoME42DirName);
      TCanvas* cNoME42 = (TCanvas*)NoME42Dir->Get(PlotName);
      RooHist* rhNoME42 = (RooHist*)cNoME42->GetPrimitive("hxy_fit_eff");
   }

   TCanvas* c = new TCanvas(cName,cTitle,800,600);

   RooRealVar x(rVar,VarName,rhME42->GetXaxis()->GetXmin(),rhME42->GetXaxis()->GetXmax());
   if (var=="ME42") {
      RooPlot* frame = x.frame(2);
   }
   else if (var=="sta") {
      RooPlot* frame = x.frame(4);
   }
   else {
      RooPlot* frame = x.frame();
   }

   rhME42->SetLineColor(kRed);
   if (var=="pt" || var=="sta") { rhNoME42->SetLineColor(kBlue); }
   
   // bin labels
   if (var=="ME42") {
      const int numLabels = 2;
      const char *isME42Labels[numLabels] = {"Non-ME4/2","ME4/2"};
      for (int i=0;i<numLabels;i++) {
         frame->GetXaxis()->SetBinLabel(i+1,isME42Labels[i]); 
      }
   }
   if (var=="sta") {
      const int numLabels = 4;
      const char *numMatchedStationsLabels[numLabels] = {"2","3","4","5"};
      for (int i=0;i<numLabels;i++) {
         frame->GetXaxis()->SetBinLabel(i+1,numMatchedStationsLabels[i]);
      }
   }

   frame->addPlotable(rhME42,"P");
   if (var=="pt") { frame->addPlotable(rhNoME42,"P"); }
   if (var=="sta") { frame->addPlotable(rhNoME42,"P"); }
   frame->SetMinimum(0.9);
   frame->SetMaximum(1.0);
   frame->SetTitle(cTitle);
   frame->SetYTitle("Efficiency");
   frame->Draw();

   // Draw Legend
   if (var=="pt" || var=="sta") {
      TLegend* l = new TLegend(0.7,0.8,0.9,0.9);
      l->AddEntry(rhME42,"ME4/2 Region","l");
      l->AddEntry(rhNoME42,"Non-ME4/2 Region","l");
      l->Draw();
   }

   c->Update();
   return c;

}
