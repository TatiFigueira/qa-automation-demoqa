# QA Automation Framework - DemoQA

Framework de automação de testes para o site [DemoQA](https://demoqa.com/) usando Selenium WebDriver, Pytest e Behave (BDD).

## 🚀 Recursos

- **Testes de UI**: Automação de interface com Selenium WebDriver
- **Testes BDD**: Cenários em linguagem natural com Behave
- **Testes de API**: Requisições e validações de APIs REST
- **Multiplataforma**: Funciona em Windows, macOS e Linux
- **Relatórios**: HTML e Allure (opcional)
- **Screenshots**: Captura automática em falhas

## 📋 Requisitos

- Python 3.8 ou superior
- Google Chrome instalado (para os testes de UI)
- Pip (gerenciador de pacotes Python)

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/qa-automation-demoqa.git
cd qa-automation-demoqa
```

### 2. Crie um ambiente virtual

**Windows:**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

## ▶️ Executando os Testes

### Método 1: Execução Direta com Behave (Recomendado para BDD)

Este método é o mais simples para executar os testes BDD que acabamos de corrigir.

**macOS/Linux:**
```bash
# 1. Ative o ambiente virtual (se não estiver ativo)
source .venv/bin/activate

# 2. Execute os testes BDD
behave tests/bdd/features/
```

**Windows:**
```cmd
# 1. Ative o ambiente virtual (se não estiver ativo)
.venv\Scripts\activate

# 2. Execute os testes BDD
behave tests/bdd/features/
```

### Método 2: Executando testes específicos

**Para um cenário BDD específico:**
```bash
behave tests/bdd/features/browser_window.feature
```

### Testes de API (Postman)

Os testes de API foram desenvolvidos como uma coleção do Postman e estão localizados em `postman_tests/` na raiz do repositório. A pasta contém:

- `DemoQA API Challenge.postman_collection.json`: coleção com os endpoints e validações.
- `DemoQA Environment.postman_environment.json`: variáveis de ambiente para uso no Postman.
- `README.md`: instruções de execução específicas para a coleção (importante para reproduzir execuções e evidências).

Como executar:

1. Abra o Postman e importe a coleção `postman_tests/DemoQA API Challenge.postman_collection.json`.
2. Importe também o environment `postman_tests/DemoQA Environment.postman_environment.json`.
3. Se desejar, abra `postman_tests/README.md` para detalhes e evidências.
4. Use o Collection Runner do Postman para executar a coleção inteira (selecionando o Environment importado).







