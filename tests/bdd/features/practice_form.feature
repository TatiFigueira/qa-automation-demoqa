Feature: Preenchimento e envio do formulário de prática no DemoQA

  Scenario: Preencher e enviar formulário com dados válidos
    Given que o usuário acessa o site DemoQA
    When ele navega até "Forms"
    And acessa o submenu "Practice Form"
    And preenche o primeiro nome com "Tatiana"
    And preenche o sobrenome com "Figueira"
    And preenche o email com "figueira.qa.tester@gmail.com"
    And seleciona o gênero "Female"
    And preenche o telefone com "11999999999"
    And seleciona a data de nascimento "11 de Novembro de 1989"
    And adiciona a matéria "Math"
    And seleciona o hobby "Reading"
    And faz upload do arquivo "arquivo_teste.txt"
    And preenche o endereço com "Rua das Flores, 123 - São Paulo"
    And submete o formulário
    Then o formulário deve ser enviado com sucesso
    And deve exibir a mensagem "Thanks for submitting the form"
    And deve salvar evidência visual
