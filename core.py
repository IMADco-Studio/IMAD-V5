import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from utils import Logger, get_random_user_agent

class FacebookDirectAutomator:
    def __init__(self, email, password, headless=True):
        self.email = email
        self.password = password
        self.headless = headless
        self.driver = self._setup_driver()

    def _setup_driver(self):
        """Configures Chrome with advanced stealth settings."""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless=new")
        
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"user-agent={get_random_user_agent()}")

        driver = webdriver.Chrome(options=chrome_options)

        # Apply Selenium Stealth
        stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        return driver

    def login(self):
        """Automates the login process on m.facebook.com."""
        try:
            Logger.info("Navigating to Facebook Login...")
            self.driver.get("https://m.facebook.com")
            
            # Find and fill email
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_address((By.NAME, "email"))
            )
            time.sleep(random.uniform(1, 2)) # Human jitter
            email_input.send_keys(self.email)
            
            # Find and fill password
            pass_input = self.driver.find_element(By.NAME, "pass")
            time.sleep(random.uniform(1, 2))
            pass_input.send_keys(self.password)
            
            # Press login
            pass_input.send_keys(Keys.RETURN)
            Logger.info("Submitted credentials. Waiting for session...")
            
            # Wait for login success (look for common post-login elements)
            WebDriverWait(self.driver, 20).until(
                lambda d: "home" in d.current_url or d.find_elements(By.XPATH, "//*[@data-sigil='m-feed-at-top']")
            )
            
            Logger.success("Direct Login Successful!")
            return True
            
        except Exception as e:
            Logger.error(f"Login failed: {e}")
            self.driver.save_screenshot("login_error.png")
            return False

    def post_comment(self, post_id, comment_text):
        """Navigates to a post and leaves a comment."""
        try:
            Logger.info(f"Accessing post ID: {post_id}")
            self.driver.get(f"https://m.facebook.com/{post_id}")
            
            # Find comment box
            comment_box = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.NAME, "comment_text"))
            )
            
            # Human-like typing
            time.sleep(random.uniform(2, 4))
            for char in comment_text:
                comment_box.send_keys(char)
                time.sleep(random.uniform(0.05, 0.2))
            
            # Find and click submit button
            submit_btn = self.driver.find_element(By.XPATH, "//button[@value='Post']")
            submit_btn.click()
            
            Logger.success(f"Comment posted: '{comment_text[:15]}...'")
            return True
            
        except Exception as e:
            Logger.error(f"Failed to post comment: {e}")
            return False

    def close(self):
        self.driver.quit()
