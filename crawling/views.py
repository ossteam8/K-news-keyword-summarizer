import json, datetime
from django.shortcuts import render
from django.views.generic.list import ListView
from itertools import zip_longest

from .models import Article, Category

import pickle


class CategoryListView(ListView):
	template_name = 'crawling/index.html' 
	
	def get(self, request):
		category_list = Category.objects.all()

		num_of_articles = {}
		for i in range(7):
			week_date = datetime.datetime.now() - datetime.timedelta(days=i)
			num_of_articles[str(i+1)] = Article.objects.filter(register_date__date=week_date).count()
		num_of_articles = json.dumps(num_of_articles)

		return render(request, self.template_name, {'category_list': category_list, 'num_of_articles': num_of_articles})


# crontab 에서 실행한 함수에서 save_articles()로 article list 넘겨줌
def save_articles(politic_article_list, economy_article_list, society_article_list):
	politic_object = Category.objects.filter(category='정치').first()
	economy_object = Category.objects.filter(category='경제').first()
	society_object = Category.objects.filter(category='사회').first()
	for politic, economy, society in zip_longest(politic_article_list, economy_article_list, society_article_list, fillvalue=None):
		try:
			if politic:
				Article.objects.create(title=politic['title'], contents=politic['contents'], url=politic['url'], category=politic_object)
			if economy:
				Article.objects.create(title=economy['title'], contents=economy['contents'], url=economy['url'], category=economy_object)
			if society:
				Article.objects.create(title=society['title'], contents=society['contents'], url=society['url'], category=society_object)
		except Exception as e:
			print(e)
			continue
	
	return True


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
			title = Article.objects.filter(pk=article_id).values('title')[0]['title']  # str
			contents = Article.objects.filter(pk=article_id).values('contents')[0]['contents']  # str
			query = contents + title
			article_contents_list.append(query)
	except:
		return None, None

	return article_id_list, article_contents_list



# topics 저장
def save_topics(category, topics, topics_num):
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
		for _, k, v in zip(range(topics_num), topics.items()):
			keywords[k] = v[0]  # {1: ['k1', ,,,]}
		# topics, keywords 저장
		category_object.update(
			topics=topics,
			keywords=keywords,
		)
	except:
		return False

	return True

