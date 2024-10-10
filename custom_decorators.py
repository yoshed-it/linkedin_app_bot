from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_for_element_to_be_clickable(by, value, timeout=10):
    def decorator(func):
        def wrapper(driver, *args, **kwargs):
            clickable_element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))
            return func(driver, clickable_element, *args, **kwargs)
        return wrapper
    return decorator