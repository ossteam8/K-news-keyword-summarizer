from .AsiaMoney import *
from .dongailbo import *
from .hangyere import *
from .Herreld import *
from .jungangilbo import *
from .kukminilbo import *
from .kyeonghang import *
from .moneyToday import *
from .neilNews import *
from .YTN import *
from datetime import datetime
def politic_crawling():
    try:
        asia = AsiaMoney_crawling()
        jungang = Jungang_crawling()
        moneytoday = MoneyToday_crawling()
        herreld = Herald_crawling()
        hangyere = Hangyere_crawling()
        donga = Donga_crawling()
        kukmin = Kukmin_crawling()
        kyeonghang = Kyeonghang_crawling()
        neil = NeilNews_crawling()
        ytn = YTN_crawling()
        asia.category_crawling(1)
        asia_list = asia.get_news()

        jungang.category_crawling(1)
        jungang_list = jungang.get_news()
        print('중앙 끝')
        moneytoday.category_crawling(1)
        moneytoday_list = moneytoday.get_news()
        print('머니투데이 끝')
        herreld.category_crawling(1)
        herreld_list = herreld.get_news()

        hangyere.category_crawling(1)
        hangyere_list = hangyere.get_news()

        donga.category_crawling(1)
        donga_list = donga.get_news()
        kukmin.category_crawling(1)
        kukmin_list = kukmin.get_news()
        kyeonghang.category_crawling(1)
        kyeonghang_list = kyeonghang.get_news()
        neil.category_crawling(1)
        neil_list = neil.get_news()
        ytn.category_crawling(1)
        ytn_list = ytn.get_news()
        politic_list = asia_list+donga_list+hangyere_list+herreld_list+jungang_list+kukmin_list+kyeonghang_list+moneytoday_list+neil_list+ytn_list
        return politic_list
    except Exception as e:
        print(e)
def economic_crawling():
    try:
        asia = AsiaMoney_crawling()
        jungang = Jungang_crawling()
        moneytoday = MoneyToday_crawling()
        herreld = Herald_crawling()
        hangyere = Hangyere_crawling()
        donga = Donga_crawling()
        kukmin = Kukmin_crawling()
        kyeonghang = Kyeonghang_crawling()
        neil = NeilNews_crawling()
        ytn = YTN_crawling()
        asia.category_crawling(2)
        asia_list = asia.get_news()
        # print('아시아끝')
        jungang.category_crawling(2)
        jungang_list = jungang.get_news()

        moneytoday.category_crawling(2)
        moneytoday_list = moneytoday.get_news()

        herreld.category_crawling(2)
        herreld_list = herreld.get_news()

        hangyere.category_crawling(2)
        hangyere_list = hangyere.get_news()

        donga.category_crawling(2)
        donga_list = donga.get_news()
        kukmin.category_crawling(2)
        kukmin_list = kukmin.get_news()
        kyeonghang.category_crawling(2)
        kyeonghang_list = kyeonghang.get_news()
        neil.category_crawling(2)
        neil_list = neil.get_news()
        ytn.category_crawling(2)
        ytn_list = ytn.get_news()
        economic_list = asia_list+donga_list+hangyere_list+herreld_list+jungang_list+kukmin_list+kyeonghang_list+moneytoday_list+neil_list+ytn_list
        return economic_list
    except Exception as e:
        print(e)

def society_crawling():
    try:
        asia = AsiaMoney_crawling()
        jungang = Jungang_crawling()
        moneytoday = MoneyToday_crawling()
        herreld = Herald_crawling()
        hangyere = Hangyere_crawling()
        donga = Donga_crawling()
        kukmin = Kukmin_crawling()
        kyeonghang = Kyeonghang_crawling()
        neil = NeilNews_crawling()
        ytn = YTN_crawling()
        asia.category_crawling(3)
        asia_list = asia.get_news()

        jungang.category_crawling(3)
        jungang_list = jungang.get_news()

        moneytoday.category_crawling(3)
        moneytoday_list = moneytoday.get_news()

        herreld.category_crawling(3)
        herreld_list = herreld.get_news()

        hangyere.category_crawling(3)
        hangyere_list = hangyere.get_news()
        donga.category_crawling(3)
        donga_list = donga.get_news()
        kukmin.category_crawling(3)
        kukmin_list = kukmin.get_news()
        kyeonghang.category_crawling(3)
        kyeonghang_list = kyeonghang.get_news()
        neil.category_crawling(3)
        neil_list = neil.get_news()
        ytn.category_crawling(3)
        ytn_list = ytn.get_news()
        society_list = asia_list+donga_list+hangyere_list+herreld_list+jungang_list+kukmin_list+kyeonghang_list+moneytoday_list+neil_list+ytn_list
        return society_list
    except Exception as e:
        print(e)
    


def run_crawling():
    print(datetime.now())
    #정치
    try:
        politic_article_list = politic_crawling()
        #경제
        economy_article_list = economic_crawling()
        #사회
        society_article_list = society_crawling()
        return politic_article_list, economy_article_list, society_article_list

    except Exception as e:
        print(e)
    

