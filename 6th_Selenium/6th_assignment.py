from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
import time

#path = os.getcwd() + "./chromedriver.exe" #실제로 할 때는 크롬 드라이버가 가장 처음에 다운로드됐던 경로로 설정해야 실행됨 

driver = webdriver.Chrome("C:\chromedriver_win32\chromedriver.exe")

try :
    driver.get("https://www.naver.com/")
    time.sleep(1)

    searchkywd = "전시회"
  
    element = driver.find_element_by_class_name("input_text")
    element.send_keys(searchkywd)
    driver.find_element_by_class_name("btn_submit").click()

    for i in range(10) :
        time.sleep(1)
        
        html = driver.page_source
        bs = BeautifulSoup(html, "html.parser")

        cont = bs.find("div", class_ = "main_pack").find_all("dl", class_ = "item_list")

        print("\npage: ", i+1)
       
        for c in cont :
            print(c.find("dd", class_ = "tit").find("a").text)
        
        driver.find_element_by_xpath('//*[@id="main_pack"]/div[2]/div/div[2]/div/div[1]/div[6]/a[2]').click()

    

finally :
    time.sleep(3)
    driver.quit()