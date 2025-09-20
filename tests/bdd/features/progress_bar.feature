Feature: Validação da Progress Bar no DemoQA

  Scenario: Controlar e validar o progresso da barra
    Given que o usuário acessa o site DemoQA
    When ele clica em "Widgets"
    And acessa o submenu "Progress Bar"
    And inicia o progresso e para antes de 25%
    Then o valor da barra deve ser menor ou igual a 25%
    When inicia novamente e aguarda até 100%
    Then a barra deve ser resetada