import vector
import numpy as np
from TauFW.PicoProducer.analysis.HiggsCPtools.Utils import *
from TauFW.PicoProducer.analysis.HiggsCPtools.GenParticles import *

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

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
    
    beta_zmf = find_restframe(p1+p2)

    lambda1_zmf = lambda1.boost(beta_zmf)
    lambda2_zmf = lambda2.boost(beta_zmf)
    p1_zmf = p1.boost(beta_zmf)
    p2_zmf = p2.boost(beta_zmf)

    lambda1_spatial = lambda1_zmf.to_xyz()
    lambda2_spatial = lambda2_zmf.to_xyz()
    p1_spatial = p1_zmf.to_xyz().unit()
    p2_spatial = p2_zmf.to_xyz().unit()

    # Perpendicular component (and normalization)
    lambda1_perp = get_perpendicular_component(lambda1_spatial, p1_spatial)
    lambda2_perp = get_perpendicular_component(lambda2_spatial, p2_spatial)

    y = y1*y2

    if tau1.charge == 1 and tau2.charge == -1:
        phi_cp = Calculate_PhiCP(lambda1_perp, lambda2_perp, p1_spatial, p2_spatial, y)
    elif tau1.charge == -1 and tau2.charge == 1:
        phi_cp = Calculate_PhiCP(lambda2_perp, lambda1_perp, p2_spatial, p1_spatial, y)
    else:
        return -1
    
    if isinstance(phi_cp, np.ndarray):
        phi_cp = phi_cp.item()
    return phi_cp

def Calculate_PhiCP(lambda1, lambda2, p1_zmf, p2_zmf, y):
    
    phi_zmf = np.arccos(lambda1.dot(lambda2))

    O_zmf = p2_zmf.dot(lambda1.cross(lambda2))
    phi_cp = np.where(O_zmf >= 0, phi_zmf, 2 * np.pi - phi_zmf)

    if y < 0:
        phi_cp += np.pi
        phi_cp %= 2 * np.pi

    return phi_cp

def find_restframe(momentum):
        beta = {
            "px": float(-momentum.px / momentum.E),
            "py": float(-momentum.py / momentum.E),
            "pz": float(-momentum.pz / momentum.E),
        }
        return vector.obj(**beta)


def get_pion_and_lambda(tau, charged, neutral):
    
    if len(charged) == 1 and len(neutral) == 0:
        best_p = get_lepton_4momentum(charged[0])
        lambda_vec = get_lambda(tau)
        y = 1
        if lambda_vec.mag == 0: ###TEMPORARY###
            print("No impact parameter!")
            return None, None, None
        
    elif len(charged) == 1 and len(neutral) == 1:
        best_p = get_lepton_4momentum(charged[0])
        lambda_vec = get_lepton_4momentum(neutral[0])
        y = best_p.E - lambda_vec.E

    elif len(charged) == 3 and len(neutral) == 0:
        best_p, lambda_vec = get_charged_pion_from_rho_decay(charged, tau.charge)
        if best_p is None:
            return None, None, None
        y = best_p.E - lambda_vec.E

    else:
        return None, None, None
    
    return best_p, lambda_vec, y

def get_charged_pion_from_rho_decay(pions, tau_charge):
    pi_pluses = [p for p in pions if p.pdgId == 211]
    pi_minuses = [p for p in pions if p.pdgId == -211]

    best_pair = None
    min_mass_diff = float("inf")

    for pi_plus in pi_pluses:
        pi_plus_p = np.array([
            pi_plus.pt * np.cos(pi_plus.phi),
            pi_plus.pt * np.sin(pi_plus.phi),
            pi_plus.pt * np.sinh(pi_plus.eta)
        ])
        pi_plus_E = np.sqrt(pi_plus.pt**2 * np.cosh(pi_plus.eta)**2 + PI_PLUS_MASS**2)

        for pi_minus in pi_minuses:
            pi_minus_p = np.array([
                pi_minus.pt * np.cos(pi_minus.phi),
                pi_minus.pt * np.sin(pi_minus.phi),
                pi_minus.pt * np.sinh(pi_minus.eta)
            ])
            pi_minus_E = np.sqrt(pi_minus.pt**2 * np.cosh(pi_minus.eta)**2 + PI_PLUS_MASS**2)

            # Invariant mass of 'Rho_0 system' candidate
            rho_p = pi_plus_p + pi_minus_p
            rho_E = pi_plus_E + pi_minus_E
            rho_mass = np.sqrt(rho_E**2 - np.dot(rho_p, rho_p))

            #print(f"ρ⁰ mass candidate: {rho_mass:.4f} GeV")

            # Check wich mass is closest to Rho(770)
            mass_diff = abs(rho_mass - RHO_ZERO_MASS)
            if mass_diff < min_mass_diff:
                min_mass_diff = mass_diff
                best_pair = (
                    vector.obj(px=pi_plus_p[0], py=pi_plus_p[1], pz=pi_plus_p[2], E=pi_plus_E),
                    vector.obj(px=pi_minus_p[0], py=pi_minus_p[1], pz=pi_minus_p[2], E=pi_minus_E)
                )

    if best_pair is None:
        print("No valid pion pairs found!")
        return None, None

    return best_pair if tau_charge == 1 else best_pair[::-1]