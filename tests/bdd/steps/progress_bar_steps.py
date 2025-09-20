from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@when('ele clica em "Widgets"')
def step_click_widgets(context):
    wait = WebDriverWait(context.driver, 10)
    widgets = wait.until(EC.element_to_be_clickable((By.XPATH, "//h5[text()='Widgets']")))
    context.driver.execute_script("arguments[0].scrollIntoView(true);", widgets)
    widgets.click()

@when('acessa o submenu "Progress Bar"')
def step_click_progress_bar(context):
    wait = WebDriverWait(context.driver, 10)
    submenu = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Progress Bar']")))
    context.driver.execute_script("arguments[0].scrollIntoView(true);", submenu)
    submenu.click()

@when('inicia o progresso e para antes de 25%')
def step_start_and_stop(context):
    start_button = context.driver.find_element(By.ID, "startStopButton")
    context.driver.execute_script("arguments[0].scrollIntoView(true);", start_button)
    start_button.click()
    while True:
        value = context.driver.find_element(By.CLASS_NAME, "progress-bar").get_attribute("aria-valuenow")
        if int(value) <= 20:
            start_button.click()
            break
        time.sleep(0.3)

@then('o valor da barra deve ser menor ou igual a 25%')
def step_validate_partial_progress(context):
    value = context.driver.find_element(By.CLASS_NAME, "progress-bar").get_attribute("aria-valuenow")
    assert int(value) <= 25

@when('inicia novamente e aguarda até 100%')
def step_start_to_full(context):
    start_button = context.driver.find_element(By.ID, "startStopButton")
    start_button.click()
    while True:
        value = context.driver.find_element(By.CLASS_NAME, "progress-bar").get_attribute("aria-valuenow")
        if int(value) == 100:
            break
        time.sleep(0.1)

@then('a barra deve ser resetada')
def step_reset_bar(context):
    wait = WebDriverWait(context.driver, 10)
    reset_button = wait.until(EC.element_to_be_clickable((By.ID, "resetButton")))
    reset_button.click()
    time.sleep(2)
    value = context.driver.find_element(By.CLASS_NAME, "progress-bar").get_attribute("aria-valuenow")
    print(f"Valor da barra após reset: {value}")
    start_button = context.driver.find_element(By.ID, "startStopButton")
    button_text = start_button.text
    assert int(value) == 0 or button_text == "Start", f"Barra não foi resetada. Valor: {value}, Texto do botão: {button_text}"
    context.driver.save_screenshot("reports/screenshots/evidencia_progress_bar.png")
    context.driver.quit()
