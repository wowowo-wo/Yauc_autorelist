from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pickle
import os

USER_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chrome_profile")
COOKIE_FILE = "yahoo_cookies.pkl"
YAHOO_AUCTIONS_URL = "https://auctions.yahoo.co.jp/"
CLOSED_AUCTIONS_URL = "https://auctions.yahoo.co.jp/closeduser/jp/show/mystatus?select=closed&hasWinner=0"
RELIST_BUTTON_XPATH = "//a[img[@alt='再出品']]"
SUBMIT_FORM_BUTTON_ID = "submit_form_btn"
RELIST_CONFIRM_XPATH = "//span[contains(@class, 'u-displayBlock') and contains(text(), '出品する')]"

def load_cookies(driver, cookie_file):
    try:
        with open(cookie_file, "rb") as f:
            cookies = pickle.load(f)
        for cookie in cookies:
            if 'domain' in cookie and not cookie['domain'].startswith('.'):
                cookie['domain'] = '.' + cookie['domain']
            driver.add_cookie(cookie)
    except Exception as e:
        print(f"Error:{e}")

def remove_all_modals(driver):
    driver.execute_script("""
        const selectors = [
            "div[class*='Modal']",
            "div[class*='modal']",
            "div[class*='Overlay']",
            "div[class*='overlay']",
            "div[class*='popup']",
            "div#modal",
            "div.PayPayMaturiModal__footer"
        ];

        selectors.forEach(function(sel) {
            document.querySelectorAll(sel).forEach(el => {
                if (el) {
                    el.style.display = 'none';
                    el.style.visibility = 'hidden';
                    el.style.zIndex = '-9999';
                    document.body.style.overflow = 'auto';
                }
            });
        });
    """)
    time.sleep(0.5)

def click_submit_form_btn(driver, timeout=15):
    wait = WebDriverWait(driver, timeout)
    try:
        driver.execute_script("if (typeof Y2SSubmit !== 'undefined' && Y2SSubmit.validation) { Y2SSubmit.validation.validationCheck = () => true; }")
        btn = wait.until(EC.presence_of_element_located((By.ID, SUBMIT_FORM_BUTTON_ID)))
        driver.execute_script("arguments[0].disabled = false;", btn)
        btn = wait.until(EC.element_to_be_clickable((By.ID, SUBMIT_FORM_BUTTON_ID)))
        driver.execute_script("arguments[0].click();", btn)
    except Exception as e:
        print(f"Error:{e}")
        raise


if __name__ == "__main__":

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument(f"--user-data-dir={USER_DATA_DIR}") 
    options.add_argument('--ignore-certificate-errors')

    os.makedirs(USER_DATA_DIR, exist_ok=True)

    driver = None
    try:
        from chromedriver_py import binary_path
        driver = webdriver.Chrome(service=Service(binary_path), options=options)
        wait = WebDriverWait(driver, 20)

        print(f"access the closed autions page: {CLOSED_AUCTIONS_URL}")
        driver.get(CLOSED_AUCTIONS_URL)
        time.sleep(1)

        relisted_count = 0
        failed_relist_count = 0

        while True:
            buttons = driver.find_elements(By.XPATH, RELIST_BUTTON_XPATH)

            if not buttons:
                print("all items are relisted or there is no item to relist")
                break

            first_button = buttons[0]

            try:
                print(f"Step:{relisted_count + failed_relist_count + 1}")
                driver.execute_script("arguments[0].scrollIntoView(true);", first_button)
                time.sleep(0.5)

                clickable_relist_button = wait.until(EC.element_to_be_clickable((By.XPATH, RELIST_BUTTON_XPATH)))
                driver.execute_script("arguments[0].click();", clickable_relist_button)

                time.sleep(2)
                remove_all_modals(driver)
                click_submit_form_btn(driver)

                wait.until(EC.element_to_be_clickable((By.XPATH, RELIST_CONFIRM_XPATH))).click()
                print("relisted")
                relisted_count += 1
                time.sleep(3)

            except TimeoutException as e:
                print(f"Timeout to relist: {e}. go next srep")
                failed_relist_count += 1
            except Exception as e:
                print(f"Error: {e}. go to next step")
                failed_relist_count += 1
            finally:
                driver.get(CLOSED_AUCTIONS_URL)
                time.sleep(5)


    except Exception as final_e:
        print(f"\nError: {final_e}")
    finally:
        if driver:
            print("close chrome")
            driver.quit()
        print(f"result:")
        print(f"{relisted_count} items were relisted.")
        print(f"{failed_relist_count} attempts were filed.")