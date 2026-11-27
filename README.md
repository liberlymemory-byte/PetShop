# PetShop API – Banho, Tosa & Transporte

Projeto final de **Testes e Qualidade de Software na Prática: da Automação ao CI**.

Mini API em Python (FastAPI) para um pet shop que oferece **banho**, **tosa** e **transporte**. A API calcula orçamentos com regras de negócio validadas e é protegida por duas suítes de testes automatizados (unitários e de integração), executadas em uma pipeline de CI no GitHub Actions.

## Equipe

- Victor André Lopes da Silva
- Ketellyane Clea
- Jefferson Jose
- Franco Dantas
- Bernardo Albuquerque

## Tema

**Pet Shop (Banho, Tosa & Transporte).** O cliente informa o nome do pet, o serviço desejado e o porte do animal, e a API devolve o valor do serviço, com desconto opcional. O transporte é calculado à parte, pela distância em quilômetros.

## Regras de negócio (`src/regras.py`)

| # | Função | O que faz | Erro lançado |
|---|--------|-----------|--------------|
| 1 | `validar_nome(nome)` | Remove espaços e exige um nome não vazio. | `ValueError` se estiver vazio ou não for texto |
| 2 | `validar_servico(servico)` | Aceita `banho`, `tosa` ou `transporte` (sem diferenciar maiúsculas). | `ValueError` se não for texto ou não existir |
| 3 | `calcular_banho(porte)` | Preço do banho: pequeno R$ 40, médio R$ 60, grande R$ 80. | `ValueError` para porte inválido |
| 4 | `calcular_tosa(porte)` | Preço da tosa: pequeno R$ 30, médio R$ 45, grande R$ 60. | `ValueError` para porte inválido |
| 5 | `calcular_transporte(distancia)` | Distância em km multiplicada por R$ 3,50. | `ValueError` se a distância for zero, negativa ou não numérica |
| 6 | `calcular_desconto(valor, percentual)` | Aplica desconto de 0% a 20% sobre o valor. | `ValueError` para valor negativo ou desconto fora de 0–20 |

Portes aceitos: `pequeno`, `medio` e `grande`.

## Rotas da API (`src/app.py`)

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/health` | Verifica se a API está funcionando. |
| GET | `/servicos` | Lista os serviços disponíveis. |
| POST | `/orcamento` | Calcula banho ou tosa, com desconto opcional. |
| POST | `/transporte` | Calcula o valor do transporte pela distância. |

Erros de negócio (`ValueError`) viram resposta **400 Bad Request** com a mensagem em `detail`. Corpo com campos ausentes ou de tipo errado retorna **422**, tratado pelo próprio FastAPI.

### Exemplos

`GET /health`

```json
{ "status": "API funcionando" }
```

`POST /orcamento`

```json
{ "nome_pet": "Thor", "servico": "banho", "porte": "medio", "desconto": 10 }
```

```json
{
  "pet": "Thor",
  "servico": "banho",
  "porte": "medio",
  "valor_original": 60.0,
  "desconto": 10.0,
  "valor_final": 54.0
}
```

`POST /transporte`

```json
{ "nome_pet": "Thor", "distancia": 5 }
```

```json
{ "pet": "Thor", "distancia_km": 5.0, "valor_transporte": 17.5 }
```

Com a API rodando, a documentação interativa fica em `http://127.0.0.1:8000/docs`.

## Como executar

Pré-requisito: Python 3.12 ou superior.

```bash
# 1. clonar o repositório
git clone https://github.com/liberlymemory-byte/PetShop.git
cd PetShop

# 2. criar e ativar o ambiente virtual
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. instalar as dependências
pip install -r requirements.txt

# 4. subir a API
uvicorn src.app:app --reload
```

A API fica disponível em `http://127.0.0.1:8000`.

## Testes

```bash
# testes unitários
pytest tests/unit -v

# testes de integração (API, com TestClient)
pytest tests/integration -v

# todos os testes com cobertura
pytest --cov=src --cov-report=html --cov-report=term-missing
```

O relatório HTML da cobertura é gerado na pasta `htmlcov/`.

- **Unitários (`tests/unit/`):** validam cada função de `regras.py`, com classes de equivalência, valores de fronteira (`@pytest.mark.parametrize`) e exceções com `pytest.raises`, no padrão AAA.
- **Integração (`tests/integration/`):** usam o `TestClient` do FastAPI para testar todas as rotas, com cenários de sucesso (200) e de erro (400/422).

## Pipeline de CI (`.github/workflows/ci.yml`)

Executada automaticamente em `push` e `pull_request`, com estratégia *fail fast* em dois jobs encadeados:

1. **`unit-tests`:** instala as dependências e roda `pytest tests/unit -v`.
2. **`integration-tests`** (`needs: unit-tests`): só executa se os unitários passarem; roda os testes de integração e gera a cobertura. O relatório `htmlcov/` é publicado como artefato **`coverage-report`** (`actions/upload-artifact@v4`, `if: always()`).

## Landing page

A pasta `frontend/` contém a página de apresentação do pet shop (`index.html` e `style.css`). Ela mostra os serviços e os preços e traz um simulador de orçamento que usa as rotas `/orcamento` e `/transporte`. Para usar:

1. Suba a API (`uvicorn src.app:app --reload`).
2. Abra `frontend/index.html` no navegador.

Se a API não responder (por exemplo, sem CORS habilitado), a página calcula o orçamento no próprio navegador com as mesmas regras.

## Estrutura do projeto

```
PetShop/
├── .github/workflows/ci.yml
├── frontend/
│   ├── index.html
│   └── style.css
├── src/
│   ├── app.py
│   └── regras.py
├── tests/
│   ├── integration/test_api.py
│   └── unit/test_regras.py
├── pytest.ini
└── requirements.txt
```
