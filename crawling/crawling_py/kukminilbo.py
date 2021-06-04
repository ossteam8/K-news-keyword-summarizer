import re
import time
import sys
from goose3 import Goose
import pickle
from goose3.text import StopWordsKorean
import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
from datetime import datetime
from dateutil.relativedelta import relativedelta
# from .categoryparser import Parse_category
from urllib.request import Request, urlopen
class Kukmin_crawling:
    #type = 1: 카테고리만 입력

    def __init__(self): 

        self.categories = ['정치','경제','사회']
        self.article_url = ""
        self.urls = []
        # self.article_info = {"title":"","contents":"","url":"","category":""}  # 각 기사의 정보들
        self.articles = [] # 각 기사들의 정보들을 담을 리스트
        self.check_valid = True # 검색했을때 나오는 데이터가 나오는지 안나오는지를 비교
        self.num_article = 0
        self.choose_category=1
    def get_date(self, now):
        now = str(now)
        year = now[:4]
        month = now[5:7]
        day = now[8:10]
        return year+month+day

    def crawling(self):
        News_end = False

        while(not News_end):
            try:
                with urllib.request.urlopen(self.article_url) as response:

                    html = response.read()
                    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')

                    #기사의 url들을 파싱하는 부분


                    article_list = soup.find("div",{"id":"container"})
                    #article_list = article_list.find("div",{"id":"contents"})# 안된다면 이부분을 넣자
                    article_list = article_list.find("div",{"class":"nws_list"})


                    try:
                        article_list = article_list.find_all("div",{"class":"nws"})

                    except:
                        self.check_valid=False
                        print("리스트 읽어오기 실패")
                        return    

                    try:
                        for article in article_list:
                            link =  article.find("a")
                            link = "http://news.kmib.co.kr/article/"+link['href']
                            self.urls.append(link)
                            
                    except:
                        print("url 찾기 실패")
                        return

                    #try:
                    next_url = ""

                    pages = soup.find("div",{"id":"container"})
                    pages = pages.find("div",{"class":"paging"})
                    current_page = pages.find("strong").string  # 현재 페이지 찾음

                    next_button = pages.find("a",{"class":"next"})

                    #next_button = pages.find("a",{"class":"btn_next"})
                    pages = pages.find_all("a")
                    try:
                        #print(pages)
                        for page in pages:

                            if page.string!=None:

                                if(int(current_page)<int(page.string)):
                                    next_url = page['href']

                                    break
                        if(next_url!=""):
                            pass
                        else: #다음 화살표 누르기
                            try:
                                next_url = next_button['href']
                            except:
                                News_end = True
                        if(not News_end):
                            self.article_url = "http://news.kmib.co.kr/article/"+next_url
                            
                    except:
                        print("페이지 이동 실패")
                        return
            except:
                return




    def category_crawling(self, choose_category):
        #동아일보는 url에 날짜를 넣으면 그 날짜만 가져온다

        now = datetime.now()-relativedelta(days=1) # 실제엔 relative(days=1)을 빼자
        now = self.get_date(now)
        if choose_category==1: #정치
            self.article_url = "http://news.kmib.co.kr/article/list.asp?sid1=pol&sid2=&sdate="+now
            self.choose_category = 1
        elif choose_category==2: # 경제
            self.article_url="http://news.kmib.co.kr/article/list.asp?sid1=eco&sid2=&sdate="+now
            self.choose_category = 2
        else: #사회
            self.article_url = "http://news.kmib.co.kr/article/list.asp?sid1=soc&sid2=&sdate="+now
            self.choose_category = 3
        self.crawling()
        

    def read_article_contents(self,url):
        try:
            with urllib.request.urlopen(url) as response:
                html = response.read()
                soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
                article_contents = soup.find("div",{"id":"articleBody"})
                text = ""
                try:
                    text = text + ' '+ article_contents.get_text(' ', strip=True)
                except:
                    print("error" , url)

                return text
        except:
            return ""
    



    def get_news(self):# 실제로 url에 들어가 기사들을 읽어온다 , 첫번째 카테고리만으로 검색했을때 데이터를 가져와준다
        #categories 는 1,2,3숫자를 받는다(여러개 가능)
        print('기사 추출 시작')
        for url in self.urls:
            article_info = {"title":"","contents":"","url":"","category":""}
            category = self.categories[self.choose_category-1]
            try:
                g = Goose({'stopwords_class':StopWordsKorean})
                article = g.extract(url=url)
                title = article.title
            except:
                continue
            #print(title)
            contents = self.read_article_contents(url)

            article_info["category"] = category
            article_info["contents"] = contents
            article_info["title"] = title
            article_info["url"] = url
            self.articles.append(article_info)
            self.num_article+=1

        return self.articles    
        

if __name__ == "__main__":

    # 단순 카테고리만 할시에는 jungang_crawling(1)이것으로 초기화를하고,
    # category_crawling( 카테고리 번호 )에서 카테고리 번호를 넣어준다(외부에서 받아올 예정)
    # 그리고 그 번호를 get_news에다가도 넣어준다

    A = Kukmin_crawling()
    A.category_crawling(3)
    ll = A.get_news()

 