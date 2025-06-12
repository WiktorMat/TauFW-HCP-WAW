# Author: Izaak Neutelings (June 2020)
# Sources:
#   https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2016#Synchronisation
#   https://cms-nanoaod-integration.web.cern.ch/integration/master-102X/mc102X_doc.html
from TauFW.PicoProducer.analysis.TreeProducerTauPair import TreeProducerTauPair


class TreeProducerTauTau(TreeProducerTauPair):
  """Class to create and prepare a custom output file & tree."""
  
  def __init__(self, filename, module, **kwargs):
    print("Loading TreeProducerTauTau for %r"%(filename))
    super(TreeProducerTauTau,self).__init__(filename,module,**kwargs)
    
        
    #############
    #   TAU 1   #
    #############
    
    self.addBranch('pt_1',                       'f')
    self.addBranch('eta_1',                      'f')
    self.addBranch('phi_1',                      'f')
    self.addBranch('m_1',                        'f')
    self.addBranch('y_1',                        'f')
    self.addBranch('dxy_1',                      'f')
    self.addBranch('dz_1',                       'f')
    self.addBranch('q_1',                        'i')
    self.addBranch('dm_1',                       'i')
    self.addBranch('dm_PNet_1',                       'i')
    self.addBranch('iso_1',                      'f', title="rawIso")
    self.addBranch('idiso_1',                    'i', title="rawIso WPs")
    self.addBranch('rawDeepTau2017v2p1VSe_1',    'f')
    self.addBranch('rawDeepTau2017v2p1VSmu_1',   'f')
    self.addBranch('rawDeepTau2017v2p1VSjet_1',  'f')
    self.addBranch('idAntiEle_1',                'i')
    self.addBranch('idAntiMu_1',                 'i')
    self.addBranch('idDecayMode_1',              '?', title="oldDecayModeFinding")
    self.addBranch('idDecayModeNewDMs_1',        '?', title="newDecayModeFinding")
    self.addBranch('idMVAoldDM2017v2_1',         'i')
    self.addBranch('idMVAnewDM2017v2_1',         'i')
    self.addBranch('idDeepTau2017v2p1VSe_1',     'i')
    self.addBranch('idDeepTau2017v2p1VSmu_1',    'i')
    self.addBranch('idDeepTau2017v2p1VSjet_1',   'i')
    self.addBranch('leadTkPtOverTauPt_1',        'f')
    self.addBranch('chargedIso_1',               'f')
    self.addBranch('neutralIso_1',               'f')
    self.addBranch('photonsOutsideSignalCone_1', 'f')
    self.addBranch('puCorr_1',                   'f')
    self.addBranch('jpt_match_1',                'f', -1, title="pt of jet matching tau")
    
        
    #############
    #   TAU 2   #
    #############
    
    self.addBranch('pt_2',                       'f')
    self.addBranch('eta_2',                      'f')
    self.addBranch('phi_2',                      'f')
    self.addBranch('m_2',                        'f')
    self.addBranch('y_2',                        'f')
    self.addBranch('dxy_2',                      'f')
    self.addBranch('dz_2',                       'f')
    self.addBranch('q_2',                        'i')
    self.addBranch('dm_2',                       'i')
    self.addBranch('dm_PNet_2',                       'i')
    self.addBranch('iso_2',                      'f', title="rawIso")
    self.addBranch('idiso_2',                    'i', title="rawIso WPs")
    self.addBranch('rawDeepTau2017v2p1VSe_2',    'f')
    self.addBranch('rawDeepTau2017v2p1VSmu_2',   'f')
    self.addBranch('rawDeepTau2017v2p1VSjet_2',  'f')
    self.addBranch('idAntiEle_2',                'i')
    self.addBranch('idAntiMu_2',                 'i')
    self.addBranch('idDecayMode_2',              '?', title="oldDecayModeFinding")
    self.addBranch('idDecayModeNewDMs_2',        '?', title="newDecayModeFinding")
    self.addBranch('idMVAoldDM2017v2_2',         'i')
    self.addBranch('idMVAnewDM2017v2_2',         'i')
    self.addBranch('idDeepTau2017v2p1VSe_2',     'i')
    self.addBranch('idDeepTau2017v2p1VSmu_2',    'i')
    self.addBranch('idDeepTau2017v2p1VSjet_2',   'i')
    self.addBranch('leadTkPtOverTauPt_2',        'f')
    self.addBranch('chargedIso_2',               'f')
    self.addBranch('neutralIso_2',               'f')
    self.addBranch('photonsOutsideSignalCone_2', 'f')
    self.addBranch('puCorr_2',                   'f')
    self.addBranch('jpt_match_2',                'f', -1, title="pt of jet matching tau")
    
    if self.module.ismc:
      self.addBranch('jpt_genmatch_1',           'f', -1, title="pt of gen jet matching tau")
      self.addBranch('jpt_genmatch_2',           'f', -1, title="pt of gen jet matching tau")
      self.addBranch('genmatch_1',               'i', -1)
      self.addBranch('genmatch_2',               'i', -1)
      self.addBranch('genvistaupt_1',            'f', -1)
      self.addBranch('genvistaupt_2',            'f', -1)
      self.addBranch('genvistaueta_1',           'f', -9)
      self.addBranch('genvistaueta_2',           'f', -9)
      self.addBranch('genvistauphi_1',           'f', -9)
      self.addBranch('genvistauphi_2',           'f', -9)
      self.addBranch('gendm_1',                  'i', -1)
      self.addBranch('gendm_2',                  'i', -1)
      self.addBranch('trigweight_tight',         'f', 1.)
      self.addBranch('idweight_1',               'f', 1., title="tau ID efficiency SF")
      self.addBranch('idweight_2',               'f', 1., title="tau ID efficiency SF")
      self.addBranch('idweight_tight_1',         'f', 1., title="tau ID efficiency SF")
      self.addBranch('idweight_tight_2',         'f', 1., title="tau ID efficiency SF")
      self.addBranch('ltfweight_1',              'f', 1., title="lepton -> tau fake rate SF")
      self.addBranch('ltfweight_2',              'f', 1., title="lepton -> tau fake rate SF")
      if module.dosys: # systematic variation (only for nominal tree)
        self.addBranch('idweightUp_1',           'f', 1.)
        self.addBranch('idweightUp_2',           'f', 1.)
        self.addBranch('idweightDown_1',         'f', 1.)
        self.addBranch('idweightDown_2',         'f', 1.)
        self.addBranch('ltfweightUp_1',          'f', 1.)
        self.addBranch('ltfweightUp_2',          'f', 1.)
        self.addBranch('ltfweightDown_1',        'f', 1.)
        self.addBranch('ltfweightDown_2',        'f', 1.)
    
    #############
    #  HiggsCP  #
    #############

    for i in range(5):
      self.addBranch(f"tau1_prod{i}_pt",    'f', -1, title=f"Transverse momentum of tau1 product {i}")
      self.addBranch(f"tau1_prod{i}_eta",   'f', -1, title=f"Eta of tau1 product {i}")
      self.addBranch(f"tau1_prod{i}_phi",   'f', -1, title=f"Phi of tau1 product {i}")
      self.addBranch(f"tau1_prod{i}_pdgId", 'i', -1, title=f"PDG ID of tau1 product {i}")

      self.addBranch(f"tau2_prod{i}_pt",    'f', -1, title=f"Transverse momentum of tau2 product {i}")
      self.addBranch(f"tau2_prod{i}_eta",   'f', -1, title=f"Eta of tau2 product {i}")
      self.addBranch(f"tau2_prod{i}_phi",   'f', -1, title=f"Phi of tau2 product {i}")
      self.addBranch(f"tau2_prod{i}_pdgId", 'i', -1, title=f"PDG ID of tau2 product {i}")

    for i in range(7):
      self.addBranch(f"gentau1_prod{i}_pt",    'f', -1, title=f"Transverse momentum of generated tau1 product {i}")
      self.addBranch(f"gentau1_prod{i}_eta",   'f', -1, title=f"Eta of generated tau1 product {i}")
      self.addBranch(f"gentau1_prod{i}_phi",   'f', -1, title=f"Phi of generated tau1 product {i}")
      self.addBranch(f"gentau1_prod{i}_pdgId", 'i', -1, title=f"PDG ID of generated tau1 product {i}")

      self.addBranch(f"gentau2_prod{i}_pt",    'f', -1, title=f"Transverse momentum of generated tau2 product {i}")
      self.addBranch(f"gentau2_prod{i}_eta",   'f', -1, title=f"Eta of generated tau2 product {i}")
      self.addBranch(f"gentau2_prod{i}_phi",   'f', -1, title=f"Phi of generated tau2 product {i}")
      self.addBranch(f"gentau2_prod{i}_pdgId", 'i', -1, title=f"PDG ID of generated tau2 product {i}")

    self.addBranch('gentau1_pt',    'f', -1, title="pt of generated tau1")
    self.addBranch('gentau1_eta',   'f', -1, title="eta of generated tau1")
    self.addBranch('gentau1_phi',   'f', -1, title="phi of generated tau1")
    self.addBranch('gentau2_pt',  'f', -1, title="pt of generated tau2")
    self.addBranch('gentau2_eta', 'f', -1, title="eta of generated tau2")
    self.addBranch('gentau2_phi', 'f', -1, title="phi of generated tau2")

    self.addBranch('tau1_IP0', 'f', -1, title="Impact parameter of first tau, x-axis")
    self.addBranch('tau1_IP1', 'f', -1, title="Impact parameter of first tau, y-axis")
    self.addBranch('tau1_IP2', 'f', -1, title="Impact parameter of first tau, z-axis")
    
    self.addBranch('tau2_IP0', 'f', -1, title="Impact parameter of second tau, x-axis")
    self.addBranch('tau2_IP1', 'f', -1, title="Impact parameter of second tau, y-axis")
    self.addBranch('tau2_IP2', 'f', -1, title="Impact parameter of second tau, z-axis")

    self.addBranch('phiCP', 'f', -1, title="Measured/reconstructed acoplanarity angle (sensitive to CP violation) in H->tautau decay. Result should be reweighed with tau spinner weights.")
    self.addBranch('genPhiCP', 'f', -1, title="Acoplanarity angle (sensitive to CP violation) in H->tautau decay, reconstructed from gen-level information. Result should be reweighed with tau spinner weights.")

    self.addBranch('tauspinner_weight_even', 'f', -1, title="Tau spinner weight for CP even hypothesis")
    self.addBranch('tauspinner_weight_odd', 'f', -1, title="Tau spinner weight for CP odd hypothesis")
    self.addBranch('tauspinner_weight_mix', 'f', -1, title="Tau spinner weight for mixed CP hypothesis")

    #############
    #  FastMTT  #
    #############

    self.addBranch('fastMTT_X1', 'f', -1, title="Fraction of first tau energy carried by its visible products. Calculated with the fastMTT algorithm with window constraint.")
    self.addBranch('fastMTT_X2', 'f', -1, title="Fraction of second tau energy carried by its visible products. Calculated with the fastMTT algorithm with window constraint.")