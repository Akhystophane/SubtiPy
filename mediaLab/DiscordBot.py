import random
import re
import unicodedata

import time
import urllib


from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from urllib.request import Request, urlopen
from PIL import Image
import os

def convert_and_delete_webp(image_path):
    # Vérifier si le fichier est un WebP
    if image_path.endswith('.webp'):
        # Ouvrir l'image WebP
        image = Image.open(image_path)

        # Définir le nom du fichier PNG
        png_path = image_path[:-5] + '.png'

        # Enregistrer l'image au format PNG
        image.save(png_path, 'PNG')
        print(f"Image convertie et enregistrée en tant que: {png_path}")

        # Supprimer le fichier WebP original
        os.remove(image_path)
        print(f"Fichier WebP supprimé: {image_path}")

    else:
        print("Le fichier spécifié n'est pas une image WebP.")

def get_cookie(driver, path):
    with open(path, 'w') as cookiesfile:
        json.dump(driver.get_cookies(), cookiesfile)

def load_cookie(driver, path):
    with open(path, 'r') as cookiesfile:
        cookies = json.load(cookiesfile)
    for cookie in cookies:
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(e)

def patterned(prompt: str) -> str:
    # 1. Normalisation Unicode pour enlever les accents
    prompt_normalized = unicodedata.normalize('NFD', prompt)
    prompt_without_accents = ''.join(
        char for char in prompt_normalized if unicodedata.category(char) != 'Mn'
    )

    # 2. Suppression de la ponctuation sauf les tirets
    prompt_without_punctuation = re.sub(r'[^\w\s-]', '', prompt_without_accents)

    # 3. Remplacement des espaces par des underscores et passage en minuscules,
    # mais en préservant la première lettre majuscule si elle existe
    if prompt_without_punctuation:
        first_char = prompt_without_punctuation[0]
        remaining = prompt_without_punctuation[1:].replace(" ", "_").lower()
        prompt_cleaned = first_char + remaining
    else:
        prompt_cleaned = ""

    # 4. Troncature de la chaîne à 40 caractères maximum
    if len(prompt_cleaned) > 40:
        words = prompt_cleaned[:40].split('_')

        # Si le dernier mot est incomplet, on l'ignore
        if len(words[-1]) < len(prompt_cleaned) - prompt_cleaned.rfind('_'):
            words.pop()

        pattern = '_'.join(words)
    else:
        pattern = prompt_cleaned

    return pattern

def load_bot(driver):
    driver.get("https://discord.com/channels/@me/1120828783230984293")
    # for _ in range(1):
    #     email_txtbox = WebDriverWait(driver, 20).until(
    #         EC.element_to_be_clickable((By.XPATH, "//*[@id='uid_7']")))
    #     email_txtbox.send_keys("emnl.busi@outlook.fr")
    #     password_txtbox = WebDriverWait(driver, 20).until(
    #         EC.element_to_be_clickable((By.XPATH, "//*[@id='uid_9']")))
    #     password_txtbox.send_keys("voVsic-medtek-7cyfva")
    #     time.sleep(1)
    #     WebDriverWait(driver, 20).until(
    #         EC.element_to_be_clickable((
    #             By.XPATH, "//*[@id='app-mount']/div[2]/div[1]/div[1]/div/div/div/div/form/div[2]/div/div[1]/div[2]/button[2]"))).click()
    #     time.sleep(3)
        # time.sleep(20)
    driver.get("https://discord.com/channels/@me/1120828783230984293")
    time.sleep(3)



def generate_img(driver, prompt, first, aspect_ratio):
    txt_box = WebDriverWait(driver, 50).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@role='textbox']"))
    )
    txt_box.send_keys("/imagine")
    if first:
        print('fiiirst')
        time.sleep(2)

    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='autocomplete-0']"))).click() #imagine button

    txt_box.send_keys(f'{prompt} --ar {aspect_ratio}')
    txt_box.send_keys(Keys.ENTER)

    pattern = patterned(prompt)
    print(pattern)

    WebDriverWait(driver, 200).until(
        EC.presence_of_element_located((
            By.XPATH, f"//a[contains(@data-safe-src, '{pattern}')]")))

    elements = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, "//*[contains(@id, 'message-accessories-')]")))
    id_pic = elements[-1].get_attribute('id')
    u_path = f"//*[@id='{id_pic}']/div[2]/div[1]/div/button[{random.randint(1,4)}]"
    time.sleep(1.5)
    print(u_path)
    U_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((
            By.XPATH, u_path)))
    U_button.click()
    number = 0
    while number < 2:
        number = len(WebDriverWait(driver, 200).until(
            EC.presence_of_all_elements_located((
                By.XPATH, f"//a[contains(@data-safe-src, '{pattern}')]"))))


    src = WebDriverWait(driver, 200).until(
        EC.presence_of_all_elements_located((
            By.XPATH, f"//a[contains(@data-safe-src, '{pattern}')]")))[1].get_attribute('data-safe-src')

    # Download image
    req = Request(url=src, headers={'User-Agent': 'Mozilla/6.0'})
    with urlopen(req) as response:
        webpage = response.read()
        file_path = f'/Users/emmanuellandau/Documents/MidjourneyBibli/{pattern}.webp'
        with open(file_path, 'wb') as file:
            file.write(webpage)

    convert_and_delete_webp(file_path)
    file_path = f'/Users/emmanuellandau/Documents/MidjourneyBibli/{pattern}.png'
    return file_path

# driver = webdriver.Chrome()
# load_bot(driver)
# generate_img(driver, "Two siblings sharing a taxi ride home, looking cheerful and content.", "/Users/emmanuellandau/Downloads")
# generate_img(driver, "A guest room in a house, prepared for a family member's visit.", "/Users/emmanuellandau/Downloads")