import FWCore.ParameterSet.Config as cms

process = cms.Process("TagProbe")

process.load('FWCore.MessageService.MessageLogger_cfi')

process.source = cms.Source("EmptySource")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )   

process.TagProbeFitTreeAnalyzer = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
	InputFileNames = cms.vstring("ME42TagAndProbeTree.root"),
	InputDirectoryName = cms.string("tagAndProbeTree"),
	InputTreeName = cms.string("fitter_tree"),
	OutputFileName = cms.string("ME42TagAndProbeTreeAnalysis.root"),
	NumCPU = cms.uint32(1),
	SaveWorkspace = cms.bool(True),
	Variables = cms.PSet(
		mass = cms.vstring("Tag-Probe Mass", "60.0", "120.0", "GeV/c^{2}"),
		pt = cms.vstring("Probe p_{T}", "0", "500", "GeV/c"),
		eta = cms.vstring("Probe #eta", "-2.4", "2.4", ""),
	),
	Categories = cms.PSet(
		passingGlobalMuon = cms.vstring("isGlobalMuon", "dummy[true=1,false=0]"),
		passingCaloMuon = cms.vstring("isCaloMuon", "dummy[true=1,false=0]"),
		passingPFMuon = cms.vstring("isPFMuon", "dummy[true=1,false=0]"),
		passingLooseMuon = cms.vstring("isLooseMuon", "dummy[true=1,false=0]"),
		passingTightMuon = cms.vstring("isTightMuon", "dummy[true=1,false=0]"),
		passingProbeMuonCut = cms.vstring("passed probe cut", "dummy[true=1,false=0]"),
		ME42PhiRegion = cms.vstring("ME42 phi ergion", "dummy[true=1,false=0]"),
	),
	Cuts = cms.PSet(
		# cant do phi cuts with current syntax, include in categories instead
	),
	PDFs = cms.PSet(
		gaussPlusLinear = cms.vstring(
			"Gaussian::signal(mass, mean[3.1,3.0,3.2], sigma[0.03,0.01,0.05])",
			"Chebychev::backgroundPass(mass, cPass[0,-1,1])",
			"Chebychev::backgroundFail(mass, cFail[0,-1,1])",
			"efficiency[0.9,0,1]",
			"signalFractionInPassing[0.9]"
		),
		gaussPlusQuadratic = cms.vstring(
			"Gaussian::signal(mass, mean[3.1,3.0,3.2], sigma[0.03,0.01,0.05])",
			"Chebychev::backgroundPass(mass, {cPass1[0,-1,1], cPass2[0,-1,1]})",
		        "Chebychev::backgroundFail(mass, {cFail1[0,-1,1], cFail2[0,-1,1]})",
			"efficiency[0.9,0,1]",
			"signalFractionInPassing[0.9]"
		),
		voigtianPlusExponential = cms.vstring(
			"Voigtian::signalPass(mass, meanP[90,80,100], width[2.495], sigmaP[3,1,20])",
			"Voigtian::signalFail(mass, meanF[90,80,100], width[2.495], sigmaF[3,1,20])",
			"Exponential::backgroundPass(mass, lp[0,-5,5])",
			"Exponential::backgroundFail(mass, lf[0,-5,5])",
			"efficiency[0.9,0,1]",
			"signalFractionInPassing[0.9]"
		),
	),

        Efficiencies = cms.PSet(
		tight_pt_withME42 = cms.PSet(
			EfficiencyCategoryAndState = cms.vstring("passingTightMuon","true","ME42PhiRegion","true"),
		        UnbinnedVariables = cms.vstring("mass"),
			BinnedVariables = cms.PSet(
				pt = cms.vdouble(20.0, 60.0, 100.0, 200.0, 500.0),
			),
			BinToPDFmap = cms.vstring("voigtianPlusExponential")
		),
		tight_eta_withME42 = cms.PSet(
			EfficiencyCategoryAndState = cms.vstring("passingTightMuon","true","ME42PhiRegion","true"),
		        UnbinnedVariables = cms.vstring("mass"),
			BinnedVariables = cms.PSet(
				eta = cms.vdouble(-2.4, -1.8, -1.2, 0.0, 1.2, 1.8, 2.4),
			),
			BinToPDFmap = cms.vstring("voigtianPlusExponential")
		),
		loose_pt_withME42 = cms.PSet(
			EfficiencyCategoryAndState = cms.vstring("passingLooseMuon","true","ME42PhiRegion","true"),
		        UnbinnedVariables = cms.vstring("mass"),
			BinnedVariables = cms.PSet(
				pt = cms.vdouble(20.0, 60.0, 100.0, 200.0, 500.0),
			),
			BinToPDFmap = cms.vstring("voigtianPlusExponential")
		),
		loose_eta_withME42 = cms.PSet(
			EfficiencyCategoryAndState = cms.vstring("passingLooseMuon","true","ME42PhiRegion","true"),
		        UnbinnedVariables = cms.vstring("mass"),
			BinnedVariables = cms.PSet(
				eta = cms.vdouble(-2.4, -1.8, -1.2, 0.0, 1.2, 1.8, 2.4),
			),
			BinToPDFmap = cms.vstring("voigtianPlusExponential")
		),
		tight_pt_withoutME42 = cms.PSet(
			EfficiencyCategoryAndState = cms.vstring("passingTightMuon","true","ME42PhiRegion","false"),
		        UnbinnedVariables = cms.vstring("mass"),
			BinnedVariables = cms.PSet(
				pt = cms.vdouble(20.0, 60.0, 100.0, 200.0, 500.0),
			),
			BinToPDFmap = cms.vstring("voigtianPlusExponential")
		),
		tight_eta_withoutME42 = cms.PSet(
			EfficiencyCategoryAndState = cms.vstring("passingTightMuon","true","ME42PhiRegion","false"),
		        UnbinnedVariables = cms.vstring("mass"),
			BinnedVariables = cms.PSet(
				eta = cms.vdouble(-2.4, -1.8, -1.2, 0.0, 1.2, 1.8, 2.4),
			),
			BinToPDFmap = cms.vstring("voigtianPlusExponential")
		),
		loose_pt_withoutME42 = cms.PSet(
			EfficiencyCategoryAndState = cms.vstring("passingLooseMuon","true","ME42PhiRegion","false"),
		        UnbinnedVariables = cms.vstring("mass"),
			BinnedVariables = cms.PSet(
				pt = cms.vdouble(20.0, 60.0, 100.0, 200.0, 500.0),
			),
			BinToPDFmap = cms.vstring("voigtianPlusExponential")
		),
		loose_eta_withoutME42 = cms.PSet(
			EfficiencyCategoryAndState = cms.vstring("passingLooseMuon","true","ME42PhiRegion","false"),
		        UnbinnedVariables = cms.vstring("mass"),
			BinnedVariables = cms.PSet(
				eta = cms.vdouble(-2.4, -1.8, -1.2, 0.0, 1.2, 1.8, 2.4),
			),
			BinToPDFmap = cms.vstring("voigtianPlusExponential")
		),
	)
)

process.fitness = cms.Path(
	process.TagProbeFitTreeAnalyzer
)
	
