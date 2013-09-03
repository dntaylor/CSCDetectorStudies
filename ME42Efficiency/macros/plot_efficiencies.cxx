void plot_all()
{
   TFile* Plots = new TFile("plots.root","RECREATE");

   TCanvas* cLooseEta = plot_single("eta","loose");
   TCanvas* cTightEta = plot_single("eta","tight");
   TCanvas* cLoosePhi = plot_single("phi","loose");
   TCanvas* cTightPhi = plot_single("phi","tight");
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

TCanvas* plot_single(string var, string type)
{
   std::cout << var << " " << type << std::endl;
   if (var=="eta") {
      std::cout << "case: eta" << std::endl;
      TString ME42FileName = "ME42TagAndProbeTreeAnalysisME42Phi.root";
      TString ME42With3Of4FileName = "ME42TagAndProbeTreeAnalysisME42With3Of4Phi.root";
      TString NoME42FileName = "ME42TagAndProbeTreeAnalysisNoME42Phi.root";
      TString PlotName = "eta_PLOT";
      TString VarName = "#eta";
      if (type=="loose") {
         TString ME42DirName = "tagAndProbeTreeME42Phi/loose_eta/fit_eff_plots/";
         TString ME42With3Of4DirName = "tagAndProbeTreeME42With3Of4Phi/loose_eta/fit_eff_plots/";
         TString NoME42DirName = "tagAndProbeTreeNoME42Phi/loose_eta/fit_eff_plots/";
         TString cName = "cLooseEta";
         TString cTitle = "Loose #eta";
         TString rVar = "rLooseEta";
      }
      if (type=="tight") {
         TString ME42DirName = "tagAndProbeTreeME42Phi/tight_eta/fit_eff_plots/";
         TString ME42With3Of4DirName = "tagAndProbeTreeME42With3Of4Phi/tight_eta/fit_eff_plots/";
         TString NoME42DirName = "tagAndProbeTreeNoME42Phi/tight_eta/fit_eff_plots/";
         TString cName = "cTightEta";
         TString cTitle = "Tight #eta";
         TString rVar = "rTightEta";
      }
   }
   if (var=="phi") {
      std::cout << "case: phi" << std::endl;
      TString ME42FileName = "ME42TagAndProbeTreeAnalysisME42Eta.root";
      TString ME42With3Of4FileName = "ME42TagAndProbeTreeAnalysisME42With3Of4Eta.root";
      TString NoME42FileName = "ME42TagAndProbeTreeAnalysisNoME42Eta.root";
      TString PlotName = "phi_PLOT";
      TString VarName = "#phi";
      if (type=="loose") {
         TString ME42DirName = "tagAndProbeTreeME42Eta/loose_phi/fit_eff_plots/";
         TString ME42With3Of4DirName = "tagAndProbeTreeME42With3Of4Eta/loose_phi/fit_eff_plots/";
         TString NoME42DirName = "tagAndProbeTreeNoME42Eta/loose_phi/fit_eff_plots/";
         TString cName = "cLoosePhi";
         TString cTitle = "Loose #phi";
         TString rVar = "rLoosePhi";
      }
      if (type=="tight") {
         TString ME42DirName = "tagAndProbeTreeME42Eta/tight_phi/fit_eff_plots/";
         TString ME42With3Of4DirName = "tagAndProbeTreeME42With3Of4Eta/tight_phi/fit_eff_plots/";
         TString NoME42DirName = "tagAndProbeTreeNoME42Eta/tight_phi/fit_eff_plots/";
         TString cName = "cTightPhi";
         TString cTitle = "Tight #phi";
         TString rVar = "rTightPhi";
      }
   }
   if (var=="pt") {
      std::cout << "case: pt" << std::endl;
      TString ME42FileName = "ME42TagAndProbeTreeAnalysisME42.root";
      TString ME42With3Of4FileName = "ME42TagAndProbeTreeAnalysisME42With3Of4.root";
      TString NoME42FileName = "ME42TagAndProbeTreeAnalysisNoME42.root";
      TString PlotName = "pt_PLOT";
      TString VarName = "p_{T}";
      if (type=="loose") {
         TString ME42DirName = "tagAndProbeTreeME42/loose_pt/fit_eff_plots/";
         TString ME42With3Of4DirName = "tagAndProbeTreeME42With3Of4/loose_pt/fit_eff_plots/";
         TString NoME42DirName = "tagAndProbeTreeNoME42/loose_pt/fit_eff_plots/";
         TString cName = "cLoosePt";
         TString cTitle = "Loose p_{T}";
         TString rVar = "rLoosePt";
      }
      if (type=="tight") {
         TString ME42DirName = "tagAndProbeTreeME42/tight_pt/fit_eff_plots/";
         TString ME42With3Of4DirName = "tagAndProbeTreeME42With3Of4/tight_pt/fit_eff_plots/";
         TString NoME42DirName = "tagAndProbeTreeNoME42/tight_pt/fit_eff_plots/";
         TString cName = "cTightPt";
         TString cTitle = "Tight p_{T}";
         TString rVar = "rTightPt";
      }
   }


   TFile* ME42 = TFile::Open(ME42FileName);
   TFile* ME42With3Of4 = TFile::Open(ME42With3Of4FileName);
   TFile* NoME42 = TFile::Open(NoME42FileName);

   TDirectory* ME42Dir = ME42->GetDirectory(ME42DirName);
   TDirectory* ME42With3Of4Dir = ME42With3Of4->GetDirectory(ME42With3Of4DirName);
   TDirectory* NoME42Dir = NoME42->GetDirectory(NoME42DirName);

   TCanvas* cME42 = (TCanvas*)ME42Dir->Get(PlotName);
   TCanvas* cME42With3Of4 = (TCanvas*)ME42With3Of4Dir->Get(PlotName);
   TCanvas* cNoME42 = (TCanvas*)NoME42Dir->Get(PlotName);

   RooHist* rhME42 = (RooHist*)cME42->GetPrimitive("hxy_fit_eff");
   RooHist* rhME42With3Of4 = (RooHist*)cME42With3Of4->GetPrimitive("hxy_fit_eff");
   RooHist* rhNoME42 = (RooHist*)cNoME42->GetPrimitive("hxy_fit_eff");
   
   TCanvas* c = new TCanvas(cName,cTitle,800,600);

   RooRealVar x(rVar,VarName,rhME42->GetXaxis()->GetXmin(),rhME42->GetXaxis()->GetXmax());
   RooPlot* frame = x.frame();

   rhME42->SetLineColor(kRed);
   rhME42With3Of4->SetLineColor(kGreen);
   rhNoME42->SetLineColor(kBlue);

   frame->addPlotable(rhME42,"P");
   frame->addPlotable(rhME42With3Of4,"P");
   frame->addPlotable(rhNoME42,"P");
   frame->SetMinimum(0.8);
   frame->SetMaximum(1.0);
   frame->SetTitle(cTitle);
   frame->SetYTitle("Efficiency");
   frame->Draw();

   // Draw Legend
   TLegend* l = new TLegend(0.1,0.1,0.4,0.2);
   l->AddEntry(rhME42,"ME4/2 Region","l");
   l->AddEntry(rhME42With3Of4,"ME4/2 Region (Req. 3 Stations)","l");
   l->AddEntry(rhNoME42,"Non-ME4/2 Region","l");
   l->Draw();

   // draw lines
   if (var=="eta") {
      TLine* l1 = new TLine(1.2,0.8,1.2,1);
      TLine* l2 = new TLine(1.8,0.8,1.8,1);
      l1->SetLineStyle(2);
      l2->SetLineStyle(2);
      l1->Draw();
      l2->Draw();
   }
   if (var=="phi") {
      TLine* l1 = new TLine(60.*TMath::Pi()/180.,0.8,60.*TMath::Pi()/180.,1);
      TLine* l2 = new TLine(120.*TMath::Pi()/180.,0.8,120.*TMath::Pi()/180.,1);
      l1->SetLineStyle(2);
      l2->SetLineStyle(2);
      l1->Draw();
      l2->Draw();
   }

   c->Update();
   return c;
}
