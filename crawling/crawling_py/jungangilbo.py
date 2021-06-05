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

from urllib.request import Request, urlopen
class Jungang_crawling:
    #type = 1: 카테고리만 입력
    #type = 2: 검색어만 입력
    #type=3 : 카테고리 + 검색어
    def __init__(self): 
        self.categories = ['정치','경제','사회']
        self.article_url = ""
        self.urls = []
        # self.article_info = {"title":"","contents":"","url":"","category":""}  # 각 기사의 정보들
        self.choose_category=0
        self.articles = [] # 각 기사들의 정보들을 담을 리스트
        self.check_valid = True # 검색했을때 나오는 데이터가 나오는지 안나오는지를 비교
        self.num_article = 0
    def get_date(self, now):
        now = str(now)
        year = now[:4]
        month = now[5:7]
        day = now[8:10]
        return year+month+day

    def crawling(self):
        News_end = False
        now = datetime.now()
        before_one_week = now-relativedelta(days=1) # 여기서 days값이 몇일전을의미 테스트용으론 1이 적당
        before_one_week =  self.get_date(before_one_week) # 일주 전을 의미
        while(not News_end):
            try:
                req = Request(self.article_url,headers={'User-Agent': 'Mozilla/5.0'})
            
                with urlopen(req) as response:
                
                    html = response.read()
                    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')

                    try:
                        article_list = soup.find("div",{"class":"list_basic"})

                        article_list = article_list.find("ul")

                        article_list = article_list.find_all("li")
                    
                        for article in article_list:
                            #if(self.type==1): # 카테고리만 일때만 이것을 시행
                            article_time = article.find("span",{"class":"byline"}).string # 날짜를 읽어옴
                            article_time = self.get_date(article_time)
                            if(int(article_time)>int(before_one_week)):
                                continue
                            if(int(article_time)<int(before_one_week)): # 일주 전까지의 자료만 필요하다
                                return 

                            link = article.find("a")
                            self.urls.append(link['href'])
                    except:
                        print("error1")
                        return

                    #try:
                    next_url = ""
                    try:
                        pages = soup.find("div",{"class":"paging_comm"})

                        current_page = pages.find("em")
                        current_page = current_page.string # 현재 페이지 번호

                        next_button = pages.find_all("span",{"class":"icon"})
                        next_button = next_button[1]
                        #next_button = pages.find("a",{"class":"btn_next"})
                        pages = pages.find_all("a",{"class":"link_page"})

                        #print(pages)
                        for page in pages:
                            #print(next_button)
                            if(int(current_page)<=int(page.string)):
                                next_url = page['href']
                                break
                        if(next_url!=""):
                            pass
                        elif next_button.string=="다음페이지":
                            next_url = next_button.parent['href']
                        elif next_button.string == "다음페이지 없음":
                            News_end = True
                        if(not News_end):
                            self.article_url = "https://news.joins.com" + next_url
                    except:
                        print('페이징 실패')
                        return


            except:
                print('사이트 접속 오류')
                return


    def category_crawling(self, choose_category):
        if choose_category==1: #정치
            self.article_url = "https://news.joins.com/politics?cloc=joongang-home-gnb2"
            self.choose_category = 1
        elif choose_category==2: # 경제
            self.article_url="https://news.joins.com/money?cloc=joongang-home-gnb3"
            self.choose_category = 2
        else: #사회
            self.article_url = "https://news.joins.com/society?cloc=joongang-home-gnb4"
            self.choose_category = 3
        self.crawling()
        


    # 검색했을때의 크롤링 + 검색,카테고리 크롤링 => 이젠 무쓸모
    def searching_category(self,searching):
        title = urllib.parse.quote(searching)
        self.article_url = "https://news.joins.com/Search/JoongangNews?Keyword="+title+"&SortType=New&SearchCategoryType=JoongangNews&PeriodType=OneWeek&ScopeType=All&ImageType=All&JplusType=All&BlogType=All&ImageSearchType=Image&TotalCount=0&StartCount=0&IsChosung=False&IssueCategoryType=All&IsDuplicate=True&Page=1&PageSize=10&IsNeedTotalCount=True"
        
        self.crawling()
        
    # def searching_category_crawling(self,searching,category):
        
    #     title = urllib.parse.quote(searching)
    #     self.article_url = "https://news.joins.com/Search/JoongangNews?Keyword="+title+"&SortType=New&SearchCategoryType=JoongangNews&PeriodType=OneWeek&ScopeType=All&ImageType=All&JplusType=All&BlogType=All&ImageSearchType=Image&TotalCount=0&StartCount=0&IsChosung=False&IssueCategoryType=All&IsDuplicate=True&Page=1&PageSize=10&IsNeedTotalCount=True"
    #     print(self.article_url)
    #     self.crawling()
    


    def read_article_contents(self,url):
        try:
            req = Request(url,headers={'User-Agent': 'Mozilla/5.0'})
        
            with urlopen(req) as response:
                html = response.read()
                soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
                article_contents = soup.find("div",{"id":"article_body"})
                text = ""
                try:
                    text = text + ' '+ article_contents.get_text(' ', strip=True)
                except:
                    print("error" , url)

                return text
        except:
            return ""
    



    def get_news(self,*categories):# 실제로 url에 들어가 기사들을 읽어온다 , 첫번째 카테고리만으로 검색했을때 데이터를 가져와준다
        #categories 는 1,2,3숫자를 받는다(여러개 가능)
        print('기사 추출 시작')
        articles = []
        for url in self.urls:
            # print(url)
            article_info = {"title":"","contents":"","url":"","category":""}
            checkc = True
            category = self.categories[self.choose_category-1]
            try:
                g = Goose({'stopwords_class':StopWordsKorean})
                article = g.extract(url=url)
                title = article.title
            except:
                continue
            #print(title)
            contents = self.read_article_contents(url)
            if(contents==""):
                continue
            find_email = re.compile('[a-zA-Z0-9_-]+@[a-z]+.[a-z]+').finditer(contents)
            for email in find_email:
                contents = contents[:email.start()]
            article_info["category"] = category
            article_info["contents"] = contents
            article_info["title"] = title
            article_info["url"] = url
                        # print(self.article_info)
            articles.append(article_info)
            self.num_article+=1

        return articles    
        

if __name__ == "__main__":

    # 단순 카테고리만 할시에는 jungang_crawling(1)이것으로 초기화를하고,
    # category_crawling( 카테고리 번호 )에서 카테고리 번호를 넣어준다(외부에서 받아올 예정)
    # 그리고 그 번호를 get_news에다가도 넣어준다

    A = Jungang_crawling()
    A.category_crawling(2)
    ll = A.get_news(3)
    # print(ll)
  
    # A = jungang_crawling(2)

    # 반대로 단순 검색시에는 2번으로 초기화를 하고
    # 안에는 검색어를 넣는다
    # 얜 검색결과가 없을떄를 대비해 check_valid를 넣어서 확인을 한다
    



    # A.searching_category("이명박")

    # for i in A.urls:
    #     print(i)

    # if(A.check_valid):
    #     ll = A.get_news()
    # else:
    #     print("검색결과가 없습니다")

    # print(len(ll))

    # 마지막으로 검색과 카테고리 검색 두개다 할때는,
    # 메소드는 검색어랑 같은 메소드를 쓴다
    # 다만 jungang_crawling(3)이 번호가 3이고, 입력받은 카테고리 번호를
    # get_news에다가 매개변수로 넣어주면된다
