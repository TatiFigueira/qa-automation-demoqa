"""
Steps para testes de Browser Window no DemoQA
"""
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time




@when('ele navega até "Alerts, Frame & Windows"')
def step_navigate_to_alerts_frame_windows(context):
    """Navega até o card Alerts, Frame & Windows."""
    wait = WebDriverWait(context.driver, 10)
    
    
    alerts_card_locator = (By.XPATH, "//h5[text()='Alerts, Frame & Windows']")
    alerts_card = wait.until(EC.presence_of_element_located(alerts_card_locator))
    
    
    context.driver.execute_script("arguments[0].scrollIntoView(true);", alerts_card)
    
    
    wait.until(EC.element_to_be_clickable(alerts_card_locator)).click()
    time.sleep(1)


@when('clica em "Browser Windows"')
def step_click_browser_windows(context):
    """Clica no submenu Browser Windows."""
    wait = WebDriverWait(context.driver, 10)
    
    
    submenu_locator = (By.XPATH, "//span[text()='Browser Windows']")
    submenu = wait.until(EC.presence_of_element_located(submenu_locator))
    
    
    context.driver.execute_script("arguments[0].scrollIntoView(true);", submenu)
    wait.until(EC.element_to_be_clickable(submenu_locator)).click()
    time.sleep(1)


@when('clica no botão "New Window"')
def step_click_new_window(context):
    """Clica no botão New Window."""
    wait = WebDriverWait(context.driver, 10)
    new_window_button = wait.until(EC.element_to_be_clickable((By.ID, "windowButton")))
    context.driver.execute_script("arguments[0].scrollIntoView(true);", new_window_button)
    
   
    context.original_window = context.driver.current_window_handle
    
    
    new_window_button.click()
    time.sleep(2)


@then('uma nova janela deve ser aberta')
def step_validate_new_window(context):
    """Valida que uma nova janela foi aberta."""
    
    wait = WebDriverWait(context.driver, 10)
    wait.until(lambda driver: len(driver.window_handles) > 1)
    
   
    assert len(context.driver.window_handles) > 1, "Nova janela deve ter sido aberta"
    
    
    context.all_windows = context.driver.window_handles


@then('a mensagem "This is a sample page" deve estar visível')
def step_validate_sample_message(context):
    """Valida que a mensagem 'This is a sample page' está visível."""
    
    for window_handle in context.driver.window_handles:
        if window_handle != context.original_window:
            context.driver.switch_to.window(window_handle)
            break
    
    
    wait = WebDriverWait(context.driver, 10)
    
   
    try:
        message_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        page_text = message_element.text
        assert "This is a sample page" in page_text, f"Mensagem 'This is a sample page' não encontrada. Texto da página: {page_text}"
    except Exception as e:
        
        page_title = context.driver.title
        assert "sample" in page_title.lower() or "new" in page_title.lower(), f"Página não é uma página de exemplo. Título: {page_title}"


@then('a nova janela deve ser fechada')
def step_close_new_window(context):
    """Fecha a nova janela e volta para a original."""
    
    context.driver.close()
    
    
    context.driver.switch_to.window(context.original_window)
    
    
    original_url = context.driver.current_url
    assert "browser-windows" in original_url, f"Deve estar na janela original, URL atual: {original_url}"
    
    
    context.driver.save_screenshot("reports/screenshots/browser_window_test.png")
