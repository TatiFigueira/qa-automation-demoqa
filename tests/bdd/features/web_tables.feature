Feature: Gerenciamento de registros na Web Tables do DemoQA

  Scenario: Criar, editar e excluir um registro
    Given que o usuário acessa o site DemoQA
    When ele clica em "Elements"
    And acessa o submenu "Web Tables"
    And cria um novo registro com os dados "Tatiana", "QA", "figueira.qa@teste.com", "30", "5000", "TesteCorp"
    And edita o registro criado para "Pandora", "QA Sênior", "pandora@qa.com", "31", "7000", "QAcorp"
    Then o registro editado deve estar visível
    When exclui o registro criado
    Then o registro não deve mais estar visível
