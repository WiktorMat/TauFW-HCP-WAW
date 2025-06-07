# Author: Izaak Neutelings (June 2020)
# Sources:
#   https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2016#Synchronisation
#   https://cms-nanoaod-integration.web.cern.ch/integration/master-102X/mc102X_doc.html
from TauFW.PicoProducer.analysis.TreeProducerTauPair import TreeProducerTauPair


class TreeProducerMuTau(TreeProducerTauPair):
  """Class to create and prepare a custom output file & tree."""
  
  def __init__(self, filename, module, **kwargs):
    print("Loading TreeProducerMuTau for %r"%(filename))
    super(TreeProducerMuTau,self).__init__(filename,module,**kwargs)
    
    
    ############
    #   MUON   #
    ############
    
    self.addBranch('pt_1',       'f')
    self.addBranch('eta_1',      'f')
    self.addBranch('phi_1',      'f')
    self.addBranch('m_1',        'f')
    self.addBranch('y_1',        'f')
    self.addBranch('dxy_1',      'f')
    self.addBranch('dz_1',       'f')
    self.addBranch('q_1',        'i')
    self.addBranch('iso_1',      'f', title="relative isolation, pfRelIso04_all")
    self.addBranch('tkRelIso_1', 'f')
    self.addBranch('idMedium_1', '?')
    self.addBranch('idTight_1',  '?')
    self.addBranch('idHighPt_1', 'i')
    
    
    ###########
    #   TAU   #
    ###########
    
    self.addBranch('pt_2',                       'f')
    self.addBranch('eta_2',                      'f')
    self.addBranch('phi_2',                      'f')
    self.addBranch('m_2',                        'f')
    self.addBranch('y_2',                        'f')
    self.addBranch('dxy_2',                      'f')
    self.addBranch('dz_2',                       'f')
    self.addBranch('q_2',                        'i')
    self.addBranch('dm_2',                       'i')
    self.addBranch('iso_2',                      'f', title="rawIso")
    self.addBranch('idiso_2',                    'i', title="rawIso WPs")
    #self.addBranch('rawAntiEle_2',               'f') # not available anymore in nanoAODv9
    #self.addBranch('rawMVAoldDM2017v2_2',        'f')
    #self.addBranch('rawMVAnewDM2017v2_2',        'f')
    self.addBranch('rawDeepTau2017v2p1VSe_2',    'f')
    self.addBranch('rawDeepTau2017v2p1VSmu_2',   'f')
    self.addBranch('rawDeepTau2017v2p1VSjet_2',  'f')

    self.addBranch('rawDeepTau2018v2p5VSe_2',    'f')
    self.addBranch('rawDeepTau2018v2p5VSmu_2',   'f')
    self.addBranch('rawDeepTau2018v2p5VSjet_2',  'f')


    #self.addBranch('idAntiEle_2',                'i')
    #self.addBranch('idAntiMu_2',                 'i')
    self.addBranch('idDecayMode_2',              '?', title="oldDecayModeFinding")
    self.addBranch('idDecayModeNewDMs_2',        '?', title="newDecayModeFinding")
    #self.addBranch('idMVAoldDM2017v2_2',         'i')
    #self.addBranch('idMVAnewDM2017v2_2',         'i')
    self.addBranch('idDeepTau2017v2p1VSe_2',     'i')
    self.addBranch('idDeepTau2017v2p1VSmu_2',    'i')
    self.addBranch('idDeepTau2017v2p1VSjet_2',   'i')

    self.addBranch('idDeepTau2018v2p5VSe_2',     'i')
    self.addBranch('idDeepTau2018v2p5VSmu_2',    'i')
    self.addBranch('idDeepTau2018v2p5VSjet_2',   'i')


    self.addBranch('leadTkPtOverTauPt_2',        'f')
    self.addBranch('chargedIso_2',               'f')
    self.addBranch('neutralIso_2',               'f')
    self.addBranch('photonsOutsideSignalCone_2', 'f')
    self.addBranch('puCorr_2',                   'f')
    self.addBranch('jpt_match_2',                'f', -1, title="pt of jet matching tau")
    
    if self.module.ismc:
      self.addBranch('jpt_genmatch_2',      'f', -1, title="pt of gen jet matching tau")
      self.addBranch('genmatch_1',          'i', -1)
      self.addBranch('genmatch_2',          'i', -1)
      self.addBranch('genvistaupt_2',       'f', -1)
      self.addBranch('genvistaueta_2',      'f', -9)
      self.addBranch('genvistauphi_2',      'f', -9)
      self.addBranch('gendm_2',             'i', -1)
      self.addBranch('idisoweight_1',       'f', 1., title="muon ID/iso efficiency SF")
      self.addBranch('idweight_2',          'f', 1., title="tau ID efficiency SF, Tight") #genmatch=5, real tau
      self.addBranch('idweight_dm_2',       'f', 1., title="tau ID efficiency SF, Tight, DM-dependent") #genmatch=5, real tau
      self.addBranch('idweight_medium_2',   'f', 1., title="tau ID efficiency SF, Medium") #genmatch=5, real tau
      self.addBranch('ltfweight_2',         'f', 1., title="lepton -> tau fake rate SF") #genmatch=1, 3 -> e or 2, 4 -> mu 
      self.addBranch('tau_pt_preSF',      'f', title="no correction applied to tau pt")
      self.addBranch('tes_sf',      'f', title="tau energy scale correction")
      self.addBranch('trigweight_2',      'f', title="tau trigger efficiency SF") 
      if self.module.dosys: # systematic variation (only for nominal tree)
        self.addBranch('idweightUp_2',      'f', 1.)
        self.addBranch('idweightDown_2',    'f', 1.)
        self.addBranch('idweightUp_dm_2',   'f', 1.)
        self.addBranch('idweightDown_dm_2', 'f', 1.)
        self.addBranch('ltfweightUp_2',     'f', 1.)
        self.addBranch('ltfweightDown_2',   'f', 1.)
      if self.module.domutau:
        self.addBranch('mutaufilter',       '?', title="has tautau -> mutau, pT>18, |eta|<2.5")

    
        
    #############
    #  HiggsCP  #
    #############

    for i in range(5):
      self.addBranch(f"tau_prod{i}_pt",    'f', -1, title=f"Transverse momentum of tau product {i}")
      self.addBranch(f"tau_prod{i}_eta",   'f', -1, title=f"Eta of tau product {i}")
      self.addBranch(f"tau_prod{i}_phi",   'f', -1, title=f"Phi of tau product {i}")
      self.addBranch(f"tau_prod{i}_pdgId", 'i', -1, title=f"PDG ID of tau product {i}")

    for i in range(3):
      self.addBranch(f"tau2_prod{i}_pt",    'f', -1, title=f"Transverse momentum of tau2 product {i}")
    for i in range(5):
      self.addBranch(f"gentau_prod{i}_pt",    'f', -1, title=f"Transverse momentum of generated tau product {i}")
      self.addBranch(f"gentau_prod{i}_eta",   'f', -1, title=f"Eta of generated tau product {i}")
      self.addBranch(f"gentau_prod{i}_phi",   'f', -1, title=f"Phi of generated tau product {i}")
      self.addBranch(f"gentau_prod{i}_pdgId", 'i', -1, title=f"PDG ID of generated tau product {i}")

    for i in range(3):

      self.addBranch(f"genmutau_prod{i}_pt",    'f', -1, title=f"Transverse momentum of generated tau product {i} in muonic tau decay channel")
      self.addBranch(f"genmutau_prod{i}_eta",   'f', -1, title=f"Eta of generated tau product {i} in muonic tau decay channel")
      self.addBranch(f"genmutau_prod{i}_phi",   'f', -1, title=f"Phi of generated tau product {i} in muonic tau decay channel")
      self.addBranch(f"genmutau_prod{i}_pdgId", 'i', -1, title=f"PDG ID of generated tau product {i} in muonic tau decay channel")

    self.addBranch('gentau_pt',    'f', -1, title="pt of generated hadronic tau")
    self.addBranch('gentau_eta',   'f', -1, title="eta of generated hadronic tau")
    self.addBranch('gentau_phi',   'f', -1, title="phi of generated hadronic tau")
    self.addBranch('genmutau_pt',  'f', -1, title="pt of generated muonic tau")
    self.addBranch('genmutau_eta', 'f', -1, title="eta of generated muonic tau")
    self.addBranch('genmutau_phi', 'f', -1, title="phi of generated muonic tau")

    self.addBranch('mu_IP0', 'f', -1, title="Impact parameter of first tau, x-axis")
    self.addBranch('mu_IP1', 'f', -1, title="Impact parameter of first tau, y-axis")
    self.addBranch('mu_IP2', 'f', -1, title="Impact parameter of first tau, z-axis")
    
    self.addBranch('tau_IP0', 'f', -1, title="Impact parameter of second tau, x-axis")
    self.addBranch('tau_IP1', 'f', -1, title="Impact parameter of second tau, y-axis")
    self.addBranch('tau_IP2', 'f', -1, title="Impact parameter of second tau, z-axis")

    self.addBranch('phiCP', 'f', -1, title="Measured violation of CP symmetry in H->tautau decay")
    self.addBranch('genphiCP', 'f', -1, title="Acoplanarity angle (sensitive to CP violation) in H->tautau decay, reconstructed from gen-level information. Result should be reweighed with tau spinner weights")

    self.addBranch('tauspinner_weight_even', 'f', -1, title="Tau spinner weight for CP even hypothesis")
    self.addBranch('tauspinner_weight_odd', 'f', -1, title="Tau spinner weight for CP odd hypothesis")
    self.addBranch('tauspinner_weight_mix', 'f', -1, title="Tau spinner weight for mixed CP hypothesis")

    #############
    #  FastMTT  #
    #############

    self.addBranch('fastMTT_X1', 'f', -1, title="Fraction of first tau energy carried by its visible products. Calculated with the fastMTT algorithm with window constraint.")
    self.addBranch('fastMTT_X2', 'f', -1, title="Fraction of second tau energy carried by its visible products. Calculated with the fastMTT algorithm with window constraint.")
