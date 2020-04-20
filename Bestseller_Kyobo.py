import requests
from urllib.request import urlopen #베스트셀러페이지에서 책 상세 페이지 URL 열기 위해
from bs4 import BeautifulSoup
import csv

#교보문고 주간 베스트셀러 1~20위 크롤링

class BookScraper :

    def __init__(self) : 
        
        self.url = "http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf"
    
    def gethtml(self) : #교보문고 베스트셀러 URL(self.url)의 정보 받아오기
        
        res = requests.get(self.url)

        if res.status_code != 200 :
            print("bad request", res.status_code)

        html = res.text
        soup = BeautifulSoup(html, "html.parser")

        return soup
    
    def getContent(self, soup) :  #베스트셀러 정보 받아오기 --> 제목, 저자, 가격(정가, 세일가)
        
        soup = self.gethtml() #베스트셀러 목록의 URL

        book_page_urls = [] #베스트셀러 목록에 있는 책들의 url을 담는 리스트
        for cover in soup.find_all('div', {'class':'detail'}): #책들의 Url만 뽑아서 리스트에 담기
            link = cover.select('a')[0].get('href')
            book_page_urls.append(link)

        order = [] #순위 --> 긁어오는 건 아니고, 아래 반복문에서 idx를 담아둠 --> idx가 url리스트들을 돌면서 0부터 순서 매기기 시작
        title = []
        author = []
        oprice = [] #정가
        sprice = [] #세일가

        for idx, book_page_url in enumerate(book_page_urls): #책들이 순위별로 있고, 순서대로 저장해야 하기 때문에 enumerate()를 사용하여 순서(idx), 책 정보 둘 다 저장
            html = urlopen(book_page_url) #책 상세설명 페이지 열고
            bstobj = BeautifulSoup(html, "html.parser") #정보 받아와서 bstobj에 저장
            title.append(bstobj.find('meta', {'property':'rb:itemName'}).get('content')) #bstobj의 메타데이터에서 'property':'rb:itemName'에 해당하는 내용(제목)을 get('content')로 받아오고, title 리스트에 저장
            author.append(bstobj.select('span.name a')[0].text) #저자 같은 경우는 따로 항목으로 없었기 때문에 span 안에 text 내용 받아오기
            oprice.append(bstobj.find('meta', {'property':'rb:originalPrice'}).get('content')) #title과 동일
            sprice.append(bstobj.find('meta', {'property':'rb:salePrice'}).get('content')) #title과 동일
            order.append(idx) #순서 저장  

        self.writeCSV(order, title, author, oprice, sprice)
        
    def writeCSV(self, order, title, author, oprice, sprice) : #CSV
        file = open('Bestseller_Kyobo.csv','a', newline='')
        wr = csv.writer(file)

        for i in range(len(title)) : 
            wr.writerow([order[i]+1, title[i], author[i], oprice[i], sprice[i]])
        
        file.close()

    def scrap(self) :
        file = open('Bestseller_Kyobo.csv','w', newline='')
        
        wr = csv.writer(file)
        wr.writerow(["순위", "책 제목", "저자", "정가", "세일가"])
        file.close()

        self.getContent(self)

if __name__ == "__main__":
    scraper = BookScraper()
    scraper.scrap()

