def dump_tau_products(tau_products, number_of_products = 5):
    """
    Dump N most energetic tau products to a list
    """

    sorted_products = sorted(
        tau_products,
        key=lambda p: getattr(p, 'pt', -1),
        reverse=True
    )

    taus = []

    for i, p in enumerate(sorted_products[:number_of_products]):
        pt  = getattr(p, 'pt', -1)
        eta = getattr(p, 'eta', -1)
        phi = getattr(p, 'phi', -1)
        pdg = getattr(p, 'pdgId', -1)

        taus.append({
            'pt': pt,
            'eta': eta,
            'phi': phi,
            'pdgId': pdg
        })

    return taus