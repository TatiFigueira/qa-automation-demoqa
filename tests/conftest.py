"""
Pytest configuration and fixtures for the QA automation project.
"""
import os
import sys
import pytest
import allure
import logging
import subprocess
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from config.settings import settings
from utils.logger import get_logger
from utils.helpers import PerformanceHelper

logger = get_logger(__name__)


def pytest_configure(config):
    """Configure pytest with custom settings."""
    # Create necessary directories
    os.makedirs(settings.SCREENSHOT_PATH, exist_ok=True)
    os.makedirs(settings.ALLURE_RESULTS_DIR, exist_ok=True)
    os.makedirs(settings.HTML_REPORTS_DIR, exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format=settings.LOG_FORMAT,
        handlers=[
            logging.FileHandler('reports/automation.log'),
            logging.StreamHandler()
        ]
    )


def pytest_runtest_setup(item):
    """Setup for each test."""
    logger.info(f"Starting test: {item.name}")


def pytest_runtest_teardown(item, nextitem):
    """Teardown for each test."""
    logger.info(f"Completed test: {item.name}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Generate test report with screenshots on failure."""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        # Take screenshot on failure
        if hasattr(item, "funcargs") and "browser" in item.funcargs:
            browser = item.funcargs["browser"]
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_name = f"failure_{item.name}_{timestamp}.png"
                screenshot_path = os.path.join(settings.SCREENSHOT_PATH, screenshot_name)
                browser.save_screenshot(screenshot_path)
                
                # Attach to Allure report
                allure.attach(
                    browser.get_screenshot_as_png(),
                    name="screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
                
                logger.error(f"Screenshot saved: {screenshot_path}")
            except Exception as e:
                logger.error(f"Failed to take screenshot: {e}")


@pytest.fixture(scope="session")
def browser():
    """Session-scoped browser fixture."""
    driver = None
    try:
        # Setup browser based on configuration
        if settings.BROWSER.lower() == "chrome":
            driver = _setup_chrome_driver()
        elif settings.BROWSER.lower() == "firefox":
            driver = _setup_firefox_driver()
        elif settings.BROWSER.lower() == "edge":
            driver = _setup_edge_driver()
        else:
            raise ValueError(f"Unsupported browser: {settings.BROWSER}")
        
        # Configure driver
        driver.maximize_window()
        driver.implicitly_wait(settings.TIMEOUT)
        
        logger.info(f"Browser {settings.BROWSER} initialized successfully")
        yield driver
        
    except Exception as e:
        logger.error(f"Failed to initialize browser: {e}")
        raise
    finally:
        if driver:
            driver.quit()
            logger.info("Browser closed")


@pytest.fixture(scope="function")
def browser_function():
    """Function-scoped browser fixture for isolated tests."""
    driver = None
    try:
        # Setup browser based on configuration
        if settings.BROWSER.lower() == "chrome":
            driver = _setup_chrome_driver()
        elif settings.BROWSER.lower() == "firefox":
            driver = _setup_firefox_driver()
        elif settings.BROWSER.lower() == "edge":
            driver = _setup_edge_driver()
        else:
            raise ValueError(f"Unsupported browser: {settings.BROWSER}")
        
        # Configure driver
        driver.maximize_window()
        driver.implicitly_wait(settings.TIMEOUT)
        
        logger.info(f"Browser {settings.BROWSER} initialized for function")
        yield driver
        
    except Exception as e:
        logger.error(f"Failed to initialize browser: {e}")
        raise
    finally:
        if driver:
            driver.quit()
            logger.info("Browser closed for function")


def _setup_chrome_driver():
    """Setup Chrome WebDriver."""
    options = ChromeOptions()
    
    # Add options based on configuration
    browser_options = settings.get_browser_options()
    for arg in browser_options.get("args", []):
        options.add_argument(arg)
    
    # Additional Chrome options
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Setup service - use direct chromedriver binary instead of relying on ChromeDriverManager
    try:
        # Get ChromeDriver using the Manager
        from webdriver_manager.chrome import ChromeDriverManager
        
        # Get the installation path but don't use it directly
        install_path = ChromeDriverManager().install()
        logger.info(f"ChromeDriverManager reported install path: {install_path}")
        
        # Special handling for macOS - sometimes the binary name is different
        binary_path = None
        parent_dir = os.path.dirname(install_path)
        
        # Diagnostic log
        logger.info(f"Looking for chromedriver binary in directory: {parent_dir}")
        try:
            dir_contents = os.listdir(parent_dir)
            logger.info(f"Directory contents: {dir_contents}")
        except Exception as e:
            logger.error(f"Failed to list directory contents: {e}")
        
        # Verification function for binary
        def is_executable_binary(path):
            if not os.path.isfile(path):
                return False
                
            # For MacOS/Linux - check file header for executable
            try:
                if sys.platform != 'win32':
                    # Check if file is executable
                    if not os.access(path, os.X_OK):
                        os.chmod(path, 0o755)  # Make executable
                        
                    # Simple file header check (first 4 bytes of valid binary)
                    with open(path, 'rb') as f:
                        header = f.read(4)
                        # Common executable headers: ELF for Linux, MZ for Windows, Mach-O for Mac
                        valid_headers = [b'\x7fELF', b'MZ', b'\xca\xfe\xba\xbe', b'\xce\xfa\xed\xfe']
                        return any(header.startswith(h) for h in valid_headers)
                else:
                    # On Windows just check the extension
                    return path.lower().endswith('.exe')
            except Exception as e:
                logger.error(f"Binary verification error for {path}: {e}")
                return False
        
        # Search strategy:
        # 1. Look for chromedriver directly (standard name)
        exact_match = os.path.join(parent_dir, 'chromedriver')
        if os.path.isfile(exact_match) and is_executable_binary(exact_match):
            binary_path = exact_match
            logger.info(f"Found chromedriver at exact path: {binary_path}")
        
        # 2. On macOS check for chromedriver_mac64 or similar variants
        elif sys.platform == 'darwin':
            mac_patterns = ['chromedriver_mac64', 'chromedriver_mac_arm64', 'chromedriver-mac']
            for pattern in mac_patterns:
                for file in os.listdir(parent_dir):
                    if pattern in file.lower() and is_executable_binary(os.path.join(parent_dir, file)):
                        binary_path = os.path.join(parent_dir, file)
                        logger.info(f"Found chromedriver macOS variant: {binary_path}")
                        break
        
        # 3. Find any executable that contains 'chromedriver' but exclude notice files
        if not binary_path:
            for file in os.listdir(parent_dir):
                file_lower = file.lower()
                # Skip common non-binary files
                if any(exclude in file_lower for exclude in ['license', 'notice', 'third_party', 'readme', '.txt']):
                    continue
                
                # Look for chromedriver in name
                if 'chromedriver' in file_lower:
                    candidate = os.path.join(parent_dir, file)
                    if is_executable_binary(candidate):
                        binary_path = candidate
                        logger.info(f"Found chromedriver by name pattern: {binary_path}")
                        break
        
        # 4. Last resort - create direct driver with ChromeDriverManager
        if not binary_path:
            logger.info("No suitable chromedriver binary found, creating service directly with ChromeDriverManager")
            from selenium.webdriver.chrome.service import Service as ChromeService
            service = ChromeService(ChromeDriverManager().install())
        else:
            # Make sure binary is executable
            if sys.platform != 'win32':
                os.chmod(binary_path, 0o755)
            service = Service(binary_path)
        
    except Exception as e:
        logger.error(f"Error during chromedriver setup: {e}", exc_info=True)
        # Last attempt - try direct ChromeDriverManager
        logger.info("Trying fallback with direct ChromeDriverManager...")
        service = Service(ChromeDriverManager().install())
    
    # Create driver
    driver = webdriver.Chrome(service=service, options=options)
    # Execute script to remove webdriver property
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver


def _setup_firefox_driver():
    """Setup Firefox WebDriver."""
    options = FirefoxOptions()
    
    # Add options based on configuration
    browser_options = settings.get_browser_options()
    for arg in browser_options.get("args", []):
        options.add_argument(arg)
    
    # Setup service
    service = Service(GeckoDriverManager().install())
    
    # Create driver
    driver = webdriver.Firefox(service=service, options=options)
    
    return driver


def _setup_edge_driver():
    """Setup Edge WebDriver."""
    options = EdgeOptions()
    
    # Add options based on configuration
    browser_options = settings.get_browser_options()
    for arg in browser_options.get("args", []):
        options.add_argument(arg)
    
    # Setup service
    service = Service(EdgeChromiumDriverManager().install())
    
    # Create driver
    driver = webdriver.Edge(service=service, options=options)
    
    return driver


@pytest.fixture(scope="function")
def performance_helper():
    """Performance helper fixture."""
    helper = PerformanceHelper()
    yield helper
    # Log final metrics
    metrics = helper.get_metrics()
    if metrics:
        logger.info(f"Performance metrics: {metrics}")


@pytest.fixture(scope="function")
def test_data():
    """Test data fixture."""
    from utils.data_generator import data_generator
    return data_generator.generate_form_data()


@pytest.fixture(scope="function")
def user_data():
    """User data fixture."""
    from utils.data_generator import data_generator
    return data_generator.generate_user_data()


@pytest.fixture(scope="function")
def api_helper():
    """API helper fixture."""
    from utils.helpers import APIHelper
    return APIHelper()




@pytest.fixture(autouse=True)
def test_logger(request):
    """Test logger fixture."""
    test_name = request.node.name
    test_logger = get_logger(f"test.{test_name}")
    
    # Log test start
    test_logger.log_test_start(test_name)
    
    yield test_logger
    
    # Log test end
    test_logger.log_test_end(test_name, "completed")


@pytest.fixture(scope="function")
def allure_environment():
    """Allure environment fixture."""
    return {
        "Browser": settings.BROWSER,
        "Base URL": settings.BASE_URL,
        "Headless": str(settings.HEADLESS),
        "Timeout": str(settings.TIMEOUT),
        "Environment": "Test"
    }


# Pytest markers
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line(
        "markers", "smoke: Smoke tests - quick validation"
    )
    config.addinivalue_line(
        "markers", "regression: Regression tests - full validation"
    )
    config.addinivalue_line(
        "markers", "api: API tests"
    )
    config.addinivalue_line(
        "markers", "ui: UI tests"
    )
    config.addinivalue_line(
        "markers", "bdd: BDD tests"
    )
    config.addinivalue_line(
        "markers", "performance: Performance tests"
    )
    config.addinivalue_line(
        "markers", "accessibility: Accessibility tests"
    )


# Pytest collection hooks
def pytest_collection_modifyitems(config, items):
    """Modify test collection."""
    # Add markers based on test location
    for item in items:
        if "api" in str(item.fspath):
            item.add_marker(pytest.mark.api)
        elif "ui" in str(item.fspath):
            item.add_marker(pytest.mark.ui)
        elif "bdd" in str(item.fspath):
            item.add_marker(pytest.mark.bdd)
        elif "performance" in str(item.fspath):
            item.add_marker(pytest.mark.performance)
        elif "accessibility" in str(item.fspath):
            item.add_marker(pytest.mark.accessibility)


# Pytest session hooks
def pytest_sessionstart(session):
    """Session start hook."""
    logger.info("Test session started")
    # Get test count from collected items
    test_count = len(session.items) if hasattr(session, 'items') else 0
    logger.info(f"Running {test_count} tests")


def pytest_sessionfinish(session, exitstatus):
    """Session finish hook."""
    logger.info(f"Test session finished with exit status: {exitstatus}")
    
    # Generate summary if items are available
    if hasattr(session, 'items') and session.items:
        passed = len([item for item in session.items if hasattr(item, 'rep_call') and item.rep_call.passed])
        failed = len([item for item in session.items if hasattr(item, 'rep_call') and item.rep_call.failed])
        skipped = len([item for item in session.items if hasattr(item, 'rep_call') and item.rep_call.skipped])
        
        logger.info(f"Test Summary: {passed} passed, {failed} failed, {skipped} skipped")
    else:
        logger.info("Test session completed")
