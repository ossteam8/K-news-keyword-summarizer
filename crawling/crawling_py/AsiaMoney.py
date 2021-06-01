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
from .categoryparser import Parse_category
from urllib.request import Request, urlopen

class AsiaMoney_crawling:
    #type = 1: 카테고리만 입력

    def __init__(self): 

        self.categories = ['정치','경제','사회']
        self.article_url = ""
        self.urls = []
        self.article_info = {"title":"","contents":"","url":"","category":""}  # 각 기사의 정보들
        self.articles = [] # 각 기사들의 정보들을 담을 리스트
        self.check_valid = True # 검색했을때 나오는 데이터가 나오는지 안나오는지를 비교
        self.num_article = 0
        self.choose_category=1
    # 1일전 이전의 몇시간전의 데이터만 가져온다
    def one_day_crawling(self, text_time):
        if '일' in text_time:
            return False
        return True

    def crawling(self):
        News_end = False
        while(not News_end):
            first_num = True
            
            try:
                req = Request(self.article_url,headers={'User-Agent': 'Mozilla/5.0'})
            
                with urlopen(req) as response:

                    html = response.read()
                    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')

                    #기사의 url들을 파싱하는 부분


                    article_list = soup.find("div",{"class":"content"})
                    #article_list = article_list.find("div",{"class":"section-list-area"})# 안된다면 이부분을 넣자


                    try:
                        first_article = article_list.find("div",{"class":"list_type"})
                        article_list = article_list.find_all("div",{"class":"listsm_type"})

                    except:
                        self.check_valid=False
                        print("리스트 읽어오기 실패")
                        return    

                    try:
                        #print(article_list[-1])

                        for article in article_list:
                            if(first_num):
                                f_article = first_article.find("a")
                                f_time = first_article.find("span",{"class":"txt_time"}).string
                                if(not self.one_day_crawling(f_time)):
                                    return
                                link = 'https:'+ f_article['href']
                                self.urls.append(link)

                            article_time = article.find("span",{"class":"txt_time"}).string
                            if(not self.one_day_crawling(article_time)):
                                    return
                            article = article.find("a")
                            link = 'https:'+ article['href']

                            self.urls.append(link)
                            #print(link)
                    except:
                        print("url 찾기 실패")
                        return

                    #try:
                    next_url = ""

                    pages = soup.find("div",{"class":"content"})
                    #pages = pages.find("span",{"class":"inner_paging"})
                    #print(pages)
                    try:
                        current_page = pages.find("span",{"class":"link_page"}).string# 현재 페이지 찾음
    
                        #print(current_page)
                        next_button = pages.find("a",{"class":"btn_next"})
    
    
                        pages = pages.find_all("a",{"class":"link_page"})
                    
                        for page in pages:

                            if(int(current_page)<int(page.string)):
                                next_url = page.string
                                break
                        if(next_url!=""):
                            pass
                        else: #다음 화살표 누르기
                            next_url = str(int(current_page)+1)
                        if(not News_end):
                            if(self.choose_category==1):
                                self.article_url = "https://www.asiae.co.kr/list/politics-all/"+next_url
                            elif(self.choose_category==2):
                                self.article_url="https://www.asiae.co.kr/list/economy-all/"+next_url
                            else:
                                self.article_url = "https://www.asiae.co.kr/list/society-all/"+next_url

                    except:
                        print("페이지 이동 실패")
                        return
            except:
                print('접속오류')
                return




    def category_crawling(self, choose_category):
        #동아일보는 url에 날짜를 넣으면 그 날짜만 가져온다

        
        if choose_category==1: #정치
            self.article_url = "https://www.asiae.co.kr/list/politics-all"
            self.choose_category = 1
        elif choose_category==2: # 경제
            self.article_url="https://www.asiae.co.kr/list/economy-all"
            self.choose_category = 2
        else: #사회
            self.article_url = "https://www.asiae.co.kr/list/society-all"
            self.choose_category = 3
        self.crawling()
        

    def read_article_contents(self,url):
        try:
            req = Request(url,headers={'User-Agent': 'Mozilla/5.0'})
        
            with urlopen(req) as response:
                html = response.read()
                soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
                article_contents = soup.find("div",{"class":"article_view"})
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

            category = self.categories[self.choose_category-1]

            g = Goose({'stopwords_class':StopWordsKorean})
            article = g.extract(url=url)
            title = article.title
            #print(title)
            contents = self.read_article_contents(url)
            if contents == "":
                continue
            #print(contents)
            self.article_info["category"] = category
            self.article_info["contents"] = contents
            self.article_info["title"] = title
            self.article_info["url"] = url
            self.articles.append(self.article_info)
            self.num_article+=1

        return self.articles    
        

if __name__ == "__main__":

    # 단순 카테고리만 할시에는 jungang_crawling(1)이것으로 초기화를하고,
    # category_crawling( 카테고리 번호 )에서 카테고리 번호를 넣어준다(외부에서 받아올 예정)
    # 그리고 그 번호를 get_news에다가도 넣어준다

    A = AsiaMoney_crawling()
    A.category_crawling(1)
    ll = A.get_news()

 