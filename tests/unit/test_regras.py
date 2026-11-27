
import pytest

from src.regras import (
    validar_nome,
    validar_servico,
    calcular_banho,
    calcular_tosa,
    calcular_transporte,
    calcular_desconto
)


# =========================
# TESTES: VALIDAR NOME
# =========================

@pytest.mark.parametrize("nome", [
    "Mel",
    "Rex",
    "Luna",
    "Buddy",
    "  Mel  "
])
def test_validar_nome_valido(nome):
    resultado = validar_nome(nome)
    assert resultado == nome.strip()


@pytest.mark.parametrize("nome", [
    "",
    "   ",
    None,
    123,
    45.6
])
def test_validar_nome_invalido(nome):
    with pytest.raises(ValueError):
        validar_nome(nome)


# =========================
# TESTES: VALIDAR SERVIÇO
# =========================

@pytest.mark.parametrize("servico", [
    "banho",
    "tosa",
    "transporte",
    "BANHO",
    "TOSA",
    "TRANSPORTE"
])
def test_validar_servico_valido(servico):
    resultado = validar_servico(servico)
    assert resultado == servico.lower()


@pytest.mark.parametrize("servico", [
    "consulta",
    "vacina",
    "hotel",
    "",
    None,
    123
])
def test_validar_servico_invalido(servico):
    with pytest.raises(ValueError):
        validar_servico(servico)


# =========================
# TESTES: CALCULAR BANHO
# =========================

@pytest.mark.parametrize("porte,valor_esperado", [
    ("pequeno", 40.00),
    ("medio", 60.00),
    ("grande", 80.00)
])
def test_calcular_banho_valido(porte, valor_esperado):
    resultado = calcular_banho(porte)
    assert resultado == valor_esperado


@pytest.mark.parametrize("porte", [
    "gigante",
    "mini",
    "extra_grande",
    "",
    None
])
def test_calcular_banho_porte_invalido(porte):
    with pytest.raises(ValueError):
        calcular_banho(porte)


# =========================
# TESTES: CALCULAR TOSA
# =========================

@pytest.mark.parametrize("porte,valor_esperado", [
    ("pequeno", 30.00),
    ("medio", 45.00),
    ("grande", 60.00)
])
def test_calcular_tosa_valida(porte, valor_esperado):
    resultado = calcular_tosa(porte)
    assert resultado == valor_esperado


@pytest.mark.parametrize("porte", [
    "gigante",
    "mini",
    "extra_grande",
    "",
    None
])
def test_calcular_tosa_porte_invalido(porte):
    with pytest.raises(ValueError):
        calcular_tosa(porte)


# =========================
# TESTES: CALCULAR TRANSPORTE
# =========================

@pytest.mark.parametrize("distancia,valor_esperado", [
    (1, 3.50),
    (5, 17.50),
    (10, 35.00),
    (2.5, 8.75)
])
def test_calcular_transporte_valido(distancia, valor_esperado):
    resultado = calcular_transporte(distancia)
    assert resultado == valor_esperado


@pytest.mark.parametrize("distancia", [
    0,
    -1,
    -5,
    "5",
    None,
    "distancia"
])
def test_calcular_transporte_invalido(distancia):
    with pytest.raises(ValueError):
        calcular_transporte(distancia)


# =========================
# TESTES: CALCULAR DESCONTO
# =========================

@pytest.mark.parametrize("valor,percentual,valor_esperado", [
    (100, 0, 100),
    (100, 10, 90),
    (100, 20, 80),
    (200, 5, 190),
    (50, 15, 42.5),
    (0, 10, 0)
])
def test_calcular_desconto_valido(valor, percentual, valor_esperado):
    resultado = calcular_desconto(valor, percentual)
    assert resultado == valor_esperado


@pytest.mark.parametrize("valor,percentual", [
    (-10, 10),
    (-1, 0),
    (100, -1),
    (100, 21),
    (100, 100),
    ("100", 10),
    (100, "10"),
    (None, 10),
    (100, None)
])
def test_calcular_desconto_invalido(valor, percentual):
    with pytest.raises(ValueError):
        calcular_desconto(valor, percentual)
