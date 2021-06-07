import json, datetime
from django.shortcuts import render
from django.views.generic.list import ListView 
from django.views.generic.detail import DetailView

from crawling.models import Article, Category


#!/usr/bin/env python
# coding: utf-8
import pyLDAvis.gensim_models as gensimvis
import warnings
warnings.filterwarnings(action='ignore')
from gensim.models import LdaModel


class KeywordsListView(ListView):
	template_name = 'crawling/keywords_list.html' 

	def get(self, request, category_id):
		category = Category.objects.get(id=category_id).category
		keywords_queryset = Category.objects.get(id=category_id).keywords
		t = Category.objects.get(id=category_id).topics
		# print("adfadf",keywords_queryset)
		# print("adfadf",t)
		
		keywords_json = {}
		if keywords_queryset:
			for idx, value in zip(range(len(keywords_queryset)), keywords_queryset.values()):
				keywords_json[idx+1]= value[0:3]
		print(keywords_json)
		keywords_json = json.dumps(keywords_json)

		week_date = datetime.datetime.now() - datetime.timedelta(days=7)
		articles_list = Article.objects.prefetch_related('category').filter(register_date__gte=week_date, category_id=category_id).order_by('register_date')

		return render(request, self.template_name, {'category_id': category_id, 'category': category, 'articles_list': articles_list, 'keywords_json': keywords_json})



class KeywordsDetailView(DetailView):
	template_name = 'crawling/keywords_detail.html'

	def get(self, request, category_id, keyword):  # type(keyword): str				
		queryset = []
		category = Category.objects.get(pk=category_id).category
		topics = Category.objects.get(pk=category_id).topics
		keywords_list = []
		
		if topics:
			for v in topics.values():
				# v[1].keys() -> article id
				if keyword in v[0]:  # ['k1', ,,,]
					keywords_list = v[0]
					for id in v[1].keys():
						article = Article.objects.filter(pk=id).first()
						if article:
							queryset.append(article)

		return render(request, self.template_name, {'articles_list': queryset, 'category_id': category_id, 'category': category, 'keyword': keyword, 'keywords_list': keywords_list})


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

	try:
		week_date = datetime.datetime.now() - datetime.timedelta(days=7)
		article_id_list = list(Article.objects.filter(register_date__gte=week_date, category=category_object).values_list('id', flat=True).order_by('id'))
		article_contents_list = []
		for article_id in article_id_list:
			article_obj = Article.objects.get(pk=article_id)
			query = article_obj.contents + article_obj.title
			article_contents_list.append(query)
	except:
		return None, None

	return article_id_list, article_contents_list


# topics 저장
def save_topics(category, topics, topics_num):
	topics = dict(sorted(topics.items(), key=lambda x: len(x[1][1]), reverse=True))
	# category 분류
	if category == '정치':
		category_object = Category.objects.filter(category=category)
	elif category == '경제':
		category_object = Category.objects.filter(category=category)
	elif category == '사회':
		category_object = Category.objects.filter(category=category)
	else:
		print('wrong category')
	
	try:
		# {1: [ ['k1', ,,,], {id: rate, id: rate, id: rate, ,,,} ] , 2: [ ['k2', ,,,], {id: rate, id: rate, id: rate, ,,,} ] ,,,}
		keywords = {}
		for _, k in zip(range(topics_num), topics.keys()):
			article_num = len(topics[k][1])
			keywords[k] = [article_num,topics[k][0]]  # {1: ['k1', ,,,]}
		# topics, keywords 저장
		category_object.update(
			topics=topics,
			keywords=keywords,
		)
	except Exception as e:
		print(e)
		return False
	print('end')
	return True



