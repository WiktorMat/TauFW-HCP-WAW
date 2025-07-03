# Author: Izaak Neutelings (June 2020)
# Description: Simple module to pre-select mutau events
import sys
import numpy as np
from TauFW.PicoProducer import datadir
from TauFW.PicoProducer.analysis.TreeProducerTauTau import *
from TauFW.PicoProducer.analysis.ModuleTauPair import *
from TauFW.PicoProducer.analysis.utils import DiTauPair, loosestIso, idIso, matchgenvistau, matchtaujet
from TauFW.PicoProducer.corrections.TrigObjMatcher import TrigObjMatcher
from TauFW.PicoProducer.corrections.TauTriggerSFs import TauTriggerSFs
from TauPOG.TauIDSFs.TauIDSFTool import TauIDSFTool, TauESTool, TauFESTool
from TauFW.PicoProducer.analysis.HiggsCPtools.PhiCP_reco import *
from TauFW.PicoProducer.analysis.HiggsCPtools.PhiCP_gen_reco import *
from TauFW.PicoProducer.analysis.HiggsCPtools.GenParticles import *
from TauFW.PicoProducer.FastMTT.FastMTT import FastMTT
from TauFW.PicoProducer.analysis.HiggsCPtools.Polarimetric import *
from TauFW.PicoProducer.analysis.HiggsCPtools.Data_Dump import *

# sys.path.append('~/CMSSW_14_1_0_pre4/src')
from TauFW.PicoProducer.corrections.DeepTau2018v2p5SFTool import DeepTau2018v2p5SFTool # NEW Tool for tau SFs and TES from correctionlib

wp_vsjet, wp_vse, wp_vsmu, syst = "Medium", "VVLoose", "Tight", "nom"
class ModuleTauTau(ModuleTauPair):
  
  def __init__(self, fname, **kwargs):
    kwargs['channel'] = 'mutau'
    super(ModuleTauTau,self).__init__(fname,**kwargs)
    self.out = TreeProducerTauTau(fname,self)
    self.deepTauSFTool = DeepTau2018v2p5SFTool(self.era) #NEW
    
    # TODO: remove hardcoded values and make wps configurable
    self.wp_vsjet = "Medium"
    self.wp_vse   = "VVLoose"
    self.wp_vsmu  = "Tight"
    self.syst     = "nom"

    # TRIGGERS
    jsonfile       = os.path.join(datadir,"trigger/tau_triggers_%d.json"%(self.year))
    #self.trigger   = TrigObjMatcher(jsonfile,trigger='ditau',isdata=self.isdata) #TO_DO
    self.tauCutPt  = 20 #Tightened from 40 for test analyses during development
    self.tauCutEta = 2.5 #Tightened from 2.1 for test analyses during development
    
    # CORRECTIONS
    #if self.ismc:
      #self.trigTool       = TauTriggerSFs('tautau','Medium',year=self.year) #TO_DO
      #self.trigTool_tight = TauTriggerSFs('tautau','Tight', year=self.year)
      #self.tesTool        = TauESTool(tauSFVersion[self.year]) # real tau energy scale
      ### TO_DO (TAU SCALES, TAU FAKE SCALES, TAU TRIGGERS for 2022) ###
      #self.fesTool        = TauFESTool(tauSFVersion[self.year]) # e -> tau fake energy scale
      #self.tauSFs         = TauIDSFTool(tauSFVersion[self.year],'DeepTau2017v2p1VSjet','Medium',dm=True)
      #self.tauSFs_tight   = TauIDSFTool(tauSFVersion[self.year],'DeepTau2017v2p1VSjet','Tight',dm=True)
      #self.etfSFs         = TauIDSFTool(tauSFVersion[self.year],'DeepTau2017v2p1VSe', 'VVLoose')
      #self.mtfSFs         = TauIDSFTool(tauSFVersion[self.year],'DeepTau2017v2p1VSmu','Loose')
    
    # CUTFLOW
    self.out.cutflow.addcut('none',         "no cut"                      )
    self.out.cutflow.addcut('trig',         "trigger"                     )
    self.out.cutflow.addcut('tau',          "tau"                         )
    self.out.cutflow.addcut('pair',         "ditau pair"                  )
    self.out.cutflow.addcut('weight',       "no cut, weighted", 15        )
    self.out.cutflow.addcut('weight_no0PU', "no cut, weighted, PU>0", 16  ) # use for normalization
    
  
  def beginJob(self):
    """Before processing any events or files."""
    super(ModuleTauTau,self).beginJob()
    print(">>> %-12s = %s"%('tauwp',     self.tauwp))
    print(">>> %-12s = %s"%('tauCutPt',  self.tauCutPt))
    print(">>> %-12s = %s"%('tauCutEta', self.tauCutEta))
    #print(">>> %-12s = '%s'"%('triggers',self.trigger.path.replace("||","\n>>> %s||"%(' '*16))))
    
  
  def analyze(self, event):
    """Process and pre-select events; fill branches and return True if the events passes,
    return False otherwise."""
    sys.stdout.flush()
    
    
    ##### NO CUT #####################################
    #if not self.fillhists(event):
    #  return False
    
    
    ##### TRIGGER ####################################
    #if not self.trigger.fired(event):
    #  return False
    self.out.cutflow.fill('trig')
    
    
    ##### TAU ########################################
    taus = [ ]
    for tau in Collection(event,'Tau'):
      if abs(tau.eta)>self.tauCutEta: continue
      if abs(tau.dz)>0.2: continue
      if tau.decayMode not in [0,1,2,10,11]: continue
      if abs(tau.charge)!=1: continue
      if tau.idDeepTau2017v2p1VSe<1: continue   # VVVLoose
      if tau.idDeepTau2017v2p1VSmu<1: continue  # VLoose
      if tau.idDeepTau2017v2p1VSjet<self.tauwp: continue
      if self.ismc:
        self.out.tau_pt_preSF[0] = tau.pt # store original tau pt before applying TES
        tau.es   = 1 # store energy scale for propagating to MET
        genmatch = tau.genPartFlav
        if genmatch==5: # real tau
          if self.tes!=None: # user-defined energy scale (for TES studies)
            tes = self.tes
          else: # recommended energy scale (apply by default)
            tes = 1 #self.tesTool.getTES(tau.pt,tau.decayMode,unc=self.tessys)
          if tes!=1:
            tau.pt   *= tes
            tau.mass *= tes
            tau.es    = tes # store for later reuse
          if self.era in ["2022EE"]: #, "2018UL", "2022_preEE", "2022_postEE", "2023", "2023BPix"]: # only for some samples, otherwise no corrections from correctionlib
            tes_correction = self.deepTauSFTool.tes(tau.pt, tau.eta, tau.decayMode, 5, self.wp_vsjet, self.wp_vse, self.syst)
            self.out.tes_sf[0] = tes_correction
            tau.pt   *= tes_correction
            tau.mass *= tes_correction
            tau.es    = tes_correction # store for later reuse
        elif self.ltf and 0<genmatch<5: # lepton -> tau fake
          tau.pt   *= self.ltf
          tau.mass *= self.ltf
          tau.es    = self.ltf # store for later reuse
        #elif genmatch in [1,3]: # electron -> tau fake (apply by default, override with 'ltf=1.0')
        #  fes = self.fesTool.getFES(tau.eta,tau.decayMode,unc=self.fes)
        #  tau.pt   *= fes
        #  tau.mass *= fes
        #  tau.es    = fes
        elif self.jtf!=1.0 and genmatch==0: # jet -> tau fake
          tau.pt   *= self.jtf
          tau.mass *= self.jtf
          tau.es    = self.jtf
      if tau.pt<self.tauCutPt: continue
      taus.append(tau)
    if len(taus)==0:
      return False
    self.out.cutflow.fill('tau')
    
    
    ##### DITAU PAIR #################################
    ditaus = [ ]
    for i, tau1 in enumerate(taus,1):
      for tau2 in taus[i:]:
        if tau1.DeltaR(tau2)<0.5: continue
        ditau = DiTauPair(tau1,tau1.rawDeepTau2017v2p1VSjet,tau2,tau2.rawDeepTau2017v2p1VSjet)
        ditaus.append(ditau)
    if len(ditaus)==0:
      return False
    tau1, tau2 = max(ditaus).pair
    tau1.tlv   = tau1.p4()
    tau2.tlv   = tau2.p4()
    self.out.cutflow.fill('pair')

    ### FastMTT ###

    measuredTauLeptons = np.array([[[1, tau1.pt, tau1.eta, tau1.phi, tau1.mass, tau1.decayMode], [1, tau2.pt, tau2.eta, tau2.phi, tau2.mass, tau2.decayMode]]])
    METx = np.array([event.PFMET_pt * np.cos(event.PFMET_phi)])
    METy = np.array([event.PFMET_pt * np.sin(event.PFMET_phi)])
    covMET = np.array([[[event.PFMET_covXX, event.PFMET_covXY], [event.PFMET_covXY, event.PFMET_covYY]]])

    fMTT = FastMTT()
    fMTT.TimeReport = False
    fMTT.myLikelihood.setWindow = [123, 127]
    fMTT.myLikelihood.enableLikelihoodComponents(window = True)
    fMTT.run(measuredTauLeptons, METx, METy, covMET)

    mFast = fMTT.mass[0]
    fMTT_tau1P4 = fMTT.tau1P4[0]
    fMTT_tau2P4 = fMTT.tau2P4[0]
    X1 = fMTT.BestX[0, 0]
    X2 = fMTT.BestX[0, 1]

    ### CP ACOPLANARITY ANGLE ###

    tau_products1 = []
    tau_products2 = []
    for product in Collection(event,'TauProd'):
      if product.tauIdx == 0:
        tau_products1.append(product)
      elif product.tauIdx == 1:
        tau_products2.append(product)

    tau1_products_list = dump_tau_products(tau_products1, number_of_products=5)
    tau2_products_list = dump_tau_products(tau_products2, number_of_products=5)

    if self.ismc:
      genParticles = []
      for genParticle in Collection(event,'GenPart'):
        genParticles.append(genParticle)

      genVisTau = []
      for genParticle in Collection(event,'GenVisTau'):
        genVisTau.append(genParticle)

      genTau1, genTau1_daughters = find_true_tau(tau1, genParticles, genVisTau)
      genTau2, genTau2_daughters = find_true_tau(tau2, genParticles, genVisTau)
      gen_tau1_products = dump_tau_products(genTau1_daughters, number_of_products=5)
      gen_tau2_products = dump_tau_products(genTau2_daughters, number_of_products=5)
    
    phi_cp = PhiCP_reco(tau1, tau2, tau_products1, tau_products2)
    if self.ismc:
      phi_cp_true = PhiCP_genReco(tau1, tau2, genParticles, genVisTau)

    '''
    ### FOR TESTS IN TAU -> RHO^pm DECAY ###
    if tau1.decayMode in [1, 2] and tau2.decayMode in [1, 2] and tau1.decayModePNet == 1 and tau2.decayModePNet == 1:
      phi_cp = PhiCP_tautau_reco(tau1, tau2, tau_products1, tau_products2)
      #phi_cp = Polarimetric_phiCP_dm1_dm1_gen(tau1, tau2, fMTT_tau1P4, fMTT_tau2P4, tau_products1, tau_products2, genParticles, genVisTau)
      phi_cp_true = Polarimetric_phiCP_dm1_dm1_reco(tau1, tau2, fMTT_tau1P4, fMTT_tau2P4, tau_products1, tau_products2)
      #phi_cp_true = Polarimetric_better_tau_solution(tau1, tau2, fMTT_tau1P4, fMTT_tau2P4, tau_products1, tau_products2, genParticles, genVisTau)
    else:
      phi_cp = -1
      phi_cp_true = -1
    '''
    
    
    # VETOS
    #extramuon_veto, extraelec_veto, dilepton_veto = getlepvetoes(event,[ ],[ ],[tau1,tau2],self.channel, self.era) #TO_DO
    #self.out.extramuon_veto[0], self.out.extraelec_veto[0], self.out.dilepton_veto[0] = getlepvetoes(event,[ ],[ ],[ ],self.channel,self.era)
    #self.out.lepton_vetoes[0]       = self.out.extramuon_veto[0] or self.out.extraelec_veto[0] #or self.out.dilepton_veto[0]
    #self.out.lepton_vetoes_notau[0] = extramuon_veto or extraelec_veto #or dilepton_veto
    
    
    # EVENT
    self.fillEventBranches(event)
    
    
    # TAU 1
    self.out.pt_1[0]                       = tau1.pt
    self.out.eta_1[0]                      = tau1.eta
    self.out.phi_1[0]                      = tau1.phi
    self.out.m_1[0]                        = tau1.mass
    self.out.y_1[0]                        = tau1.tlv.Rapidity()
    self.out.dxy_1[0]                      = tau1.dxy
    self.out.dz_1[0]                       = tau1.dz
    self.out.q_1[0]                        = tau1.charge
    self.out.dm_1[0]                       = tau1.decayMode
    self.out.dm_PNet_1[0]                 = tau1.decayModePNet
    self.out.iso_1[0]                      = tau1.rawIso
    #self.out.idiso_1[0]                    = idIso(tau1) # cut-based tau isolation (rawIso) #TO_DO
    self.out.rawDeepTau2017v2p1VSe_1[0]    = tau1.rawDeepTau2017v2p1VSe
    self.out.rawDeepTau2017v2p1VSmu_1[0]   = tau1.rawDeepTau2017v2p1VSmu
    self.out.rawDeepTau2017v2p1VSjet_1[0]  = tau1.rawDeepTau2017v2p1VSjet
    #self.out.idAntiEle_1[0]                = tau1.idAntiEle #TO_DO
    #self.out.idAntiMu_1[0]                 = tau1.idAntiMu #TO_DO
    self.out.idDecayMode_1[0]              = tau1.idDecayMode
    self.out.idDecayModeNewDMs_1[0]        = tau1.idDecayModeNewDMs
    #self.out.idMVAoldDM2017v2_1[0]         = tau1.idMVAoldDM2017v2 #TO_DO
    #self.out.idMVAnewDM2017v2_1[0]         = tau1.idMVAnewDM2017v2 #TO_DO
    self.out.idDeepTau2017v2p1VSe_1[0]     = tau1.idDeepTau2017v2p1VSe
    self.out.idDeepTau2017v2p1VSmu_1[0]    = tau1.idDeepTau2017v2p1VSmu
    self.out.idDeepTau2017v2p1VSjet_1[0]   = tau1.idDeepTau2017v2p1VSjet
    #self.out.chargedIso_1[0]               = tau1.chargedIso #TO_DO
    #self.out.neutralIso_1[0]               = tau1.neutralIso #TO_DO
    self.out.leadTkPtOverTauPt_1[0]        = tau1.leadTkPtOverTauPt
    #self.out.photonsOutsideSignalCone_1[0] = tau1.photonsOutsideSignalCone #TO_DO
    #self.out.puCorr_1[0]                   = tau1.puCorr #TO_DO
    
    
    # TAU 2
    self.out.pt_2[0]                       = tau2.pt
    self.out.eta_2[0]                      = tau2.eta
    self.out.phi_2[0]                      = tau2.phi
    self.out.m_2[0]                        = tau2.mass
    self.out.y_2[0]                        = tau2.tlv.Rapidity()
    self.out.dxy_2[0]                      = tau2.dxy
    self.out.dz_2[0]                       = tau2.dz
    self.out.q_2[0]                        = tau2.charge
    self.out.dm_2[0]                       = tau2.decayMode
    self.out.dm_PNet_2[0]                 = tau2.decayModePNet
    self.out.iso_2[0]                      = tau2.rawIso
    #self.out.idiso_2[0]                    = idIso(tau2) # cut-based tau isolation (rawIso) #TO_DO
    self.out.rawDeepTau2017v2p1VSe_2[0]    = tau2.rawDeepTau2017v2p1VSe
    self.out.rawDeepTau2017v2p1VSmu_2[0]   = tau2.rawDeepTau2017v2p1VSmu
    self.out.rawDeepTau2017v2p1VSjet_2[0]  = tau2.rawDeepTau2017v2p1VSjet
    #self.out.idAntiEle_2[0]                = tau2.idAntiEle #TO_DO
    #self.out.idAntiMu_2[0]                 = tau2.idAntiMu #TO_DO
    self.out.idDecayMode_2[0]              = tau2.idDecayMode
    self.out.idDecayModeNewDMs_2[0]        = tau2.idDecayModeNewDMs
    #self.out.idMVAoldDM2017v2_2[0]         = tau2.idMVAoldDM2017v2 #TO_DO
    #self.out.idMVAnewDM2017v2_2[0]         = tau2.idMVAnewDM2017v2 #TO_DO
    self.out.idDeepTau2017v2p1VSe_2[0]     = tau2.idDeepTau2017v2p1VSe
    self.out.idDeepTau2017v2p1VSmu_2[0]    = tau2.idDeepTau2017v2p1VSmu
    self.out.idDeepTau2017v2p1VSjet_2[0]   = tau2.idDeepTau2017v2p1VSjet
    #self.out.chargedIso_2[0]               = tau2.chargedIso #TO_DO
    #self.out.neutralIso_2[0]               = tau2.neutralIso #TO_DO
    self.out.leadTkPtOverTauPt_2[0]        = tau2.leadTkPtOverTauPt
    #self.out.photonsOutsideSignalCone_2[0] = tau2.photonsOutsideSignalCone #TO_DO
    #self.out.puCorr_2[0]                   = tau2.puCorr #TO_DO
    
    
    # GENERATOR
    if self.ismc:
      self.out.genmatch_1[0]     = tau1.genPartFlav
      self.out.genmatch_2[0]     = tau2.genPartFlav
      pt1, eta1, phi1, status1   = matchgenvistau(event,tau1)
      pt2, eta2, phi2, status2   = matchgenvistau(event,tau2)
      self.out.genvistaupt_1[0]  = pt1
      self.out.genvistaueta_1[0] = eta1
      self.out.genvistauphi_1[0] = phi1
      self.out.gendm_1[0]        = status1
      self.out.genvistaupt_2[0]  = pt2
      self.out.genvistaueta_2[0] = eta2
      self.out.genvistauphi_2[0] = phi2
      self.out.gendm_2[0]        = status2
    
    
    # JETS
    jets, met, njets_vars, met_vars = self.fillJetBranches(event,tau1,tau2)
    if self.ismc:
      self.out.jpt_match_1[0], self.out.jpt_genmatch_1[0] = matchtaujet(event,tau1,self.ismc)
      self.out.jpt_match_2[0], self.out.jpt_genmatch_2[0] = matchtaujet(event,tau2,self.ismc)
    
    
    # WEIGHTS
    if self.ismc:
      self.fillCommonCorrBranches(event,jets,met,njets_vars,met_vars)
      if tau1.idDeepTau2017v2p1VSjet>=2 and tau2.idDeepTau2017v2p1VSjet>=2:
        self.btagTool.fillEffMaps(jets,usejec=self.dojec)
      #self.out.trigweight[0]             = self.trigTool.getSFPair(tau1,tau2) #TO_DO
      #self.out.trigweight_tight[0]       = self.trigTool_tight.getSFPair(tau1,tau2) #TO_DO
      #if self.dosys:
      #  self.out.trigweightUp[0]         = self.trigTool.getSFPair(tau1,tau2,unc='Up') #TO_DO
      #  self.out.trigweightDown[0]       = self.trigTool.getSFPair(tau1,tau2,unc='Down') #TO_DO
      
      # DEFAULTS
      self.out.idweight_1[0]        = 1.
      self.out.idweight_2[0]        = 1.
      self.out.idweight_tight_1[0]  = 1.
      self.out.idweight_tight_2[0]  = 1.
      self.out.ltfweight_2[0]       = 1.
      self.out.ltfweight_2[0]       = 1.
      if self.dosys:
        self.out.idweightUp_1[0]    = 1.
        self.out.idweightUp_2[0]    = 1.
        self.out.idweightDown_1[0]  = 1.
        self.out.idweightDown_2[0]  = 1.
        self.out.ltfweightUp_1[0]   = 1.
        self.out.ltfweightUp_2[0]   = 1.
        self.out.ltfweightDown_1[0] = 1.
        self.out.ltfweightDown_2[0] = 1.
      
      if self.era in ["2022EE"]:
        genmatch1 = tau1.genPartFlav
        if genmatch1==5: # real tau
          self.out.idweight_1[0]        = self.deepTauSFTool.sf_vsjet(tau1.pt, tau1.decayMode, genmatch1, self.wp_vsjet, self.wp_vse, self.syst, "pt")
          self.out.idweight_dm_1[0]     = self.deepTauSFTool.sf_vsjet(tau1.pt, tau1.decayMode, genmatch1, self.wp_vsjet, self.wp_vse, self.syst, "dm")
          self.out.idweight_medium_1[0] = 1.0 # for now 
          if self.dosys:
            self.out.idweightUp_1[0]      = self.deepTauSFTool.sf_vsjet(tau1.pt, tau1.decayMode, genmatch1, self.wp_vsjet, self.wp_vse, "up", "pt")
            self.out.idweightDown_1[0]    = self.deepTauSFTool.sf_vsjet(tau1.pt, tau1.decayMode, genmatch1, self.wp_vsjet, self.wp_vse, "down", "pt")
            self.out.idweightUp_dm_1[0]   = self.deepTauSFTool.sf_vsjet(tau1.pt, tau1.decayMode, genmatch1, self.wp_vsjet, self.wp_vse, "up", "dm")
            self.out.idweightDown_dm_1[0] = self.deepTauSFTool.sf_vsjet(tau1.pt, tau1.decayMode, genmatch1, self.wp_vsjet, self.wp_vse, "down", "dm")
        elif genmatch1 in [1,3]: # electron -> tau fake
          self.out.ltfweight_1[0]       = self.deepTauSFTool.sf_vse(tau1.eta, tau1.decayMode, genmatch1, self.wp_vse, self.syst)
          if self.dosys:
            self.out.ltfweightUp_1[0]   = self.deepTauSFTool.sf_vse(tau1.eta, tau1.decayMode, genmatch1, self.wp_vse, "up")
            self.out.ltfweightDown_1[0] = self.deepTauSFTool.sf_vse(tau1.eta, tau1.decayMode, genmatch1, self.wp_vse, "down")
        elif genmatch1 in [2,4]: # muon -> tau fake
          self.out.ltfweight_1[0]       = self.deepTauSFTool.sf_vsmu(tau1.eta, genmatch1, self.wp_vsmu, self.syst)
          if self.dosys:
            self.out.ltfweightUp_1[0]   = self.deepTauSFTool.sf_vsmu(tau1.eta, genmatch1, self.wp_vsmu, "up")
            self.out.ltfweightDown_1[0] = self.deepTauSFTool.sf_vsmu(tau1.eta, genmatch1, self.wp_vsmu, "down")

        genmatch2 = tau2.genPartFlav
        if genmatch2==5: # real tau
          self.out.idweight_2[0]        = self.deepTauSFTool.sf_vsjet(tau2.pt, tau2.decayMode, genmatch2, self.wp_vsjet, self.wp_vse, self.syst, "pt")
          self.out.idweight_dm_2[0]     = self.deepTauSFTool.sf_vsjet(tau2.pt, tau2.decayMode, genmatch2, self.wp_vsjet, self.wp_vse, self.syst, "dm")
          self.out.idweight_medium_2[0] = 1.0 # for now 
          if self.dosys:
            self.out.idweightUp_2[0]      = self.deepTauSFTool.sf_vsjet(tau2.pt, tau2.decayMode, genmatch2, self.wp_vsjet, self.wp_vse, "up", "pt")
            self.out.idweightDown_2[0]    = self.deepTauSFTool.sf_vsjet(tau2.pt, tau2.decayMode, genmatch2, self.wp_vsjet, self.wp_vse, "down", "pt")
            self.out.idweightUp_dm_2[0]   = self.deepTauSFTool.sf_vsjet(tau2.pt, tau2.decayMode, genmatch2, self.wp_vsjet, self.wp_vse, "up", "dm")
            self.out.idweightDown_dm_2[0] = self.deepTauSFTool.sf_vsjet(tau2.pt, tau2.decayMode, genmatch2, self.wp_vsjet, self.wp_vse, "down", "dm")
        elif genmatch2 in [1,3]: # electron -> tau fake
          self.out.ltfweight_2[0]       = self.deepTauSFTool.sf_vse(tau2.eta, tau2.decayMode, genmatch2, self.wp_vse, self.syst)
          if self.dosys:
            self.out.ltfweightUp_2[0]   = self.deepTauSFTool.sf_vse(tau2.eta, tau2.decayMode, genmatch2, self.wp_vse, "up")
            self.out.ltfweightDown_2[0] = self.deepTauSFTool.sf_vse(tau2.eta, tau2.decayMode, genmatch2, self.wp_vse, "down")
        elif genmatch2 in [2,4]: # muon -> tau fake
          self.out.ltfweight_2[0]       = self.deepTauSFTool.sf_vsmu(tau2.eta, genmatch2, self.wp_vsmu, self.syst)
          if self.dosys:
            self.out.ltfweightUp_2[0]   = self.deepTauSFTool.sf_vsmu(tau2.eta, genmatch2, self.wp_vsmu, "up")
            self.out.ltfweightDown_2[0] = self.deepTauSFTool.sf_vsmu(tau2.eta, genmatch2, self.wp_vsmu, "down")  

    # MET & DILEPTON VARIABLES
    self.fillMETAndDiLeptonBranches(event,tau1,tau2,met,met_vars)

    # HIGGS CP
    self.out.tau1_IP0[0] = tau1.IPx
    self.out.tau1_IP1[0] = tau1.IPy
    self.out.tau1_IP2[0] = tau1.IPz

    self.out.tau2_IP0[0] = tau2.IPx
    self.out.tau2_IP1[0] = tau2.IPy
    self.out.tau2_IP2[0] = tau2.IPz

    for i, tau in enumerate(tau1_products_list):
      getattr(self.out, f"tau1_prod{i}_pt")[0]    = tau['pt']
      getattr(self.out, f"tau1_prod{i}_eta")[0]   = tau['eta']
      getattr(self.out, f"tau1_prod{i}_phi")[0]   = tau['phi']
      getattr(self.out, f"tau1_prod{i}_pdgId")[0] = tau['pdgId']

    for i, tau in enumerate(tau2_products_list):
        getattr(self.out, f"tau2_prod{i}_pt")[0]    = tau['pt']
        getattr(self.out, f"tau2_prod{i}_eta")[0]   = tau['eta']
        getattr(self.out, f"tau2_prod{i}_phi")[0]   = tau['phi']
        getattr(self.out, f"tau2_prod{i}_pdgId")[0] = tau['pdgId']

    if self.ismc:
      for i, tau in enumerate(gen_tau1_products):
        getattr(self.out, f"gentau1_prod{i}_pt")[0]    = tau['pt']
        getattr(self.out, f"gentau1_prod{i}_eta")[0]   = tau['eta']
        getattr(self.out, f"gentau1_prod{i}_phi")[0]   = tau['phi']
        getattr(self.out, f"gentau1_prod{i}_pdgId")[0] = tau['pdgId']

      for i, tau in enumerate(gen_tau2_products):
          getattr(self.out, f"gentau2_prod{i}_pt")[0]    = tau['pt']
          getattr(self.out, f"gentau2_prod{i}_eta")[0]   = tau['eta']
          getattr(self.out, f"gentau2_prod{i}_phi")[0]   = tau['phi']
          getattr(self.out, f"gentau2_prod{i}_pdgId")[0] = tau['pdgId']
      
      if genTau1 != None:
        self.out.gentau1_pt[0] = genTau1.pt
        self.out.gentau1_eta[0] = genTau1.eta
        self.out.gentau1_phi[0] = genTau1.phi
      if genTau2 != None: 
        self.out.gentau2_pt[0] = genTau2.pt
        self.out.gentau2_eta[0] = genTau2.eta
        self.out.gentau2_phi[0] = genTau2.phi

    if self.ismc:
      self.out.genPhiCP[0]           = phi_cp_true
    self.out.phiCP[0]               = phi_cp
    
    if self.ismc:
      self.out.tauspinner_weight_even[0] = event.TauSpinner_weight_cp_0
      self.out.tauspinner_weight_odd[0]  = event.TauSpinner_weight_cp_0p5
      self.out.tauspinner_weight_mix[0]  = event.TauSpinner_weight_cp_0p25

    ###FastMTT###

    self.out.fastMTT_X1[0] = X1
    self.out.fastMTT_X2[0] = X2
    
    self.out.fill()
    return True
    
