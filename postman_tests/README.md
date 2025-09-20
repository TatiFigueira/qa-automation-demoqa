# 🚀 Automação de Testes de API - DemoQA

Este projeto realiza a automação dos principais endpoints da API do site [DemoQA](https://demoqa.com), utilizando o Postman com execução contínua via Collection Runner.

## ✅ Funcionalidades testadas

- Criar usuário
- Gerar token de acesso
- Verificar autorização
- Listar livros disponíveis
- Alugar dois livros
- Verificar livros alugados
- Remover livros do usuário

## 🧪 Tecnologias utilizadas

- Postman
- Postman Collection Runner
- Variáveis de ambiente
- Scripts em JavaScript (Pre-request e Post-response)

## 📁 Estrutura

- `DemoQA API Challenge.postman_collection.json`: Collection com todos os endpoints
- `DemoQA Environment.postman_environment.json`: Variáveis dinâmicas usadas nos testes
- `README.md`: Documentação do projeto
- `evidencias/`: Relatórios e prints da execução (opcional)

## 🧭 Execução

1. Importe a Collection e o Environment no Postman
2. Abra o Collection Runner
3. Selecione o Environment
4. Clique em **Run**

Todos os testes serão executados em sequência, com validações automáticas e variáveis dinâmicas.

---

## 👩‍💻 Autor

- **Tatiana Figueira**
