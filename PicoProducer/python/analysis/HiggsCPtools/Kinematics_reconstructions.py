import ROOT
import math
import numpy as np
from TauFW.PicoProducer.analysis.HiggsCPtools.Utils import *

import warnings
warnings.filterwarnings("ignore", category=UserWarning)
    
def get_neutralPion_4momentum(tau_products):
    energy = 0.0
    leading_momentum = [0.0, 0.0, 0.0]  # Normalized direction
    leading_energy = 0.0

    for product in tau_products:
        abs_pdgId = abs(product.pdgId)
        eta = product.eta
        phi = product.phi
        pt = product.pt

        if abs_pdgId == 11:
            product_energy = math.sqrt(pt**2 * math.cosh(eta)**2 + ELECTRON_MASS**2)
        elif product.pdgId == 22:
            product_energy = pt * math.cosh(eta)
        else:
            continue

        energy += product_energy

        if product_energy > leading_energy:
            leading_energy = product_energy
            leading_momentum[0] = math.cos(phi) / math.cosh(eta)
            leading_momentum[1] = math.sin(phi) / math.cosh(eta)
            leading_momentum[2] = math.tanh(eta)

    total_momentum = math.sqrt(max(0.0, energy**2 - PI_ZERO_MASS**2))  # avoid sqrt of negative

    leading_momentum = [x * total_momentum for x in leading_momentum]

    pion_vec = ROOT.TLorentzVector()
    pion_vec.SetPxPyPzE(leading_momentum[0], leading_momentum[1], leading_momentum[2], energy)

    return pion_vec

def get_charged_pion_from_rho_decay(pions, tau_charge):
    pi_pluses = [p for p in pions if p.pdgId == 211]
    pi_minuses = [p for p in pions if p.pdgId == -211]

    best_pair = None
    min_mass_diff = float("inf")

    for pi_plus in pi_pluses:
        pi_plus_vec = ROOT.TLorentzVector()
        pi_plus_vec.SetPtEtaPhiM(pi_plus.pt, pi_plus.eta, pi_plus.phi, PI_PLUS_MASS)

        for pi_minus in pi_minuses:
            pi_minus_vec = ROOT.TLorentzVector()
            pi_minus_vec.SetPtEtaPhiM(pi_minus.pt, pi_minus.eta, pi_minus.phi, PI_PLUS_MASS)

            rho_vec = pi_plus_vec + pi_minus_vec
            rho_mass = rho_vec.M()

            mass_diff = abs(rho_mass - RHO_ZERO_MASS)
            if mass_diff < min_mass_diff:
                min_mass_diff = mass_diff
                best_pair = (pi_plus_vec, pi_minus_vec)

    if best_pair is None:
        print("No valid pion pairs found!")
        return None, None

    return best_pair if tau_charge == 1 else (best_pair[1], best_pair[0])