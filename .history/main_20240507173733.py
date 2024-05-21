from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_data(url)-> list:
    browser_options = ChromeOptions()
    browser_options.headless = True

    driver = Chrome(options=browser_options)
    driver.get(url)

    data = driver.page_source

    driver.quit()
    

    return data



def main():
    with open("credentials.json") as f:
        credentials = json.load(f)
    
    username = credentials["username"]
    password = credentials["password"]

    data = get_data("https://vav.unob.cz/requests/index")

    driver = Chrome()
    #driver.get("https://vav.unob.cz/auth/login")
    driver.get("https://vav.unob.cz/requests/index")

    #print("Username:", username)
    #print("Password:", password)

    # Získání elementů pro jméno a heslo
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")

    # Vyplnění přihlašovacích údajů
    username_field.send_keys(username)
    password_field.send_keys(password)

    # Odeslání formuláře
    password_field.submit()

 
    # Získání HTML obsahu stránky po přihlášení
    page_source = driver.page_source




    #with open("dataX.json", "w") as d:
    #    d.write(page_source)

    print (page_source)


if __name__ == '__main__':
    main()
