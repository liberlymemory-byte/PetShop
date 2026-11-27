# src/app.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.regras import (
    validar_nome,
    validar_servico,
    calcular_banho,
    calcular_tosa,
    calcular_transporte,
    calcular_desconto,
)

app = FastAPI(title="PetShop API")


# Modelos de dados
class OrcamentoRequest(BaseModel):
    nome_pet: str
    servico: str
    porte: str
    desconto: float = 0


class TransporteRequest(BaseModel):
    nome_pet: str
    distancia: float


# Rota de saúde da API
@app.get("/health")
def health():
    return {"status": "API funcionando"}


# Rota 1 - Listar serviços
@app.get("/servicos")
def listar_servicos():
    return {
        "servicos": ["banho", "tosa", "transporte"]
    }


# Rota 2 - Calcular orçamento
@app.post("/orcamento")
def calcular_orcamento(dados: OrcamentoRequest):
    try:
        validar_nome(dados.nome_pet)
        servico = validar_servico(dados.servico)

        if servico == "banho":
            valor = calcular_banho(dados.porte)

        elif servico == "tosa":
            valor = calcular_tosa(dados.porte)

        else:
            raise ValueError(
                "Para transporte, utilize a rota específica."
            )

        valor_final = calcular_desconto(valor, dados.desconto)

        return {
            "pet": dados.nome_pet,
            "servico": servico,
            "porte": dados.porte,
            "valor_original": valor,
            "desconto": dados.desconto,
            "valor_final": valor_final
        }

    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


# Rota 3 - Calcular transporte
@app.post("/transporte")
def calcular_valor_transporte(dados: TransporteRequest):
    try:
        validar_nome(dados.nome_pet)
        valor = calcular_transporte(dados.distancia)

        return {
            "pet": dados.nome_pet,
            "distancia_km": dados.distancia,
            "valor_transporte": valor
        }

    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))