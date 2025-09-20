"""
Environment configuration for Behave BDD tests
"""
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def before_all(context):
    """Setup before all tests."""
    # Create necessary directories
    os.makedirs("reports/screenshots", exist_ok=True)
    os.makedirs("reports/allure-results", exist_ok=True)
    os.makedirs("reports/html-reports", exist_ok=True)


def before_scenario(context, scenario):
    """Setup before each scenario."""
    # Setup Chrome driver
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    service = Service(ChromeDriverManager().install())
    context.driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Execute script to remove webdriver property
    context.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")


def after_scenario(context, scenario):
    """Cleanup after each scenario."""
    if hasattr(context, 'driver'):
        context.driver.quit()


def after_all(context):
    """Cleanup after all tests."""
    pass
