def dump_tau_products(tau_products, number_of_products = 5):
    """
    Dump N most energetic tau products to a list
    """

    seen = set()
    unique_products = []
    for p in tau_products:
        key = (getattr(p, 'pdgId', -1),
               round(getattr(p, 'pt', -1), 3),
               round(getattr(p, 'eta', -1), 3),
               round(getattr(p, 'phi', -1), 3))
        if key not in seen:
            seen.add(key)
            unique_products.append(p)

    sorted_products = sorted(
        unique_products,
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