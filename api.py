from fastapi import FastAPI, Form
from pydantic import BaseModel, Field
from justice_fees import LegalFeesCalculator,FraisJudiciaires, LegalFeesCalculator2
from enum import Enum


class Fees(BaseModel):
    operation_type: str = Field(..., description="The type of operation", example="immatriculation")
    amount: int = Field(..., description="The amount", example=1000)
    roles: int = Field(..., description="The number of roles", example=1)
    half_roles: int = Field(..., description="The number of half roles", example=1)
    travel_expenses: int = Field(..., description="Total travel expenses", example=100)
    expert_fees: int = Field(..., description="Expert fees", example=200)
    fee: int = Field(..., description="Fee", example=50)
    days: int = Field(..., description="Number of days", example=2)
    is_executory_title: bool = Field(..., description="Is executory title?", example=True)
    revenues: int = Field(..., description="Revenues", example=10000)
    actif_realise: int = Field(..., description="Actif realise", example=5000)
    price: int = Field(..., description="Price", example=15000)
    montant_initial: int = Field(..., description="Montant initial", example=1000)
    retard: bool = Field(..., description="Is it late?", example=True)
    mois_de_retard: int = Field(..., description="Number of delay months", example=3)

class CommerceOperationType(str, Enum):
    immatriculation = 'immatriculation'
    delivrance_copie = 'delivrance_copie'
    inscription_modificative = 'inscription_modificative'
    requisitions_inscriptions = 'requisitions_inscriptions'
    transcription_pv = 'transcription_pv'
    depot_acte_societe = 'depot_acte_societe'
    depot_statuts_societe = 'depot_statuts_societe'
    depots_posterieurs = 'depots_posterieurs'
    radiation_inscription = 'radiation_inscription'
    radiation_office = 'radiation_office'

class NantissementsOperationType(str, Enum):
    depot_vente = 'depot_vente'
    inscription_creance = 'inscription_creance'
    inscriptions_complementaires = 'inscriptions_complementaires'
    inscription_domicile = 'inscription_domicile'
    inscription_domicile_tiers = 'inscription_domicile_tiers'
    mainlevee_nantissement = 'mainlevee_nantissement'
    mainlevee_office = 'mainlevee_office'
    transcription_contrat = 'transcription_contrat'
    delivrance_extrait = 'delivrance_extrait'
    mention_effets_commerce = 'mention_effets_commerce'
    radiation = 'radiation'
    renouvellement_inscription = 'renouvellement_inscription'
    nantissement_credit_agricole = 'nantissement_credit_agricole'

class FraisJudiciairesParams(BaseModel):
    montant_initial: float
    retard: bool
    mois_de_retard: int

app = FastAPI(title="Calculateur de Frais Judiciaires", description="Une API pour calculer différents frais judiciaires.")

class FeeParams(BaseModel):
    operation_type: CommerceOperationType
    amount: float = 0

class NantissementsParams(BaseModel):
    operation_type: NantissementsOperationType
    amount: float = 0


@app.post("/register_commerce/", summary="Enregistrer une opération de commerce", description="Enregistre une opération de commerce et calcule les frais associés.")
def register_commerce(operation_type: CommerceOperationType = Form(...), amount: float = Form(0.0)):
    calculator = LegalFeesCalculator2()
    calculator.register_commerce(operation_type.value, amount)
    return {"total": calculator.total_fees()}

@app.post("/nantissements/", summary="Enregistrer une opération de nantissement", description="Enregistre une opération de nantissement et calcule les frais associés.")
def nantissements(operation_type: NantissementsOperationType = Form(...), amount: float = Form(0.0)):
    calculator = LegalFeesCalculator2()
    calculator.nantissements(operation_type.value, amount)
    return {"total": calculator.total_fees()}

@app.get("/droit_plaidoirie/", summary="Calculer le droit de plaidoirie", description="Calcule le droit de plaidoirie qui est fixe à 10 dirhams.")
def droit_plaidoirie():
    calculator = LegalFeesCalculator2()
    calculator.droit_plaidoirie()
    return {"total": calculator.total_fees()}

@app.post("/frais_judiciaires/", summary="Calculer les frais judiciaires", description="Calcule les frais judiciaires, y compris l'amende et la majoration en cas de retard.")
def frais_judiciaires(montant_initial: float = Form(...), retard: bool = Form(False), mois_de_retard: int = Form(0)):
    acte = FraisJudiciaires(montant_initial, retard, mois_de_retard)
    return {"total": acte.calculer_frais}

@app.post("/calculate-fees")
async def calculate_fees(fees: Fees):
    legal_calculator = LegalFeesCalculator()
    legal_calculator.calculate_fee(fees.fee)
    legal_calculator.calculate_copies_fees(fees.roles, fees.half_roles)
    legal_calculator.calculate_travel_fees(fees.travel_expenses)
    legal_calculator.calculate_expert_fees(fees.expert_fees)

    judicial_calculator = JudicialFeeCalculator()
    judicial_calculator.calculate_fee_based_on_amount(fees.amount)
    judicial_calculator.calculate_fixed_fee(fees.fee)
    judicial_calculator.calculate_proces_verbal_offers(fees.amount)
    judicial_calculator.calculate_protest(fees.amount)
    judicial_calculator.calculate_eviction_or_possession(fees.days)
    judicial_calculator.calculate_seizure_procedure(fees.amount, fees.is_executory_title, fees.days)
    judicial_calculator.calculate_faillite_liquidation(fees.amount)
    judicial_calculator.calculate_administrations_judiciaires(fees.revenues, fees.actif_realise)
    judicial_calculator.calculate_ventes_publiques(fees.price)
    judicial_calculator.calculate_distributions(fees.amount)

    legal_calculator2 = LegalFeesCalculator2()
    legal_calculator2.register_commerce(fees.operation_type, fees.amount)

    frais_judiciaires = FraisJudiciaires(fees.montant_initial, fees.retard, fees.mois_de_retard)

    total_fees = legal_calculator.calculate_total() + \
                 judicial_calculator.calculate_total() + \
                 legal_calculator2.calculate_total() + \
                 frais_judiciaires.calculer_frais()

    return {"total_fees": total_fees}