from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@when('ele clica em "Elements"')
def step_click_elements(context):
    wait = WebDriverWait(context.driver, 10)
    element = wait.until(EC.presence_of_element_located((By.XPATH, "//h5[text()='Elements']")))
    context.driver.execute_script("arguments[0].scrollIntoView(true);", element)
    element.click()

@when('acessa o submenu "Web Tables"')
def step_click_web_tables(context):
    wait = WebDriverWait(context.driver, 10)
    submenu = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Web Tables']")))
    context.driver.execute_script("arguments[0].scrollIntoView(true);", submenu)
    submenu.click()

@when('cria um novo registro com os dados "{first}", "{last}", "{email}", "{age}", "{salary}", "{department}"')
def step_create_record(context, first, last, email, age, salary, department):
    wait = WebDriverWait(context.driver, 10)
    add_button = wait.until(EC.element_to_be_clickable((By.ID, "addNewRecordButton")))
    context.driver.execute_script("arguments[0].scrollIntoView(true);", add_button)
    add_button.click()

    wait.until(EC.visibility_of_element_located((By.ID, "firstName"))).send_keys(first)
    context.driver.find_element(By.ID, "lastName").send_keys(last)
    context.driver.find_element(By.ID, "userEmail").send_keys(email)
    context.driver.find_element(By.ID, "age").send_keys(age)
    context.driver.find_element(By.ID, "salary").send_keys(salary)
    context.driver.find_element(By.ID, "department").send_keys(department)

    submit_button = context.driver.find_element(By.ID, "submit")
    context.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
    context.driver.execute_script("arguments[0].click();", submit_button)

@when('edita o registro criado para "{first}", "{last}", "{email}", "{age}", "{salary}", "{department}"')
def step_edit_record(context, first, last, email, age, salary, department):
    edit_button = context.driver.find_element(By.XPATH, "//span[@title='Edit']")
    context.driver.execute_script("arguments[0].scrollIntoView(true);", edit_button)
    edit_button.click()

    wait = WebDriverWait(context.driver, 10)
    wait.until(EC.visibility_of_element_located((By.ID, "firstName"))).clear()
    context.driver.find_element(By.ID, "firstName").send_keys(first)
    context.driver.find_element(By.ID, "lastName").clear()
    context.driver.find_element(By.ID, "lastName").send_keys(last)
    context.driver.find_element(By.ID, "userEmail").clear()
    context.driver.find_element(By.ID, "userEmail").send_keys(email)
    context.driver.find_element(By.ID, "age").clear()
    context.driver.find_element(By.ID, "age").send_keys(age)
    context.driver.find_element(By.ID, "salary").clear()
    context.driver.find_element(By.ID, "salary").send_keys(salary)
    context.driver.find_element(By.ID, "department").clear()
    context.driver.find_element(By.ID, "department").send_keys(department)

    submit_button = context.driver.find_element(By.ID, "submit")
    context.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
    context.driver.execute_script("arguments[0].click();", submit_button)

@then('o registro editado deve estar visível')
def step_validate_edited_record(context):
    table = context.driver.find_element(By.CLASS_NAME, "rt-table")
    assert "QA Sênior" in table.text

@when('exclui o registro criado')
def step_delete_record(context):
    delete_button = context.driver.find_element(By.XPATH, "//span[@title='Delete']")
    context.driver.execute_script("arguments[0].scrollIntoView(true);", delete_button)
    delete_button.click()

@then('o registro não deve mais estar visível')
def step_validate_deletion(context):
    wait = WebDriverWait(context.driver, 10)
    table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rt-table")))
    assert "Pandora" not in table.text
    context.driver.save_screenshot("evidencia_web_tables.png")
    context.driver.quit()