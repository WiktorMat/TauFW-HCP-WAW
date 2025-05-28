import vector
import numpy as np
from TauFW.PicoProducer.analysis.HiggsCPtools.Utils import *
from TauFW.PicoProducer.analysis.HiggsCPtools.GenParticles import *
from TauFW.PicoProducer.analysis.HiggsCPtools.Kinematics_reconstructions import *

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import ROOT
import math

def get_genPions(tau1, tau2, genParticles, genVisTau):
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
        return None, None, None, None
    
    tau1_negative = genTau1.pdgId == 15
    tau2_negative = genTau2.pdgId == 15
    if (tau1_negative and tau2_negative) or (not tau1_negative and not tau2_negative):
        print("Both taus are negative or positive.")
        return None, None, None, None
    
    return charged_pions1, neutral_pions1, charged_pions2, neutral_pions2

def PhiCP_tautau_genReco(tau1, tau2, genParticles, genVisTau):

    charged1, neutral1, charged2, neutral2 = get_genPions(tau1, tau2, genParticles, genVisTau)

    if charged1 is None or neutral1 is None or charged2 is None or neutral2 is None:
        return -1

    p1, lambda1, y1 = get_pion_and_lambda(tau1, charged1, neutral1)
    if p1 is None or lambda1 is None:
        return -1

    p2, lambda2, y2 = get_pion_and_lambda(tau2, charged2, neutral2)
    if p2 is None or lambda2 is None:
        return -1
    
    y = y1*y2
    
    firstNeg = tau1.charge < 0
    
    phi_cp = acoCP(p1, p2, lambda1, lambda2, firstNeg, y)
    
    return phi_cp

def acoCP(P1, P2, R1, R2, firstNeg, y):

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

    if y<0:
        acop = acop + ROOT.TMath.Pi()

    if sign<0:
        acop = 2.0*ROOT.TMath.Pi() - acop

    acop %= 2.0*ROOT.TMath.Pi()

    return acop


def get_pion_and_lambda(tau, charged, neutral):
    # Method 1: only charged pion, IP method
    if len(charged) == 1 and len(neutral) == 0:
        best_p = get_lepton_4momentum(charged[0])  # TLorentzVector
        lambda_vec = get_lambda(tau)  # TLorentzVector

        if lambda_vec.Mag() == 0:
            print("No impact parameter!")
            return None, None, None
        
        y = 1

    # Method 2: 1 charged, 1 neutral pion, Decay-Plane method
    elif len(charged) == 1 and len(neutral) == 1:
        best_p = get_lepton_4momentum(charged[0])
        lambda_vec = get_lepton_4momentum(neutral[0])
        y = best_p.E() - lambda_vec.E()

    # Method 3: 3 charged (via rho0), 0 neutral pions, Decay-Plane method
    elif len(charged) == 3 and len(neutral) == 0:
        best_p, lambda_vec = get_charged_pion_from_rho_decay(charged, tau.charge)
        if best_p is None:
            return None, None, None
        y = best_p.E() - lambda_vec.E()

    # Other decay channels not implemented
    else:
        return None, None, None

    return best_p, lambda_vec, y