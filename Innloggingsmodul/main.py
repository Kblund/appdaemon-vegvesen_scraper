
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.options import Options
from time import sleep
from base64 import b64encode as enc
import pyperclip as pc





driver_dir = "/config/custom_components/vegvesen"
BaseURL = "https://oidc-login.atlas.vegvesen.no/idporten/login?returnUrl=https://www.vegvesen.no/dinside/oversikt/"
PersonNummer ="06090397484"
mobilnr = "91910850"
cookieFile = "/usr/share/hassio/homeassistant/appdaemon/apps/vegvesen-scraper/const/cookie"

def document_ready(css):
    WebDriverWait(driver, timeout=10).until(lambda x: x.find_element(By.CSS_SELECTOR,value= css))
    sleep(0.1)
    return

def cookieFormat(string):
    newStr = enc(
		bytes(f"SVVSecurityTokenIdporten={string};",'UTF-8')
	)
    
    with open(cookieFile,"wb") as f:
        f.write(newStr)
    return newStr

def getSessionToken():
    cookies = driver.get_cookies()
    for cookie in cookies:
        if "SVVSecurityTokenIdporten" in cookie["name"]:
          return cookie["value"]


chromeOptions = Options()
chromeOptions.headless = True
driver = webdriver.Chrome(options=chromeOptions)
driver.get(BaseURL)
WebDriverWait(driver, timeout=10).until(lambda x: x.find_element(By.CLASS_NAME, "ln-List_Element_Logo"))
BankID_knapp  = driver.find_element(by=By.CSS_SELECTOR,value='.ln-List_Element_Logo img[alt="BankID"]')
BankID_knapp.click()
WebDriverWait(driver, timeout=10).until(lambda x: x.find_element(By.CLASS_NAME, "T_DG8_4QIEDdPkqVFDVm"))

InputFelt =  driver.find_element(by=By.CSS_SELECTOR,value='input')
InputFelt.click()
InputFelt.clear() ; InputFelt.send_keys(PersonNummer)
InputFelt.submit()
WebDriverWait(driver, timeout=10).until(lambda x: x.find_element(By.CLASS_NAME, "button"))
sleep(2)
Knapper = driver.find_elements(by=By.XPATH,value="//button")

BankID_knapp_Mobil = ''
for i in Knapper:
    if "mobil" in str(i.text):
        print(i.text)
        BankID_knapp_Mobil = i
        break
sleep(1) ; BankID_knapp_Mobil.click()
document_ready("input")

mobilnr_felt = driver.find_element(By.CSS_SELECTOR,value="input")
mobilnr_felt.send_keys(mobilnr)
mobilnr_felt.submit()
WebDriverWait(driver, timeout=200).until(lambda x: x.find_element(By.CSS_SELECTOR,value=".link-card__bg.ikon-dinekjoretoy"))

encodedcookie = cookieFormat(getSessionToken())
print(encodedcookie)

driver.quit()
