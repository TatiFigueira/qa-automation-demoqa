"""
Structured logging utility for the QA automation project.
"""
import logging
import json
import sys
from datetime import datetime
from typing import Dict, Any, Optional
from config.settings import settings


class StructuredLogger:
    """Structured logger for test automation."""
    
    def __init__(self, name: str, level: str = None):
        """Initialize the structured logger."""
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level or settings.LOG_LEVEL))
        
        # Prevent duplicate handlers
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self) -> None:
        """Setup log handlers."""
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # File handler
        file_handler = logging.FileHandler('reports/automation.log')
        file_handler.setLevel(logging.DEBUG)
        
        # Formatter
        formatter = logging.Formatter(settings.LOG_FORMAT)
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        # Add handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def _log_structured(self, level: str, message: str, **kwargs) -> None:
        """Log structured message."""
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
            **kwargs
        }
        
        log_message = json.dumps(log_data, ensure_ascii=False)
        getattr(self.logger, level.lower())(log_message)
    
    def debug(self, message: str, **kwargs) -> None:
        """Log debug message."""
        self._log_structured("DEBUG", message, **kwargs)
    
    def info(self, message: str, **kwargs) -> None:
        """Log info message."""
        self._log_structured("INFO", message, **kwargs)
    
    def warning(self, message: str, **kwargs) -> None:
        """Log warning message."""
        self._log_structured("WARNING", message, **kwargs)
    
    def error(self, message: str, **kwargs) -> None:
        """Log error message."""
        self._log_structured("ERROR", message, **kwargs)
    
    def critical(self, message: str, **kwargs) -> None:
        """Log critical message."""
        self._log_structured("CRITICAL", message, **kwargs)
    
    def log_test_start(self, test_name: str, test_class: str = None) -> None:
        """Log test start event."""
        self.info(
            "Test started",
            event="test_start",
            test_name=test_name,
            test_class=test_class
        )
    
    def log_test_end(self, test_name: str, status: str, duration: float = None, **kwargs) -> None:
        """Log test end event."""
        self.info(
            "Test completed",
            event="test_end",
            test_name=test_name,
            status=status,
            duration=duration,
            **kwargs
        )
    
    def log_test_failure(self, test_name: str, error: str, screenshot_path: str = None) -> None:
        """Log test failure event."""
        self.error(
            "Test failed",
            event="test_failure",
            test_name=test_name,
            error=error,
            screenshot_path=screenshot_path
        )
    
    def log_page_navigation(self, page_name: str, url: str) -> None:
        """Log page navigation event."""
        self.info(
            "Page navigation",
            event="page_navigation",
            page_name=page_name,
            url=url
        )
    
    def log_element_interaction(self, action: str, element: str, value: str = None) -> None:
        """Log element interaction event."""
        self.debug(
            "Element interaction",
            event="element_interaction",
            action=action,
            element=element,
            value=value
        )
    
    def log_assertion(self, assertion_type: str, expected: Any, actual: Any, result: bool) -> None:
        """Log assertion event."""
        self.debug(
            "Assertion",
            event="assertion",
            assertion_type=assertion_type,
            expected=expected,
            actual=actual,
            result=result
        )
    
    def log_performance(self, operation: str, duration: float, **metrics) -> None:
        """Log performance metrics."""
        self.info(
            "Performance metric",
            event="performance",
            operation=operation,
            duration=duration,
            **metrics
        )


def get_logger(name: str) -> StructuredLogger:
    """Get a logger instance."""
    return StructuredLogger(name)
