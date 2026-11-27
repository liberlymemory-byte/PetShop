
from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


# ==========================================
# TESTES DA ROTA GET /health
# ==========================================

def test_health_api_funcionando():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "API funcionando"}


# ==========================================
# TESTES DA ROTA GET /servicos
# ==========================================

def test_listar_servicos():
    response = client.get("/servicos")

    assert response.status_code == 200
    assert response.json() == {
        "servicos": ["banho", "tosa", "transporte"]
    }


# ==========================================
# TESTES DA ROTA POST /orcamento
# ==========================================

def test_orcamento_banho_sucesso():
    dados = {
        "nome_pet": "Mel",
        "servico": "banho",
        "porte": "pequeno",
        "desconto": 0
    }

    response = client.post("/orcamento", json=dados)

    assert response.status_code == 200
    assert response.json() == {
        "pet": "Mel",
        "servico": "banho",
        "porte": "pequeno",
        "valor_original": 40.00,
        "desconto": 0,
        "valor_final": 40.00
    }


def test_orcamento_tosa_com_desconto():
    dados = {
        "nome_pet": "Rex",
        "servico": "tosa",
        "porte": "medio",
        "desconto": 10
    }

    response = client.post("/orcamento", json=dados)

    assert response.status_code == 200
    assert response.json() == {
        "pet": "Rex",
        "servico": "tosa",
        "porte": "medio",
        "valor_original": 45.00,
        "desconto": 10,
        "valor_final": 40.50
    }


def test_orcamento_servico_invalido():
    dados = {
        "nome_pet": "Mel",
        "servico": "consulta",
        "porte": "pequeno",
        "desconto": 0
    }

    response = client.post("/orcamento", json=dados)

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Serviço não disponível."
    }


def test_orcamento_porte_invalido():
    dados = {
        "nome_pet": "Mel",
        "servico": "banho",
        "porte": "gigante",
        "desconto": 0
    }

    response = client.post("/orcamento", json=dados)

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Porte inválido."
    }


def test_orcamento_desconto_invalido():
    dados = {
        "nome_pet": "Mel",
        "servico": "banho",
        "porte": "pequeno",
        "desconto": 25
    }

    response = client.post("/orcamento", json=dados)

    assert response.status_code == 400
    assert response.json() == {
        "detail": "O desconto deve estar entre 0% e 20%."
    }


# ==========================================
# TESTES DA ROTA POST /transporte
# ==========================================

def test_transporte_sucesso():
    dados = {
        "nome_pet": "Mel",
        "distancia": 5
    }

    response = client.post("/transporte", json=dados)

    assert response.status_code == 200
    assert response.json() == {
        "pet": "Mel",
        "distancia_km": 5,
        "valor_transporte": 17.50
    }


def test_transporte_distancia_invalida():
    dados = {
        "nome_pet": "Mel",
        "distancia": -5
    }

    response = client.post("/transporte", json=dados)

    assert response.status_code == 400
    assert response.json() == {
        "detail": "A distância deve ser maior que zero."
    }


def test_transporte_nome_invalido():
    dados = {
        "nome_pet": "",
        "distancia": 5
    }

    response = client.post("/transporte", json=dados)

    assert response.status_code == 400
    assert response.json() == {
        "detail": "O nome não pode estar vazio."
    }
