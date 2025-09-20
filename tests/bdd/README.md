# Testes BDD (Behavior Driven Development)

Este diretório contém os testes BDD do projeto, utilizando o framework Behave.

## Estrutura

```
tests/bdd/
├── features/        # Arquivos .feature com cenários BDD em linguagem Gherkin
│   ├── browser_window.feature
│   ├── practice_form.feature
│   ├── progress_bar.feature
│   └── web_tables.feature
└── steps/           # Implementação dos passos (steps) em Python
    ├── browser_window_steps.py
    ├── common_steps.py
    ├── practice_form_steps.py
    ├── progress_bar_steps.py
    └── web_tables_steps.py
```

## Features disponíveis

1. **Progress Bar** - Testes de controle e validação da barra de progresso
2. **Web Tables** - Testes de criação, edição e exclusão de registros em tabelas
3. **Browser Window** - Testes de abertura de nova janela e verificação de conteúdo
4. **Practice Form** - Testes de preenchimento e submissão de formulário

## Executando os testes

### Script interativo

Para uma execução interativa, use o script `run_bdd_tests.sh`, que permite selecionar qual feature executar:

```bash
./run_bdd_tests.sh
```

Esse script exibirá um menu onde você pode selecionar qual feature deseja executar, ou rodar todas.

### Script com relatórios detalhados

Para executar todos os testes BDD e gerar relatórios detalhados em vários formatos:

```bash
./run_bdd_with_reports.sh
```

Este script gera:
- Relatório texto (.txt)
- Relatório JSON (.json)
- Relatório HTML (.html)
- Relatório JUnit (para integração com CI/CD)
- Relatório Allure (se disponível no sistema)

### Execução manual via Behave

Para executar manualmente via linha de comando:

```bash
# Executar uma feature específica
behave tests/bdd/features/progress_bar.feature

# Executar todas as features
behave tests/bdd/features/

# Executar com formatação específica
behave tests/bdd/features/ -f pretty
```

## Evidências e Relatórios

Os relatórios e evidências são gerados automaticamente nas seguintes pastas:

- **Screenshots**: `reports/screenshots/`
- **Relatórios HTML**: `reports/html-reports/`
- **Resultados Allure**: `reports/allure-results/`

## Ambiente

Para configurar o ambiente para os testes BDD:

```bash
# Criar e ativar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Para relatórios HTML adicionais
pip install behave-html-formatter
```