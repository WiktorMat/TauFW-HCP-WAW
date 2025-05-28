import math
import ROOT
import numpy as np
from TauFW.PicoProducer.analysis.HiggsCPtools.Utils import *
from TauFW.PicoProducer.analysis.HiggsCPtools.GenParticles import *
from TauFW.PicoProducer.analysis.HiggsCPtools.Kinematics_reconstructions import *
from TauFW.PicoProducer.analysis.HiggsCPtools.tau_reconstruction import *
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

def Polarimetric_phiCP_dm1_dm1_reco(tau1, tau2, tauP4_fMTT1, tauP4_fMTT2, tau1Prod, tau2Prod):

    tau1_vec, _, cp1_4momentum = Tau_momentum_reconstruction(tau1, tauP4_fMTT1, tau1Prod)
    tau2_vec, _, cp2_4momentum = Tau_momentum_reconstruction(tau2, tauP4_fMTT2, tau2Prod)

    if tau1_vec is None or tau2_vec is None:
        return -1
    
    tau1_reco = ROOT.TLorentzVector()
    tau1_reco.SetVectM(tau1_vec, TAU_MASS)

    tau2_reco = ROOT.TLorentzVector()
    tau2_reco.SetVectM(tau2_vec, TAU_MASS)

    np1_4momentum = get_neutralPion_4momentum(tau1Prod)
    np2_4momentum = get_neutralPion_4momentum(tau2Prod)

    helicity1 = Helicity_Rho(cp1_4momentum, np1_4momentum, tau1_reco)
    helicity2 = Helicity_Rho(cp2_4momentum, np2_4momentum, tau2_reco)

    First_negative = tau1.charge < 0
    phi_CP = acoCP(helicity1, helicity2, tau1_reco, tau2_reco, First_negative)
    return phi_CP

def get_genPions_taons(tau1, tau2, genParticles, genVisTau):
    genTau1, genTau1_daughters = find_true_tau(tau1, genParticles, genVisTau)
    genTau2, genTau2_daughters = find_true_tau(tau2, genParticles, genVisTau)

    charged_pions1 = []
    neutral_pions1 = []
    neutrinos1 = []
    for daugther in genTau1_daughters:
        if abs(daugther.pdgId) == 211:
            charged_pions1.append(daugther)
        elif abs(daugther.pdgId) == 111:
            neutral_pions1.append(daugther)
        elif abs(daugther.pdgId) == 12 or abs(daugther.pdgId) == 14 or abs(daugther.pdgId) == 16:
            neutrinos1.append(daugther)
    
    charged_pions2 = []
    neutral_pions2 = []
    neutrinos2 = []
    for daugther in genTau2_daughters:
        if abs(daugther.pdgId) == 211:
            charged_pions2.append(daugther)
        elif abs(daugther.pdgId) == 111:
            neutral_pions2.append(daugther)
        elif abs(daugther.pdgId) == 12 or abs(daugther.pdgId) == 14 or abs(daugther.pdgId) == 16:
            neutrinos2.append(daugther)

    if genTau1 is None or genTau2 is None:
        print("No gen-level match for this tau.")
        return None, None, None, None, None, None
    
    tau1_negative = genTau1.pdgId == 15
    tau2_negative = genTau2.pdgId == 15
    if (tau1_negative and tau2_negative) or (not tau1_negative and not tau2_negative):
        print("Both taus are negative or positive.")
        return None, None, None, None, None, None
    
    return charged_pions1, neutral_pions1, charged_pions2, neutral_pions2, genTau1, genTau2


###Testing function to try how impactful are the wrong choices of the reconstructed taus

def Polarimetric_better_tau_solution(tau1, tau2, tauP4_fMTT1, tauP4_fMTT2, tau1Prod, tau2Prod, genParticles, genVisTau):

    gencharged1, genneutral1, gencharged2, genneutral2, gentau1, gentau2 = get_genPions_taons(tau1, tau2, genParticles, genVisTau)
    
    if gencharged1 is None or genneutral1 is None or gencharged2 is None or genneutral2 is None:
        return -1

    tau1_gen = get_lepton_4momentum(gentau1)
    tau2_gen = get_lepton_4momentum(gentau2)

    tau1_vec, tau1_worse, cp1_4momentum = Tau_momentum_reconstruction(tau1, tauP4_fMTT1, tau1Prod)
    tau2_vec, tau2_worse, cp2_4momentum = Tau_momentum_reconstruction(tau2, tauP4_fMTT2, tau2Prod)

    if tau1_vec is None or tau2_vec is None:
        return -1
    
    # Create TLorentzVectors from XYZVectors (or ROOT TVector3)
    tau1_candidate1 = ROOT.TLorentzVector()
    tau1_candidate1.SetVectM(tau1_vec, TAU_MASS)

    tau1_candidate2 = ROOT.TLorentzVector()
    tau1_candidate2.SetVectM(tau1_worse, TAU_MASS)

    tau2_candidate1 = ROOT.TLorentzVector()
    tau2_candidate1.SetVectM(tau2_vec, TAU_MASS)

    tau2_candidate2 = ROOT.TLorentzVector()
    tau2_candidate2.SetVectM(tau2_worse, TAU_MASS)

    # Choose the closer one to the gen tau based on ∆R or p4 distance
    def choose_better_reco(candidate1, candidate2, gen):
        d1 = candidate1.DeltaR(gen)
        d2 = candidate2.DeltaR(gen)
        return candidate1 if d1 < d2 else candidate2

    tau1_reco = choose_better_reco(tau1_candidate1, tau1_candidate2, tau1_gen)
    tau2_reco = choose_better_reco(tau2_candidate1, tau2_candidate2, tau2_gen)

    np1_4momentum = get_neutralPion_4momentum(tau1Prod)
    np2_4momentum = get_neutralPion_4momentum(tau2Prod)

    helicity1 = Helicity_Rho(cp1_4momentum, np1_4momentum, tau1_reco)
    helicity2 = Helicity_Rho(cp2_4momentum, np2_4momentum, tau2_reco)

    First_negative = tau1.charge < 0
    phi_CP = acoCP(helicity1, helicity2, tau1_reco, tau2_reco, First_negative)
    return phi_CP

def Polarimetric_phiCP_dm1_dm1_gen(tau1, tau2, tauP4_fMTT1, tauP4_fMTT2, tau1Prod, tau2Prod, genParticles, genVisTau):

    #tau1_reco_3momentum, cp1_4momentum = Tau_momentum_reconstruction(tau1, tauP4_fMTT1, tau1Prod)
    #tau2_reco_3momentum, cp2_4momentum = Tau_momentum_reconstruction(tau2, tauP4_fMTT2, tau2Prod)

    gencharged1, genneutral1, gencharged2, genneutral2, gentau1, gentau2 = get_genPions_taons(tau1, tau2, genParticles, genVisTau)

    if gencharged1 is None or genneutral1 is None or gencharged2 is None or genneutral2 is None:
        return -1

    if len(gencharged1) == 1 and len(genneutral1) == 1 and len(gencharged2) == 1 and len(genneutral2) == 1:
        cp1_4momentum = get_lepton_4momentum(gencharged1[0])
        cp2_4momentum = get_lepton_4momentum(gencharged2[0])
        np1_4momentum = get_lepton_4momentum(genneutral1[0])
        np2_4momentum = get_lepton_4momentum(genneutral2[0])
        tau1_reco = get_lepton_4momentum(gentau1)
        tau2_reco = get_lepton_4momentum(gentau2)
    else:
        return -1

    if tau1_reco is None or tau2_reco is None:
        return -1

    helicity1 = Helicity_Rho(cp1_4momentum, np1_4momentum, tau1_reco)
    helicity2 = Helicity_Rho(cp2_4momentum, np2_4momentum, tau2_reco)

    First_negative = tau1.charge < 0
    phi_CP = acoCP(helicity1, helicity2, tau1_reco, tau2_reco, First_negative)
    return phi_CP


def find_restframe_root(p4):
    return ROOT.TVector3(-p4.BoostVector())

def Helicity_Rho(tempPi, tempPi0, tauP4):

    tempQ = tempPi - tempPi0
    NN = tauP4 - tempPi - tempPi0
    tempN = ROOT.TLorentzVector()

    tempN.SetPtEtaPhiM(NN.Pt(),NN.Eta(),NN.Phi(),0.)

    X1 = tempQ.E()*tempN.E()-tempQ.Px()*tempN.Px()-tempQ.Py()*tempN.Py()-tempQ.Pz()*tempN.Pz()
    X2 = tempQ.E()*tempQ.E()-tempQ.Px()*tempQ.Px()-tempQ.Py()*tempQ.Py()-tempQ.Pz()*tempQ.Pz()
    tempPV = X1*tempQ-X2*tempN

    pv = ROOT.TLorentzVector()
    pv.SetXYZT(tempPV.X(),tempPV.Y(),tempPV.Z(),tempPV.T())
    
    return pv

def acoCP(P1, P2, R1, R2, firstNeg):

    Prongsum = P1 + P2
    boost = -Prongsum.BoostVector()
    
    P1.Boost(boost)
    P2.Boost(boost)
    R1.Boost(boost)
    R2.Boost(boost)
    
    vecP1 = P1.Vect().Unit()
    vecP2 = P2.Vect().Unit()
    vecR1 = R1.Vect()
    vecR2 = R2.Vect()

    R1transv = vecR1 - vecP1*(vecP1.Dot(vecR1))
    R2transv = vecR2 - vecP2*(vecP2.Dot(vecR2))

    n1 = R1transv.Unit()
    n2 = R2transv.Unit()

    cos_phi = n1.Dot(n2)
    acop = math.acos(cos_phi)

    sign = vecP2.Dot(n1.Cross(n2))
    
    if firstNeg:
        sign = vecP1.Dot(n2.Cross(n1))

    if sign<0:
        acop = 2.0*ROOT.TMath.Pi() - acop

    return acop