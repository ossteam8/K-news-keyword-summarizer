import re
from goose3 import Goose
from goose3.text import StopWordsKorean
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.relativedelta import relativedelta
from urllib.request import Request, urlopen

class Herald_crawling:
    def __init__(self): 
        self.categories = ['정치','경제','사회']
        self.article_url = ""
        self.urls = []
        self.articles = [] # 각 기사들의 정보들을 담을 리스트
        self.check_valid = True # 검색했을때 나오는 데이터가 나오는지 안나오는지를 비교
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
            now = datetime.now()
            before_one_week = now-relativedelta(days=1) # 여기서 days값이 몇일전을의미 테스트용으론 1이 적당
            before_one_week =  self.get_date(before_one_week) # 일주 전을 의미
            try:
                req = Request(self.article_url,headers={'User-Agent': 'Mozilla/5.0'})
                with urlopen(req) as response:
                    html = response.read()
                    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
                    #기사의 url들을 파싱하는 부분
                    article_list = soup.find("div",{"class":"list_wrap"})
                    article_list = article_list.find("div",{"class":"list_l"})
                    try:
                        article_list = article_list.find("div",{"class":"list"})
                        article_list = article_list.find("ul")
                        article_list = article_list.find_all("li")
                    except:
                        self.check_valid=False
                        print("리스트 읽어오기 끝")
                        return    
                    try:
                        for article in article_list:
                            article_time = article.find("div",{"class":"l_date"}).string
                            article_time = self.get_date(article_time)
                            if(int(article_time)>int(before_one_week)):
                                continue
                            if(int(article_time)<int(before_one_week)):
                                return
                            link =  article.find("a")
                            link = "http://biz.heraldcorp.com/"+link['href']
                            self.urls.append(link)
                    except:
                        print("url 찾기 실패")
                        return
                    try:
                        next_url = ""
                        pages = soup.find("div",{"class":"page_wrap"})
                        current_page = pages.find("a",{"class":"active"}).string  # 현재 페이지 찾음
                        next_button = pages.find("a",{"class":"next"})
                        pages = pages.find_all("a")
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
                            self.article_url = "http://biz.heraldcorp.com/"+next_url
                    except:
                        print("페이지 이동 실패")
                        return
            except:
                return




    def category_crawling(self, choose_category):
        if choose_category==1: #정치
            self.article_url = "http://biz.heraldcorp.com/list.php?ct=010108000000"
            self.choose_category = 1
        elif choose_category==2: # 경제
            self.article_url="http://biz.heraldcorp.com/list.php?ct=010104000000"
            self.choose_category = 2
        else: #사회
            self.article_url = "http://biz.heraldcorp.com/list.php?ct=010109000000"
            self.choose_category = 3
        self.crawling()
        

    def read_article_contents(self,url):
        try:
            req = Request(url,headers={'User-Agent': 'Mozilla/5.0'})
            with urlopen(req) as response:
                html = response.read()
                soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
                article_contents = soup.find("div",{"id":"articleText"})
                text = ""
                try:
                    text = text + ' '+ article_contents.get_text(' ', strip=True)
                except:
                    print("error" , url)
                return text
        except:
            return ""                
    



    def get_news(self):# 실제로 url에 들어가 기사들을 읽어온다 , 첫번째 카테고리만으로 검색했을때 데이터를 가져와준다
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
            if title=="":
                continue
            contents = self.read_article_contents(url)
            if contents == "":
                continue
            find_email = re.compile('[a-zA-Z0-9_-]+@[a-z]+.[a-z]+').finditer(contents)
            for email in find_email:
                contents = contents[:email.start()]
            article_info["category"] = category
            article_info["contents"] = contents
            article_info["title"] = title
            article_info["url"] = url
            self.articles.append(article_info)
        return self.articles    
        

if __name__ == "__main__":

    A = Herald_crawling()
    A.category_crawling(2)
    ll = A.get_news()

 