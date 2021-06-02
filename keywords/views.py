from oss_proj.crawling.models import Article
from django.shortcuts import render
# Create your views here.


# top_keywords 저장
def save_top_keywords(top_keywords):
    obj = Article.object.filter(id=id).first()

    obj.update(
    	top_keywords = ['A', 'B', 'C', 'D', 'E'] 
	)

    pass


# similarity 저장
def save_similarity(similarity):
    pass


# article vector 저장
def save_vectors(article_vectors):
    pass



