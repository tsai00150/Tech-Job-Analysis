from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json
import configparser
config= configparser.ConfigParser()
config.read('config.ini')
USERNAME = config['reuters']['username']
PASSWORD = config['reuters']['password']

def crawl_reuters(keyword, startpage, endpage, steps):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.set_window_size(1920,1080)
    time.sleep(10)
    url = "https://www.reuters.com/site-search/?query=layoff&section=technology&offset=0"
    driver.get(url)
    time.sleep(10)
    path = '//a[contains(@href,"https://www.reuters.com/account/sign-in/?redirect=https%3A%2F%2Fwww.reuters.com%2Fsite-search%2F%3Fquery%3Dlayoff%26section%3Dtechnology%26offset%3D0")]'
    driver.find_element(By.XPATH, path).click()
    time.sleep(10)  
    username = USERNAME
    password = PASSWORD
    uname = driver.find_element("name", "email")
    uname.send_keys(username)
    pword = driver.find_element("name", "password") 
    pword.send_keys(password)
    driver.find_element(By.XPATH, "//button[contains(@type, 'submit')]").click()
    time.sleep(10)
    data = []
    for offset in range(startpage, endpage, steps):
        url = "https://www.reuters.com/site-search/?query={keyword}&section=business&offset={offset}"\
              .format(keyword=keyword, offset=str(offset))
        driver.get(url)
        time.sleep(5)
        urlist = driver.find_elements(By.XPATH, '//a[contains(@data-testid,"Heading")]')
        links = []
        for url in urlist:    
            links.append(url.get_attribute('href')) 
            time.sleep(2)
        for link in links:
            info = {}
            driver.get(link)
           
            info['link'] = link
            info['title'] = driver.find_element(By.XPATH, '//h1[contains(@data-testid,"Heading")]').text
            info['paragraph'] = driver.find_element(By.XPATH, '//div[contains(@class,"article-body__content__17Yit")]').text
            date_info = driver.find_element(By.XPATH,'//time[contains(@data-testid,"Text")]').text
            try:
                date = date_info.split("read")[1].split(':')[0]
                month = date.split(',')[0]
                year = date.split(',')[1].strip(' ')[:4]
                info['date'] = month + ' ' + year
            except:
                info['date'] = "Janurary 1 2000"
            data.append(info)

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    driver.close()