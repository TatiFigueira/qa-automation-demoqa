"""
Centralized configuration settings for the QA automation project.
"""
import os
from dataclasses import dataclass
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class Settings:
    """Application settings loaded from environment variables."""
    
    # Base Configuration
    BASE_URL: str = os.getenv("BASE_URL", "https://demoqa.com")
    TIMEOUT: int = int(os.getenv("TIMEOUT", "10"))
    BROWSER: str = os.getenv("BROWSER", "chrome")
    HEADLESS: bool = os.getenv("HEADLESS", "false").lower() == "true"
    
    # Screenshot Configuration
    SCREENSHOT_PATH: str = os.getenv("SCREENSHOT_PATH", "reports/screenshots")
    SCREENSHOT_ON_FAILURE: bool = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
    
    # Reporting
    ALLURE_RESULTS_DIR: str = os.getenv("ALLURE_RESULTS_DIR", "reports/allure-results")
    HTML_REPORTS_DIR: str = os.getenv("HTML_REPORTS_DIR", "reports/html-reports")
    
    # Test Configuration
    PARALLEL_WORKERS: int = int(os.getenv("PARALLEL_WORKERS", "4"))
    RETRY_COUNT: int = int(os.getenv("RETRY_COUNT", "2"))
    
    # API Configuration
    API_BASE_URL: str = os.getenv("API_BASE_URL", "https://demoqa.com/api")
    API_TIMEOUT: int = int(os.getenv("API_TIMEOUT", "30"))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # Specific URLs
    @property
    def LOGIN_URL(self) -> str:
        return f"{self.BASE_URL}/login"
    
    @property
    def FORM_URL(self) -> str:
        return f"{self.BASE_URL}/automation-practice-form"
    
    @property
    def PROGRESS_BAR_URL(self) -> str:
        return f"{self.BASE_URL}/progress-bar"
    
    @property
    def WEB_TABLES_URL(self) -> str:
        return f"{self.BASE_URL}/webtables"
    
    @property
    def BOOKS_URL(self) -> str:
        return f"{self.BASE_URL}/books"
    
    @property
    def PROFILE_URL(self) -> str:
        return f"{self.BASE_URL}/profile"
    
    def get_browser_options(self) -> Dict[str, Any]:
        """Get browser-specific options."""
        options = {
            "chrome": {
                "args": [
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--window-size=1920,1080"
                ]
            },
            "firefox": {
                "args": [
                    "--width=1920",
                    "--height=1080"
                ]
            },
            "edge": {
                "args": [
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--window-size=1920,1080"
                ]
            }
        }
        
        if self.HEADLESS:
            if self.BROWSER == "chrome":
                options["chrome"]["args"].append("--headless")
            elif self.BROWSER == "firefox":
                options["firefox"]["args"].append("--headless")
            elif self.BROWSER == "edge":
                options["edge"]["args"].append("--headless")
        
        return options.get(self.BROWSER, {})


# Global settings instance
settings = Settings()
