# regras.py

SERVICOS_DISPONIVEIS = ["banho", "tosa", "transporte"]

PRECOS_BANHO = {
    "pequeno": 40.00,
    "medio": 60.00,
    "grande": 80.00
}

PRECOS_TOSA = {
    "pequeno": 30.00,
    "medio": 45.00,
    "grande": 60.00
}


# 1. Validar nome
def validar_nome(nome):
    if not isinstance(nome, str) or nome.strip() == "":
        raise ValueError("O nome não pode estar vazio.")
    return nome.strip()


# 2. Validar serviço
def validar_servico(servico):
    if not isinstance(servico, str):
        raise ValueError("O serviço deve ser informado como texto.")

    if servico.lower() not in SERVICOS_DISPONIVEIS:
        raise ValueError("Serviço não disponível.")

    return servico.lower()


# 3. Calcular preço do banho
def calcular_banho(porte):
    if porte not in PRECOS_BANHO:
        raise ValueError("Porte inválido.")

    return PRECOS_BANHO[porte]


# 4. Calcular preço da tosa
def calcular_tosa(porte):
    if porte not in PRECOS_TOSA:
        raise ValueError("Porte inválido.")

    return PRECOS_TOSA[porte]


# 5. Calcular preço do transporte
def calcular_transporte(distancia):
    if not isinstance(distancia, (int, float)) or distancia <= 0:
        raise ValueError("A distância deve ser maior que zero.")

    return distancia * 3.50


# 6. Calcular desconto
def calcular_desconto(valor, percentual):
    if not isinstance(valor, (int, float)) or valor < 0:
        raise ValueError("O valor deve ser positivo.")

    if not isinstance(percentual, (int, float)) or percentual < 0 or percentual > 20:
        raise ValueError("O desconto deve estar entre 0% e 20%.")

    return valor - (valor * percentual / 100)