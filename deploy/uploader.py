import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

OUTPUT_DIR = "../products"
CONFIG_PATH = "../config/settings.json"
GUMROAD_URL = "https://gumroad.com/products/new"

def find_latest_product_dir():
    dirs = [os.path.join(OUTPUT_DIR, d) for d in os.listdir(OUTPUT_DIR)]
    dirs = [d for d in dirs if os.path.isdir(d)]
    return max(dirs, key=os.path.getmtime)

def load_config():
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def upload_to_gumroad():
    config = load_config()
    creds = config["gumroad"]
    author = config["author"]

    folder = find_latest_product_dir()
    with open(os.path.join(folder, "meta.json")) as f:
        meta = json.load(f)

    chrome_opts = Options()
    chrome_opts.add_argument("--headless")
    chrome_opts.add_argument("--window-size=1920x1080")

    driver = webdriver.Chrome(options=chrome_opts)
    wait = WebDriverWait(driver, 20)

    try:
        # Login
        driver.get("https://gumroad.com/login")
        wait.until(EC.presence_of_element_located((By.NAME, "user[email]")))
        driver.find_element(By.NAME, "user[email]").send_keys(creds["email"])
        driver.find_element(By.NAME, "user[password]").send_keys(creds["password"])
        driver.find_element(By.NAME, "commit").click()

        # Go to new product page
        wait.until(EC.url_contains("/dashboard"))
        driver.get(GUMROAD_URL)

        # Fill product form
        wait.until(EC.presence_of_element_located((By.NAME, "product[name]")))
        driver.find_element(By.NAME, "product[name]").send_keys(meta["title"])
        driver.find_element(By.NAME, "product[price]").clear()
        driver.find_element(By.NAME, "product[price]").send_keys(author["default_price"])

        desc_field = driver.find_element(By.NAME, "product[description]")
        desc_field.send_keys(Keys.CONTROL + "a")
        desc_field.send_keys(Keys.BACKSPACE)
        desc_field.send_keys(meta["description"])

        # Upload files
        cover_input = driver.find_element(By.ID, "product_preview")
        cover_input.send_keys(os.path.abspath(os.path.join(folder, "cover.png")))

        file_input = driver.find_element(By.NAME, "product[file_url]")
        file_input.send_keys(os.path.abspath(os.path.join(folder, "ebook.pdf")))

        # Save
        time.sleep(4)
        save_button = driver.find_element(By.XPATH, "//button[contains(text(),'Publish')]")
        driver.execute_script("arguments[0].click();", save_button)

        print("✅ Ebook uploaded successfully!")

    except Exception as e:
        print(f"🚨 Error uploading to Gumroad: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    upload_to_gumroad()
