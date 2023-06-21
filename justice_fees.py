class LegalFeesCalculator:

    def __init__(self):
        self.reset()

    def reset(self):
        self.total = 0

    def register_commerce(self, operation_type, amount=0):
        # Définir les frais en fonction du type d'opération
        fees_dict = {
            'immatriculation': 150,
            'delivrance_copie': 20,
            'inscription_modificative': 50,
            'requisitions_inscriptions': 100,
            'transcription_pv': 50,
            'depot_acte_societe': 200,
            'depot_statuts_societe': 200,
            'depots_posterieurs': 50,
            'radiation_inscription': 50,
            'radiation_office': 0
        }
        self.total += fees_dict[operation_type]

    def nantissements(self, operation_type, amount=0):
        fees_dict = {
            'depot_vente': 150,
            'inscription_creance': 0.005 * amount,  # 0,50 %
            'inscriptions_complementaires': 50,
            'inscription_domicile': 0.005 * amount,  # 0,50 %
            'inscription_domicile_tiers': 50,
            'mainlevee_nantissement': 50,
            'mainlevee_office': 0,
            'transcription_contrat': 0.005 * amount,  # 0,50 %
            'delivrance_extrait': 20,
            'mention_effets_commerce': 20,
            'radiation': max(0.005 * amount, 50),  # 0,50 % avec un minimum de 50
            'renouvellement_inscription': 0.005 * amount,  # 0,50 %
            'nantissement_credit_agricole': 0
        }
        self.total += fees_dict[operation_type]

    def droit_plaidoirie(self, amount=0):
        # Le droit de plaidoirie est fixe à 10 dirhams
        self.total += 10

    def total_fees(self):
        return self.total


class FraisJudiciaires:
    def __init__(self, montant_initial, retard=False, mois_de_retard=0):
        self.montant_initial = montant_initial
        self.retard = retard
        self.mois_de_retard = mois_de_retard

    def calculer_frais(self):
        frais = self.montant_initial
        if self.retard:
            frais += self.calculer_amende() + self.calculer_majoration()
        return frais

    def calculer_amende(self):
        return 0.1 * self.montant_initial  # 10% du montant initial

    def calculer_majoration(self):
        majoration = 0.05 * self.montant_initial  # 5% pour le premier mois
        if self.mois_de_retard > 1:
            majoration += (self.mois_de_retard - 1) * 0.005 * self.montant_initial  # 0.50% pour chaque
            # mois supplémentaire
        return majoration


# Exemple d'utilisation
calculator = LegalFeesCalculator()
calculator.register_commerce('immatriculation')
calculator.nantissements('inscription_creance', amount=10000)
calculator.droit_plaidoirie()
print(f"le total des frais calculés: {calculator.total_fees()} dirhams.")  # Doit afficher le total des frais calculés


# Pour un acte avec un montant initial de 1000 dirhams, payé avec un retard de 3 mois
acte = FraisJudiciaires(1000, retard=True, mois_de_retard=3)
print(f"Les frais totaux pour cet acte sont : {acte.calculer_frais()} dirhams.")
