from django.shortcuts import render

# from django.urls import reverse_lazy
# Generic View는 정해진 것을 사용하기 때문에 쉽지만 정해진 규약이 많다
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView  # show data
# from django.views.generic.edit import CreateView, UpdateView, DeleteView  # add data

import json
from django.db.models import query
# from django.db.models.query import Prefetch, QuerySet
import datetime
from itertools import zip_longest

from .models import Article, Category


# Create your views here.
def index(request):
	category_list = Category.objects.all()
	return render(request, 'crawling/index.html', {'category_list': category_list})


# category 선택 시, 해당 category 의 keywords 를 보여줌!
class CategoryDetailView(DetailView):
	template_name = 'crawling/keywords.html' 

	def get(self, request, category_id):
		print("category_id",category_id)
		# queryset: dict {'k1': w1, 'k2': w2, 'k3': w3, ...}
		keywords_queryset = Category.objects.filter(id=category_id).values('keywords')[0]['keywords']
		querysetJson = json.dumps(keywords_queryset)
		# == articles = Article.objects.select_related('category').filter(category_id=category_id)
		week_date = datetime.datetime.now() - datetime.timedelta(days=7)
		articles_queryset = Article.objects.prefetch_related('category').filter(register_date__gte=week_date, category_id=category_id).order_by('register_date')
		# obj = articles_queryset.filter(id=id)
		# obj.update(
		# 	top_keywords = ['A', 'B', 'C', 'D', 'E']
		# )
		print(articles_queryset)
		
		return render(request, self.template_name, {'keywords_list': keywords_queryset, 'articles_list': articles_queryset, 'queryset_json': querysetJson})


# 키워드 선택 -> 기사 나열!!  
# prefetch_related: 역방향 참조 이용해서 해당 카테고리에 있는 article을 가져와야함.
# 기사 가져올 때 해당 키워드가 있어야 함
class ArticleDetailView(DetailView):
	template_name = 'crawling/articles.html'

	def get(self, request, category_id, keyword):
		week_date = datetime.datetime.now() - datetime.timedelta(days=7)
		articles = Article.objects.prefetch_related('category').filter(register_date__gte=week_date, category_id=category_id).order_by('register_date')
		queryset = []
		for a in articles.values():
			if keyword in a['top_keywords']:
				queryset.append(a)  # 해당 키워드를 top_keywords에 포함하고 있는 객체만 append

		print(queryset)
		# top_keyword
		# obj = articles_queryset
		# for o in obj.values():
		# 	if o['top_keywords'] and 'A' in o['top_keywords']:
		# 		print(True)
		# 	print(o['top_keywords'])
		
		
		return render(request, self.template_name, {'articles_list': queryset})


# summary 화면
# class ArticleDetailView(DetailView):
#     # id = article id !! (pk)
#     queryset = Article.objects.filter(pk=id)
#     template_name = '.html'
#     context_object_name = 'article'


# 일주일 기사만 가져오기
# def date_view(self, request):
#         week_date = datetime.datetime.now() - datetime.timedelta(days=7)
#         week_data = Article.objects.filter(register_date__gte=week_date)
#         data = Order.objects.filter(register_date__lt=week_date)
#         context = dict(
#             self.admin_site.each_context(request),
#             week_data=week_data,
#             data=data,
#         )


# crontab 에서 실행한 함수에서 save_articles()로 article list 넘겨줌
def save_articles(politic_article_list, economy_article_list, society_article_list):
	politic_object = Category.objects.filter(category='정치').first()
	economy_object = Category.objects.filter(category='경제').first()
	society_object = Category.objects.filter(category='사회').first()
	# for politic in politic_article_list:
	# 	# article save
	# 	print(politic)
	# 	# for p in politic:
	# 	Article.objects.create(title=politic['title'], contents=politic['contents'], url=politic['url'], category=politic_object)
	
	# for economy in economy_article_list:
	# 	# article save
	# 	Article.objects.create(title=economy['title'], contents=economy['contents'], url=economy['url'], category=economy_object)

	# for society in society_article_list:
	# 	# article save
	# 	Article.objects.create(title=society['title'], contents=society['contents'], url=society['url'], category=society_object)

	for politic, economy, society in zip_longest(politic_article_list, economy_article_list, society_article_list, fillvalue=None):
		if politic:
			Article.objects.create(title=politic['title'], contents=politic['contents'], url=politic['url'], category=politic_object)
		if economy:
			Article.objects.create(title=economy['title'], contents=economy['contents'], url=economy['url'], category=economy_object)
		if society:
			Article.objects.create(title=society['title'], contents=society['contents'], url=society['url'], category=society_object)

