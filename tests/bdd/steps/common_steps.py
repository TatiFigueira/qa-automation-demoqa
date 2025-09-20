"""
Steps comuns para todos os testes BDD
"""
import os
import sys
import logging
from behave import given
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger("BDD-Tests")

def setup_chrome_driver():
    """Setup Chrome WebDriver com tratamento robusto de binários."""
    options = Options()
    
    
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    try:
        
        install_path = ChromeDriverManager().install()
        logger.info(f"ChromeDriverManager reportou caminho de instalação: {install_path}")
        
        # Busca pelo binário do chromedriver
        binary_path = None
        parent_dir = os.path.dirname(install_path)
        
       
        def is_executable_binary(path):
            if not os.path.isfile(path):
                return False
                
            
            try:
                if sys.platform != 'win32':
                    
                    if not os.access(path, os.X_OK):
                        os.chmod(path, 0o755)
                        
                  
                    with open(path, 'rb') as f:
                        header = f.read(4)
                         
                        valid_headers = [b'\x7fELF', b'MZ', b'\xca\xfe\xba\xbe', b'\xce\xfa\xed\xfe']
                        return any(header.startswith(h) for h in valid_headers)
                else:
                   
                    return path.lower().endswith('.exe')
            except Exception as e:
                logger.error(f"Erro na verificação do binário {path}: {e}")
                return False
        
        
        exact_match = os.path.join(parent_dir, 'chromedriver')
        if os.path.isfile(exact_match) and is_executable_binary(exact_match):
            binary_path = exact_match
        
        
        elif sys.platform == 'darwin':
            mac_patterns = ['chromedriver_mac64', 'chromedriver_mac_arm64', 'chromedriver-mac']
            for pattern in mac_patterns:
                for file in os.listdir(parent_dir):
                    if pattern in file.lower() and is_executable_binary(os.path.join(parent_dir, file)):
                        binary_path = os.path.join(parent_dir, file)
                        break
                if binary_path:
                    break
        
        
        if not binary_path:
            for file in os.listdir(parent_dir):
                file_lower = file.lower()
                # Pular arquivos não-binários comuns
                if any(exclude in file_lower for exclude in ['license', 'notice', 'third_party', 'readme', '.txt']):
                    continue
                
               
                if 'chromedriver' in file_lower:
                    candidate = os.path.join(parent_dir, file)
                    if is_executable_binary(candidate):
                        binary_path = candidate
                        break
        
        
        if not binary_path:
            logger.info("Nenhum binário chromedriver adequado encontrado, criando serviço diretamente")
            service = Service(ChromeDriverManager().install())
        else:
            
            if sys.platform != 'win32':
                os.chmod(binary_path, 0o755)
            service = Service(binary_path)
        
    except Exception as e:
        logger.error(f"Erro durante configuração do chromedriver: {e}")
       
        service = Service(ChromeDriverManager().install())
    
    return webdriver.Chrome(service=service, options=options)


@given('que o usuário acessa o site DemoQA')
def step_open_demoqa(context):
    """Acessa o site DemoQA."""
    # Inicializa o logger
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
   
    context.driver = setup_chrome_driver()
    context.driver.get("https://demoqa.com")
    context.driver.maximize_window()
    
    
    context.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    logger.info("Site DemoQA acessado com sucesso")
