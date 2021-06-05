from crawling.crawling_py.main_crawling import run_crawling
from crawling.views import save_articles


# db에 저장
def run():  
    politic_article_list, economy_article_list, society_article_list = run_crawling()
    save_articles(politic_article_list, economy_article_list, society_article_list)
    
    print("success!!")

    