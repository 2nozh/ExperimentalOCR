import timeit
from functools import wraps
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import lackey
import easyocr
import time
from PIL import ImageGrab
from selenium.webdriver.common.by import By

GOOGLE_PATH="C:\\Users\\aseslavinskaya\\Desktop\\chrome.exe"
def getTextBox(resultSet,text):
    for [bbox,value,prob] in resultSet:
        if text in value:
            print("found",text,"in",value,"coord:",bbox)
            return bbox

def getAllText():
    reader = easyocr.Reader(['en','ru'])
    result = reader.readtext("screen.png")
    return result
def ocrTest_google():
    options = Options()
    #options.add_experimental_option('headless', 'True')
    browser = webdriver.Chrome(options)
    browser.get("https://www.google.com/")
    browser.maximize_window()
    browser.execute_script('alert("script")')
    time.sleep(1)
    browser.switch_to.alert.accept()
    search_bar = browser.find_element(By.CSS_SELECTOR,'textarea[title="Поиск"]')
    search_bar.send_keys("купить книги")
    search_bar.send_keys(Keys.ENTER)
    first_link = browser.find_element(By.CSS_SELECTOR,'#search a')
    first_link.click()
    snapshot = ImageGrab.grab()
    save_path = "screen.png"
    snapshot.save(save_path)
    result = getAllText()
    for (bbox, text, prob) in result:
        print(bbox, text, prob)
    box = getTextBox(result, "Поиск")
    print(box)
    match = lackey.Match(0.9, lackey.Location(10, 10), [box[0], [(box[1][0] - box[0][0]), (box[2][1] - box[0][1])]])
    match.highlight(5, "red")
    ActionChains(browser).move_by_offset(match.x,match.y).click().send_keys("учебник").perform()
    match.click()
    browser.execute_script('alert("script")')
    time.sleep(1)
    browser.switch_to.alert.accept()
    #lackey.type("учебник")
    #lackey.type(lackey.Key.ENTER)
    time.sleep(10)

"""
    
    
    
    print("start read", time.time())
    
    print("end read", time.time())
    print("start search and draw", time.time())
    for (bbox, text, prob) in result:
        print(bbox, text, prob)
    box= getTextBox(result,"ello")
    print(box)

    match = lackey.Match(0.9,lackey.Location(10,10),[box[0],[(box[1][0]-box[0][0]),(box[2][1]-box[0][1])]])
    match.highlight(5,"red")
    print("end search and draw", time.time())



"""

if __name__ == '__main__':
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get("https://www.google.com/")

    snapshot = ImageGrab.grab()
    save_path = "screen.png"
    snapshot.save(save_path)
    result = getAllText()
    for (bbox, text, prob) in result:
        print(bbox, text, prob)
    box = getTextBox(result, "повезёт")
    print(box)
    match = lackey.Match(0.9, lackey.Location(10, 10), [box[0], [(box[1][0] - box[0][0]), (box[2][1] - box[0][1])]])
    match.highlight(5, "red")
    search_bar = browser.find_element(By.CSS_SELECTOR,'textarea[title="Поиск"]')
    search_bar.click()
    time.sleep(2)
    ActionChains(browser).move_by_offset(200, 200).click().perform()
    time.sleep(2)
    ActionChains(browser).move_by_offset(match.x,match.y).click().perform()
    time.sleep(10)
    #print("x and y",match.x,match.y)
    #ocrTest_google()
