import vector
import numpy as np
import ROOT
import math

PI_PLUS_MASS = 0.13957
PI_ZERO_MASS = 0.1349766
RHO_ZERO_MASS = 0.77526
ELECTRON_MASS = 0.000511
TAU_MASS = 1.77686

def get_chargedPion_4momentum(tauProd):
    eta = tauProd.eta
    phi = tauProd.phi
    pt = tauProd.pt

    px = pt * math.cos(phi)
    py = pt * math.sin(phi)
    pz = pt * math.sinh(eta)
    energy = math.sqrt(px**2 + py**2 + pz**2 + PI_PLUS_MASS**2)

    p4 = ROOT.TLorentzVector()
    p4.SetPxPyPzE(px, py, pz, energy)
    return p4

def get_lepton_4momentum(particle):
    pt = particle.pt
    eta = particle.eta
    phi = particle.phi

    pdgid = abs(particle.pdgId)
    
    # Mass from PDG ID
    if abs(pdgid) == 15:  # tau
        mass = 1.77686
    elif abs(pdgid) in [12, 14, 16]:  # neutrino e, mu, tau
        mass = 0.0
    elif abs(pdgid) == 111:  # neutral pion
        mass = 0.1349768
    elif abs(pdgid) == 211:  # charged pion
        mass = 0.1395704
    elif abs(pdgid) == 11:  # electron
        mass = 0.000511
    elif abs(pdgid) == 13:  # muon
        mass = 0.105658
    else:
        mass = particle.mass  # fallback

    px = pt * math.cos(phi)
    py = pt * math.sin(phi)
    pz = pt * math.sinh(eta)
    e  = math.sqrt(px**2 + py**2 + pz**2 + mass**2)

    vec = ROOT.TLorentzVector()
    vec.SetPxPyPzE(px, py, pz, e)

    return vec

def calculate_zmf(p1, p2):
    
    total_p = p1 + p2
    beta = vector.array(
        {
            "px": -total_p.px / total_p.E,
            "py": -total_p.py / total_p.E,
            "pz": -total_p.pz / total_p.E,
        }
    )
    print('beta: ', beta)
    return beta

def get_lambda(lepton):
    lambda_vec = ROOT.TLorentzVector()
    lambda_vec.SetPxPyPzE(lepton.IPx, lepton.IPy, lepton.IPz, 0.0)
    return lambda_vec

def get_perpendicular_component(vector, reference):
    reference_unit = reference.Unit()
    projection = reference_unit * vector.Dot(reference_unit)
    perpendicular = vector - projection
    return perpendicular.Unit()

def make_tlorentzvector(px, py, pz, mass=TAU_MASS):
    p2 = px**2 + py**2 + pz**2
    energy = math.sqrt(p2 + mass**2)
    vec = ROOT.TLorentzVector(px, py, pz, energy)
    return vec