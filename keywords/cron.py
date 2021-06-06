from multiprocessing import freeze_support

from .views import get_articles, save_topics
from keywords.LDAkey_extractor import LDA_TR

def lda_job():
    freeze_support()
    lda_tr = LDA_TR()

    category = ["정치", "경제", "사회"]
    for c in category:
        id_news, news = get_articles(c)
        etc, num = lda_tr.save_topics(news, id_news)
        save_topics(c, etc, num)
    

