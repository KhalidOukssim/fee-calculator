from fastapi import FastAPI, Form
from pydantic import BaseModel
from justice_fees import LegalFeesCalculator,FraisJudiciaires
from enum import Enum

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
    calculator = LegalFeesCalculator()
    calculator.register_commerce(operation_type.value, amount)
    return {"total": calculator.total_fees()}

@app.post("/nantissements/", summary="Enregistrer une opération de nantissement", description="Enregistre une opération de nantissement et calcule les frais associés.")
def nantissements(operation_type: NantissementsOperationType = Form(...), amount: float = Form(0.0)):
    calculator = LegalFeesCalculator()
    calculator.nantissements(operation_type.value, amount)
    return {"total": calculator.total_fees()}

@app.get("/droit_plaidoirie/", summary="Calculer le droit de plaidoirie", description="Calcule le droit de plaidoirie qui est fixe à 10 dirhams.")
def droit_plaidoirie():
    calculator = LegalFeesCalculator()
    calculator.droit_plaidoirie()
    return {"total": calculator.total_fees()}

@app.post("/frais_judiciaires/", summary="Calculer les frais judiciaires", description="Calcule les frais judiciaires, y compris l'amende et la majoration en cas de retard.")
def frais_judiciaires(montant_initial: float = Form(...), retard: bool = Form(False), mois_de_retard: int = Form(0)):
    acte = FraisJudiciaires(montant_initial, retard, mois_de_retard)
    return {"total": acte.calculer_frais}