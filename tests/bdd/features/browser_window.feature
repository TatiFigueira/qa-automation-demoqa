Feature: Validação de nova janela no DemoQA

  Scenario: Abrir nova janela e verificar mensagem
    Given que o usuário acessa o site DemoQA
    When ele navega até "Alerts, Frame & Windows"
    And clica em "Browser Windows"
    And clica no botão "New Window"
    Then uma nova janela deve ser aberta
    And a mensagem "This is a sample page" deve estar visível
    And a nova janela deve ser fechada