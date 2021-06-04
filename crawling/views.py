from django.db.models import query
from django.shortcuts import render

# from django.urls import reverse_lazy
# Generic View는 정해진 것을 사용하기 때문에 쉽지만 정해진 규약이 많다
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView 

import json
import datetime
from itertools import zip_longest

from .models import Article, Category


class CategoryListView(ListView):
	template_name = 'crawling/index.html' 
	
	def get(self, request):
		category_list = Category.objects.all()
		num_of_articles = {}
		for i in range(7):
			week_date = datetime.datetime.now() - datetime.timedelta(days=i)
			articles = Article.objects.filter(register_date__date=week_date).order_by('register_date')
			num_of_articles[str(i+1)] = articles.count()
		return render(request, self.template_name, {'category_list': category_list})


# category 선택 시, 해당 category 의 keywords 를 보여줌!
class CategoryDetailView(DetailView):
	template_name = 'crawling/keywords.html' 

	def get(self, request, category_id):
		category = Category.objects.filter(id=category_id).values('category')[0]['category']

		# queryset: dict {'k1': w1, 'k2': w2, 'k3': w3, ...}
		keywords_json = json.dumps(Category.objects.filter(id=category_id).values('keywords')[0]['keywords'])
		week_date = datetime.datetime.now() - datetime.timedelta(days=7)
		articles_list = Article.objects.prefetch_related('category').filter(register_date__gte=week_date, category_id=category_id).order_by('register_date')

		return render(request, self.template_name, {'category_id': category_id, 'category': category, 'articles_list': articles_list, 'keywords_json': keywords_json})


# 키워드 선택 -> 기사 나열!!  
# prefetch_related: 역방향 참조 이용해서 해당 카테고리에 있는 article을 가져와야함.
# 기사 가져올 때 해당 키워드가 있어야 함
class ArticleListView(ListView):
	template_name = 'crawling/articles.html'

	def get(self, request, category_id, keyword):  # type(keyword): str
		category = Category.objects.filter(pk=category_id).values('category')[0]['category']
		
		week_date = datetime.datetime.now() - datetime.timedelta(days=7)
		articles = Article.objects.prefetch_related('category').filter(register_date__gte=week_date, category_id=category_id).order_by('register_date')
		
		queryset = []
		# print(list(articles.values('top_keywords')))
		# for k, o in zip_longest(list(articles.values('top_keywords')), articles):
		# 	# top_keywords = list(articles.values('top_keywords'))
		# 	# print(top_keywords)
		# 	print(k['top_keywords'].values())
		# 	if k['top_keywords'].values() and keyword in k['top_keywords'].values():
		# 		queryset.append(o)  # 해당 키워드를 top_keywords에 포함하고 있는 객체만 append
		# 		print("queryset",queryset)
		# 		continue

		return render(request, self.template_name, {'articles_list': queryset, 'category': category, 'keyword': keyword})


# summary 화면
class ArticleDetailView(DetailView):
	# id = article id !! (pk)
	template_name = 'crawling/summary.html'

	def get(self, request, article_id):
		queryset = Article.objects.filter(pk=article_id).first()
		
		return render(request, self.template_name, {'article':queryset})



# crontab 에서 실행한 함수에서 save_articles()로 article list 넘겨줌
def save_articles(politic_article_list, economy_article_list, society_article_list):
	politic_object = Category.objects.filter(category='정치').first()
	economy_object = Category.objects.filter(category='경제').first()
	society_object = Category.objects.filter(category='사회').first()

	for politic, economy, society in zip_longest(politic_article_list, economy_article_list, society_article_list, fillvalue=None):
		if politic:
			Article.objects.create(title=politic['title'], contents=politic['contents'], url=politic['url'], category=politic_object)
		if economy:
			Article.objects.create(title=economy['title'], contents=economy['contents'], url=economy['url'], category=economy_object)
		if society:
			Article.objects.create(title=society['title'], contents=society['contents'], url=society['url'], category=society_object)


# NLP에 필요한 기사 return
def get_articles(category):  # category -> '정치' or '경제' or '사회'
	# category 분류
	if category == '정치':
		category_object = Category.objects.filter(category=category).first()
	elif category == '경제':
		category_object = Category.objects.filter(category=category).first()
	elif category == '사회':
		category_object = Category.objects.filter(category=category).first()
	else:
		print('wrong category')

	id_query = Article.objects.filter(category=category_object).values_list('id', flat=True).order_by('id')
	article_id_list = list(id_query)
	article_contents_list = []
	for article_id in article_id_list:
		contents_query = Article.objects.filter(pk=article_id).values('contents')[0]['contents']  # str
		article_contents_list.append(contents_query)

	return article_id_list, article_contents_list


# topics 저장
def save_topics(category, topics):
	# category 분류
	if category == '정치':
		category_object = Category.objects.filter(category=category)
	elif category == '경제':
		category_object = Category.objects.filter(category=category)
	elif category == '사회':
		category_object = Category.objects.filter(category=category)
	else:
		print('wrong category')
	
	category_object.update(
		topics = topics
	)