from multiprocessing import freeze_support

from .views import get_articles, save_topics
from .keywords_extract.app import LDA_TR

def lda_job():
    print("start")    
    freeze_support()
    lda_tr = LDA_TR()
    print("start 2")
    category = ["정치", "경제", "사회"]
    for c in category:
        id_news, news = get_articles(c)
        etc, num = lda_tr.save_topics(news, id_news)
        print('타입 : ', etc)
        save_topics(c, etc, num)
    

    