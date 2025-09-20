"""
Data generation utilities for test automation.
"""
import random
import string
from datetime import datetime, timedelta
from typing import Dict, List, Any
from faker import Faker


class DataGenerator:
    """Data generator for test data creation."""
    
    def __init__(self, locale: str = 'pt_BR'):
        """Initialize the data generator with locale."""
        self.fake = Faker(locale)
        self.fake_en = Faker('en_US')  # For English data when needed
    
    def generate_user_data(self) -> Dict[str, Any]:
        """Generate complete user data for forms."""
        return {
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "email": self.fake.email(),
            "phone": self.fake.phone_number(),
            "mobile": self.generate_mobile_number(),
            "address": self.fake.address(),
            "city": self.fake.city(),
            "state": self.fake.state(),
            "postal_code": self.fake.postcode(),
            "country": self.fake.country(),
            "age": random.randint(18, 65),
            "salary": random.randint(3000, 15000),
            "company": self.fake.company(),
            "job_title": self.fake.job(),
            "website": self.fake.url()
        }
    
    def generate_form_data(self) -> Dict[str, Any]:
        """Generate data specifically for practice form."""
        return {
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "email": self.fake.email(),
            "gender": random.choice(["Male", "Female", "Other"]),
            "mobile": self.generate_mobile_number(),
            "date_of_birth": self.generate_date_of_birth(),
            "subjects": self.generate_subjects(),
            "hobbies": self.generate_hobbies(),
            "current_address": self.fake.address(),
            "state": self.fake.state(),
            "city": self.fake.city()
        }
    
    def generate_mobile_number(self) -> str:
        """Generate a valid mobile number for forms."""
        # Generate 10-digit mobile number
        return ''.join([str(random.randint(0, 9)) for _ in range(10)])
    
    def generate_date_of_birth(self) -> str:
        """Generate a date of birth in DD MMM YYYY format."""
        start_date = datetime(1950, 1, 1)
        end_date = datetime(2005, 12, 31)
        random_date = self.fake.date_between(start_date=start_date, end_date=end_date)
        return random_date.strftime("%d %b %Y")
    
    def generate_subjects(self, count: int = None) -> List[str]:
        """Generate random subjects."""
        subjects = [
            "Math", "Physics", "Chemistry", "Biology", "Computer Science",
            "English", "History", "Geography", "Economics", "Art",
            "Music", "Physical Education", "Literature", "Philosophy"
        ]
        count = count or random.randint(1, 3)
        return random.sample(subjects, min(count, len(subjects)))
    
    def generate_hobbies(self, count: int = None) -> List[str]:
        """Generate random hobbies."""
        hobbies = ["Sports", "Reading", "Music"]
        count = count or random.randint(1, 3)
        return random.sample(hobbies, min(count, len(hobbies)))
    
    def generate_web_table_data(self, count: int = 5) -> List[Dict[str, Any]]:
        """Generate data for web tables."""
        data = []
        for _ in range(count):
            data.append({
                "first_name": self.fake.first_name(),
                "last_name": self.fake.last_name(),
                "email": self.fake.email(),
                "age": random.randint(18, 65),
                "salary": random.randint(3000, 15000),
                "department": random.choice([
                    "Compliance", "Insurance", "Legal", "Engineering",
                    "Human Resources", "Marketing", "Sales", "Finance"
                ])
            })
        return data
    
    def generate_api_data(self) -> Dict[str, Any]:
        """Generate data for API testing."""
        return {
            "title": self.fake.sentence(nb_words=3),
            "body": self.fake.text(max_nb_chars=200),
            "userId": random.randint(1, 100),
            "id": random.randint(1, 1000),
            "completed": random.choice([True, False])
        }
    
    def generate_file_data(self) -> Dict[str, Any]:
        """Generate file-related test data."""
        return {
            "filename": f"test_file_{random.randint(1000, 9999)}.txt",
            "content": self.fake.text(max_nb_chars=500),
            "file_size": random.randint(1024, 10240),  # 1KB to 10KB
            "file_type": random.choice(["txt", "pdf", "doc", "jpg", "png"])
        }
    
    def generate_performance_data(self, count: int = 100) -> List[Dict[str, Any]]:
        """Generate data for performance testing."""
        data = []
        for i in range(count):
            data.append({
                "id": i + 1,
                "name": f"Performance Test Item {i + 1}",
                "value": random.randint(1, 1000),
                "timestamp": datetime.now().isoformat(),
                "category": random.choice(["A", "B", "C", "D", "E"])
            })
        return data
    
    def generate_random_string(self, length: int = 10, include_digits: bool = True) -> str:
        """Generate a random string."""
        characters = string.ascii_letters
        if include_digits:
            characters += string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    
    def generate_email_variations(self, base_email: str) -> List[str]:
        """Generate email variations for testing."""
        name, domain = base_email.split('@')
        variations = [
            f"{name}+test@{domain}",
            f"{name}.test@{domain}",
            f"test.{name}@{domain}",
            f"{name}_{random.randint(100, 999)}@{domain}"
        ]
        return variations
    
    def generate_phone_variations(self, base_phone: str) -> List[str]:
        """Generate phone number variations for testing."""
        variations = [
            f"({base_phone[:2]}) {base_phone[2:6]}-{base_phone[6:]}",
            f"+55 {base_phone[:2]} {base_phone[2:6]}-{base_phone[6:]}",
            f"{base_phone[:2]}.{base_phone[2:6]}.{base_phone[6:]}",
            f"{base_phone[:2]}-{base_phone[2:6]}-{base_phone[6:]}"
        ]
        return variations
    
    def generate_invalid_data(self) -> Dict[str, Any]:
        """Generate invalid data for negative testing."""
        return {
            "invalid_email": "invalid-email",
            "invalid_phone": "123",
            "invalid_date": "32/13/2023",
            "empty_string": "",
            "special_chars": "!@#$%^&*()",
            "sql_injection": "'; DROP TABLE users; --",
            "xss_attack": "<script>alert('XSS')</script>",
            "very_long_string": "x" * 1000
        }
    
    def generate_edge_case_data(self) -> Dict[str, Any]:
        """Generate edge case data for boundary testing."""
        return {
            "min_length_string": "a",
            "max_length_string": "x" * 255,
            "unicode_string": "测试字符串",
            "numeric_string": "12345",
            "mixed_case": "TeStInG",
            "whitespace_only": "   ",
            "newline_string": "line1\nline2\nline3",
            "tab_string": "col1\tcol2\tcol3"
        }
    
    def generate_login_credentials(self) -> Dict[str, str]:
        """Generate login credentials for testing."""
        return {
            "valid_username": "pandoraTeste",
            "valid_password": "Pandora@123",
            "invalid_username": f"invalid_user_{random.randint(1000, 9999)}",
            "invalid_password": f"wrong_pass_{random.randint(1000, 9999)}",
            "empty_username": "",
            "empty_password": ""
        }
    
    def generate_progress_bar_test_data(self) -> Dict[str, Any]:
        """Generate data for progress bar testing."""
        return {
            "start_value": 0,
            "target_stop_value": random.randint(15, 25),
            "end_value": 100,
            "reset_value": 0,
            "test_intervals": [10, 25, 50, 75, 90, 100]
        }
    
    def generate_web_table_test_data(self) -> Dict[str, Any]:
        """Generate specific data for web table testing."""
        return {
            "create_data": {
                "firstName": "Tatiana",
                "lastName": "QA",
                "email": "figueira.qa@teste.com",
                "age": "30",
                "salary": "5000",
                "department": "TesteCorp"
            },
            "edit_data": {
                "firstName": "Pandora",
                "lastName": "QA Sênior",
                "email": "pandora@qa.com",
                "age": "31",
                "salary": "7000",
                "department": "QAcorp"
            },
            "search_terms": ["Cierra", "cierra@example.com", "29", "10000", "Insurance"],
            "invalid_data": {
                "firstName": "",
                "lastName": "",
                "email": "invalid-email",
                "age": "abc",
                "salary": "-1000",
                "department": ""
            }
        }
    
    def generate_browser_window_test_data(self) -> Dict[str, Any]:
        """Generate data for browser window testing."""
        return {
            "original_window_title": "DEMOQA",
            "new_tab_expected_content": "sample",
            "navigation_urls": [
                "https://demoqa.com/sample",
                "https://demoqa.com/browser-windows",
                "https://demoqa.com/"
            ]
        }
    
    def generate_form_validation_data(self) -> Dict[str, Any]:
        """Generate data for form validation testing."""
        return {
            "required_fields": ["firstName", "lastName", "userEmail", "userNumber"],
            "email_validation": {
                "valid": ["test@example.com", "user.name@domain.co.uk", "test+tag@example.org"],
                "invalid": ["invalid-email", "@domain.com", "test@", "test@domain", "test..test@domain.com"]
            },
            "phone_validation": {
                "valid": ["1234567890", "9876543210", "5555555555"],
                "invalid": ["123", "abc1234567", "123-456-789", "123.456.7890"]
            },
            "age_validation": {
                "valid": ["18", "25", "65", "30"],
                "invalid": ["abc", "17", "66", "-5", "0"]
            }
        }


# Global data generator instance
data_generator = DataGenerator()
