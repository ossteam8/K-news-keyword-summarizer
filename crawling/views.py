import json, datetime
from django.shortcuts import render
from django.views.generic.list import ListView
from itertools import zip_longest

from .models import Article, Category


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
	print('시작')
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




