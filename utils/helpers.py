"""
Helper utilities for test automation.
"""
import os
import time
import json
import hashlib
import requests
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


class WebDriverHelper:
    """Helper class for WebDriver operations."""
    
    def __init__(self, driver):
        """Initialize with WebDriver instance."""
        self.driver = driver
        self.wait = WebDriverWait(driver, settings.TIMEOUT)
    
    def wait_for_page_load(self, timeout: int = None) -> bool:
        """Wait for page to load completely."""
        timeout = timeout or settings.TIMEOUT
        try:
            self.wait.until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            return True
        except TimeoutException:
            logger.warning("Page load timeout exceeded")
            return False
    
    def scroll_to_bottom(self) -> None:
        """Scroll to bottom of page."""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
    
    def scroll_to_top(self) -> None:
        """Scroll to top of page."""
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
    
    def scroll_to_element(self, element) -> None:
        """Scroll to specific element."""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)
    
    def get_page_height(self) -> int:
        """Get total page height."""
        return self.driver.execute_script("return document.body.scrollHeight")
    
    def get_viewport_height(self) -> int:
        """Get viewport height."""
        return self.driver.execute_script("return window.innerHeight")
    
    def is_element_in_viewport(self, element) -> bool:
        """Check if element is in viewport."""
        return self.driver.execute_script(
            "var rect = arguments[0].getBoundingClientRect();"
            "return (rect.top >= 0 && rect.left >= 0 && "
            "rect.bottom <= window.innerHeight && "
            "rect.right <= window.innerWidth);",
            element
        )


class FileHelper:
    """Helper class for file operations."""
    
    @staticmethod
    def create_test_file(filename: str, content: str, directory: str = "temp") -> str:
        """Create a test file with content."""
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, filename)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Created test file: {file_path}")
        return file_path
    
    @staticmethod
    def delete_file(file_path: str) -> bool:
        """Delete a file."""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Deleted file: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete file {file_path}: {e}")
            return False
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """Get file size in bytes."""
        try:
            return os.path.getsize(file_path)
        except OSError:
            return 0
    
    @staticmethod
    def create_screenshot_directory() -> str:
        """Create screenshot directory if it doesn't exist."""
        os.makedirs(settings.SCREENSHOT_PATH, exist_ok=True)
        return settings.SCREENSHOT_PATH


class ValidationHelper:
    """Helper class for data validation."""
    
    @staticmethod
    def is_valid_email(email: str) -> bool:
        """Validate email format."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        """Validate phone number format."""
        import re
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', phone)
        # Check if it has 10 or 11 digits
        return len(digits_only) in [10, 11]
    
    @staticmethod
    def is_valid_date(date_string: str, format_string: str = "%d %b %Y") -> bool:
        """Validate date format."""
        try:
            datetime.strptime(date_string, format_string)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Validate URL format."""
        import re
        pattern = r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?$'
        return bool(re.match(pattern, url))


class PerformanceHelper:
    """Helper class for performance testing."""
    
    def __init__(self):
        """Initialize performance helper."""
        self.start_times = {}
        self.metrics = {}
    
    def start_timer(self, operation: str) -> None:
        """Start timing an operation."""
        self.start_times[operation] = time.time()
        logger.debug(f"Started timing: {operation}")
    
    def end_timer(self, operation: str) -> float:
        """End timing an operation and return duration."""
        if operation not in self.start_times:
            logger.warning(f"No start time found for operation: {operation}")
            return 0.0
        
        duration = time.time() - self.start_times[operation]
        self.metrics[operation] = duration
        logger.info(f"Operation '{operation}' took {duration:.2f} seconds")
        return duration
    
    def get_metrics(self) -> Dict[str, float]:
        """Get all performance metrics."""
        return self.metrics.copy()
    
    def reset_metrics(self) -> None:
        """Reset all metrics."""
        self.start_times.clear()
        self.metrics.clear()


class APIHelper:
    """Helper class for API testing."""
    
    def __init__(self, base_url: str = None):
        """Initialize API helper."""
        self.base_url = base_url or settings.API_BASE_URL
        self.session = requests.Session()
        self.session.timeout = settings.API_TIMEOUT
    
    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """Make GET request."""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"GET request to: {url}")
        return self.session.get(url, **kwargs)
    
    def post(self, endpoint: str, data: Dict[str, Any] = None, **kwargs) -> requests.Response:
        """Make POST request."""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"POST request to: {url}")
        return self.session.post(url, json=data, **kwargs)
    
    def put(self, endpoint: str, data: Dict[str, Any] = None, **kwargs) -> requests.Response:
        """Make PUT request."""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PUT request to: {url}")
        return self.session.put(url, json=data, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """Make DELETE request."""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"DELETE request to: {url}")
        return self.session.delete(url, **kwargs)
    
    def validate_response(self, response: requests.Response, expected_status: int = 200) -> bool:
        """Validate API response."""
        if response.status_code != expected_status:
            logger.error(f"Expected status {expected_status}, got {response.status_code}")
            return False
        
        try:
            response.json()  # Validate JSON format
            return True
        except ValueError:
            logger.error("Response is not valid JSON")
            return False


class DataHelper:
    """Helper class for data manipulation."""
    
    @staticmethod
    def generate_hash(data: str) -> str:
        """Generate MD5 hash of data."""
        return hashlib.md5(data.encode()).hexdigest()
    
    @staticmethod
    def generate_timestamp() -> str:
        """Generate current timestamp."""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    @staticmethod
    def format_currency(amount: float, currency: str = "USD") -> str:
        """Format amount as currency."""
        if currency == "USD":
            return f"${amount:,.2f}"
        elif currency == "EUR":
            return f"€{amount:,.2f}"
        elif currency == "BRL":
            return f"R${amount:,.2f}"
        else:
            return f"{amount:,.2f} {currency}"
    
    @staticmethod
    def clean_string(text: str) -> str:
        """Clean string by removing extra whitespace."""
        return " ".join(text.split())
    
    @staticmethod
    def extract_numbers(text: str) -> List[int]:
        """Extract all numbers from text."""
        import re
        return [int(x) for x in re.findall(r'\d+', text)]
    
    @staticmethod
    def compare_lists(list1: List[Any], list2: List[Any]) -> bool:
        """Compare two lists for equality."""
        return sorted(list1) == sorted(list2)


class AssertionHelper:
    """Helper class for custom assertions."""
    
    @staticmethod
    def assert_contains(actual: str, expected: str, message: str = None) -> None:
        """Assert that actual contains expected."""
        if expected not in actual:
            error_msg = message or f"Expected '{expected}' to be in '{actual}'"
            raise AssertionError(error_msg)
    
    @staticmethod
    def assert_not_contains(actual: str, expected: str, message: str = None) -> None:
        """Assert that actual does not contain expected."""
        if expected in actual:
            error_msg = message or f"Expected '{expected}' not to be in '{actual}'"
            raise AssertionError(error_msg)
    
    @staticmethod
    def assert_greater_than(actual: float, expected: float, message: str = None) -> None:
        """Assert that actual is greater than expected."""
        if actual <= expected:
            error_msg = message or f"Expected {actual} to be greater than {expected}"
            raise AssertionError(error_msg)
    
    @staticmethod
    def assert_less_than(actual: float, expected: float, message: str = None) -> None:
        """Assert that actual is less than expected."""
        if actual >= expected:
            error_msg = message or f"Expected {actual} to be less than {expected}"
            raise AssertionError(error_msg)
    
    @staticmethod
    def assert_between(actual: float, min_val: float, max_val: float, message: str = None) -> None:
        """Assert that actual is between min_val and max_val."""
        if not (min_val <= actual <= max_val):
            error_msg = message or f"Expected {actual} to be between {min_val} and {max_val}"
            raise AssertionError(error_msg)
