from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import os
import time
import csv

#path = os.getcwd() + "./chromedriver.exe" #실제로 할 때는 크롬 드라이버가 가장 처음에 다운로드됐던 경로로 설정해야 실행됨 

driver = webdriver.Chrome("C:\chromedriver_win32\chromedriver.exe")

file = open('Exhibitions.csv', 'a', newline='')
csvwriter =  csv.writer(file)
csvwriter.writerow(["No.", "Name", "Date", "Place", "Location"])
#csvwriter.writerow(["No.", "Name", "Date", "Place"])

try :
    driver.get("https://www.naver.com/")
    time.sleep(1)

    searchkywd = "전시회"
  
    element = driver.find_element_by_class_name("input_text")
    element.send_keys(searchkywd)
    driver.find_element_by_class_name("btn_submit").click()
    driver.find_element_by_xpath('//*[@id="main_pack"]/div[2]/div/div[2]/div/div[1]/div[4]/div/ul/li[2]').click()
    #pages = driver.find_element_by_xpath('//*[@id="main_pack"]/div[2]/div/div[2]/div/div[1]/div[6]/span/text()')
    
    driver.implicitly_wait(10)

    html = driver.page_source
    bs = BeautifulSoup(html, "html.parser")
    
    pages = bs.find("span", class_ = "info _navi_tpl").text
    pages=pages[2:]
    print(pages) #자꾸 전체 페이지가 나옴,,, 왜 서울에만 해당하는 페이지 안나오는건데,,,, 

    pages = int(pages)

    exhbt = []
    date = []
    place = []
    Location = []

    for i in range(25):
        time.sleep(1)
        
        html = driver.page_source
        bs = BeautifulSoup(html, "html.parser")

        #if (bs.find("div", class_ = "list_info _list_base") == None):
        #    break # 더 이상 안 나오면 중지시키는 거 --> 실패

        #else:   
     
        cont_1 = bs.find("div", class_ = "main_pack").find_all("dl", class_ = "item_list")
        for c in cont_1 :
            print(c.find("dd", class_ = "tit").find("a").text)
            print(c.find("dd", class_ = "period").text)
            print(c.find_all("dd")[2].text)
            exhbt.append(c.find("dd", class_ = "tit").find("a").text)
            date.append(c.find("dd", class_ = "period").text)
            place.append(c.find_all("dd")[2].text)
        
        cont_2 = bs.find("div", class_ = "main_pack").find_all("div", class_ = "btn_box")
        for c2 in cont_2 :
            if (c2.find("a", class_= "map") == None):
                print("No Map")
                Location.append("No Map")
            else:
                print(c2.find("a", class_= "map").attrs["href"])
                Location.append(c2.find("a", class_= "map").attrs["href"])

        #전시회포스터는,, 나중에!^^
        #cont_3 = bs.find("div", class_ = "main_pack").find_all("div", _class = "thumb")
        #for c3 in cont_3:
        #    print(c3.find("img")["src"].text)
            
        driver.find_element_by_xpath('//*[@id="main_pack"]/div[2]/div/div[2]/div/div[1]/div[6]/a[2]').click()

finally:
    time.sleep(3)
    driver.quit()

file = open('Exhibitions.csv', 'a', newline='')
csvwriter =  csv.writer(file)

for i in range(len(exhbt)):
    csvwriter.writerow([str(i+1), exhbt[i], date[i], place[i], Location[i]])

file.close()