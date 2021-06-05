import json, datetime
from django.shortcuts import render
from django.views.generic.list import ListView 
from django.views.generic.detail import DetailView

from crawling.models import Article, Category


# category 선택 시, 해당 category 의 keywords 를 보여줌!
class KeywordsListView(ListView):
	template_name = 'crawling/keywords_list.html' 

	def get(self, request, category_id):
		category = Category.objects.filter(id=category_id).values('category')[0]['category']

		category_object = Category.objects.filter(pk=category_id)
		category_object.update(
		  topics={1: [ ['k1', 'k11'], {11: 0.1, 22: 0.2, 35555:0.3} ] , 2: [ ['k2', 'k22', 'k222'], {10: 1, 11: 1.1, 12: 1.2} ] }
		)

		# queryset: dict {1: ['k1', ,,,], 2: ['k2', ,,,], ,,,}
		keywords_queryset = Category.objects.filter(id=category_id).values('keywords')[0]['keywords']
		keywords_json = {}
		if keywords_queryset:
			for k, v in keywords_queryset.items():
				keywords_json[v[0]] = k
		
		keywords_json = json.dumps(keywords_json)

		week_date = datetime.datetime.now() - datetime.timedelta(days=7)
		articles_list = Article.objects.prefetch_related('category').filter(register_date__gte=week_date, category_id=category_id).order_by('register_date')

		return render(request, self.template_name, {'category_id': category_id, 'category': category, 'articles_list': articles_list, 'keywords_json': keywords_json})


# 키워드 선택 -> 기사 나열!!  
# prefetch_related: 역방향 참조 이용해서 해당 카테고리에 있는 article을 가져와야함.
# 기사 가져올 때 해당 키워드가 있어야 함
class KeywordsDetailView(DetailView):
	template_name = 'crawling/keywords_detail.html'

	def get(self, request, category_id, keyword):  # type(keyword): str				
		queryset = []
		category = Category.objects.filter(pk=category_id)
		# {1: [ ['k1', ,,,], {id: rate, id: rate, id: rate, ,,,} ] , 2: [ ['k2', ,,,], {id: rate, id: rate, id: rate, ,,,} ] ,,,}
		topics = Category.objects.filter(pk=category_id).values('topics')[0]['topics']
		
		if topics:
			for v in topics.values():
				# v[1].keys() -> article id
				if keyword in v[0]:  # ['k1', ,,,]
					for id in v[1].keys():
						article = Article.objects.filter(pk=id).first()
						if article:
							queryset.append(article)

		return render(request, self.template_name, {'articles_list': queryset, 'category': category, 'keyword': keyword})




