class LegalFeesCalculator:
    def __init__(self):
        self.total = 0
    
    def calculate_copies_fees(self, roles, half_roles):
        '''
        roles: Le nombre de rôles complets
        half_roles: Le nombre de demi rôles
        '''
        role_price = 10
        half_role_price = 5
        self.total += (roles * role_price) + (half_roles * half_role_price)

    def calculate_travel_fees(self, travel_expenses):
        '''
        travel_expenses: Les frais de déplacement totaux
        '''
        self.total += travel_expenses

    def calculate_expert_fees(self, expert_fees):
        '''
        expert_fees: Les honoraires des experts
        '''
        self.total += expert_fees

    def calculate_fee(self, fee):
        self.total += fee

    def calculate_total(self):
        return self.total

class JudicialFeeCalculator(LegalFeesCalculator):

    def calculate_fixed_fee(self, fee):
        self.total += fee
    def calculate_fee_based_on_amount(self, amount):
        if 1000 <= amount <= 5000:
            self.calculate_fee(max(0.04 * amount, 50))
        elif 5001 <= amount <= 20000:
            self.calculate_fee(max(0.025 * amount, 200))
        elif amount > 20000:
            self.calculate_fee(0.01 * amount + 300)

    def calculate_proces_verbal_offers(self, amount):
        self.calculate_fee(min(max(0.01 * amount, 50), 150))

    def calculate_protest(self, amount):
        self.calculate_fee(50 + 0.005 * amount)

    def calculate_eviction_or_possession(self, days):
        self.calculate_fee(50 * days)

    def calculate_seizure_procedure(self, amount, is_executory_title=True, days=1):
        fee = 50 if is_executory_title else 150
        self.calculate_fee(fee * days)
        if amount > 10000:
            self.total *= 2

    def calculate_faillite_liquidation(self, amount):
        self.calculate_fee(0.1 * amount)

    def calculate_administrations_judiciaires(self, revenues, actif_realise):
        self.calculate_fee(0.1 * (revenues + actif_realise))

    def calculate_ventes_publiques(self, price):
        self.calculate_fee(0.1 * price)

    def calculate_distributions(self, amount):
        self.calculate_fee(0.05 * amount)


class LegalFeesCalculator2(LegalFeesCalculator):
    def register_commerce(self, operation_type, amount=0):
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
        self.calculate_fee(fees_dict[operation_type])

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
        self.calculate_fee(fees_dict[operation_type])

    def droit_plaidoirie(self, amount=0):
        # Le droit de plaidoirie est fixe à 10 dirhams
        self.calculate_fee(10)


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
            majoration += (self.mois_de_retard - 1) * 0.005 * self.montant_initial  # 0.50% for each additional month
        return majoration

