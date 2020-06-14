#!/usr/bin/env python3
""" developer by Dojopy """
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


class BotWhatsapp:
    def __init__(self):
        self.path_driver = '/usr/local/bin/chromedriver'
        self.base_url = 'https://web.whatsapp.com/'
        self.timeout = 30
        self.set_paths()

    def set_paths(self):
        self.base_input = '._3FRCZ'
        self.firs_contact = '//*[@id="pane-side"]/div[1]/div/div/div[1]'
        self.base_sent = '/html/body/div/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]'

    def start_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-extensions')
        options.add_argument('--profile-directory=Default')
        options.add_argument("--disable-plugins-discovery")
        options.add_argument("--user-data-dir=/home/henry/app-data-browser/")   # setear ruta local path

        self.browser = webdriver.Chrome(executable_path=self.path_driver,
                                        chrome_options=options)
        self.browser.get(self.base_url)
        try:
            WebDriverWait(self.browser, self.timeout).until(
                EC.presence_of_element_located(
                (By.CSS_SELECTOR, self.base_input)))
            return True
        except Exception as e:
            print(e)
            return False

    def send_message_to_contact(self, contact, message):
        start = self.start_browser()
        if not start:
            return False

        user_search = self.search_user_or_group(contact)
        if not (user_search or contact or message):
            return False
        message = message.strip()
        try:
            send_msg = WebDriverWait(self.browser, self.timeout).until(
                EC.presence_of_element_located(
                (By.XPATH, self.base_sent)))
        except Exception as e:
            print(e)
            return
        messages = message.split("\n")
        for msg in messages:
            send_msg.send_keys(msg)
            send_msg.send_keys(Keys.SHIFT + Keys.ENTER)
            sleep(1)
        send_msg.send_keys(Keys.ENTER)
        print('mensaje enviado.')
        return True

    def search_user_or_group(self, contact):
        search = self.browser.find_element_by_css_selector(self.base_input)
        search.clear()
        search.send_keys(contact)
        try:
            vali_ = WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located(
                (By.XPATH, self.firs_contact)))
            if vali_.is_displayed():
                search.send_keys(Keys.ENTER)
                return True
        except Exception as e:
            print(e)
            print('No se encontro contacto.')
        return False


obj = BotWhatsapp()
obj.send_message_to_contact('935489552', 'Hola Bro!!')
