import vector
import numpy as np

PI_PLUS_MASS = 0.13957
PI_ZERO_MASS = 0.1349766
RHO_ZERO_MASS = 0.77526
ELECTRON_MASS = 0.000511

ZERO_4VECTOR = vector.array(
        {
            "pt": [0],
            "eta": [0],
            "phi": [0],
            "M": [0]
        }
    )

def get_chargedPion_4momentum(tauProd):
    eta = tauProd.eta
    pdgID = tauProd.pdgId
    pt = tauProd.pt
    phi = tauProd.phi
    #tau_index = tauProd.tauIdx

    return vector.array(
        {
            "pt": [pt],
            "eta": [eta],
            "phi": [phi],
            "M": [PI_PLUS_MASS]
        }
    )

def get_lepton_4momentum(particle):
    pt = particle.pt
    eta = particle.eta
    phi = particle.phi

    pdgid = abs(particle.pdgId)
    
    # Ustal masę na podstawie typu cząstki (PDG ID)
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
        mass = particle.mass  # fallback (jeśli root podał coś konkretnego)

    return vector.obj(
        pt=pt,
        eta=eta,
        phi=phi,
        mass=mass
    )

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

    return vector.array(
        {
            "px": [lepton.IPx],
            "py": [lepton.IPy],
            "pz": [lepton.IPz],
            "E": [0],
        }
    )

def get_perpendicular_component(vector, reference):
    projection = (vector.dot(reference)) * reference
    perpendicular = vector - projection
    return perpendicular.unit()