from django.shortcuts import render

# from django.urls import reverse_lazy
# Generic View는 정해진 것을 사용하기 때문에 쉽지만 정해진 규약이 많다
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView  # show data
# from django.views.generic.edit import CreateView, UpdateView, DeleteView  # add data

import json
from django.db.models import query
# from django.db.models.query import Prefetch, QuerySet


from .models import Article, Category


# Create your views here.
def index(request):
	category_list = Category.objects.all()
	return render(request, 'crawling/index.html', {'category_list': category_list})

# def keywords(request):
#     # 기사 키워드 render
#     return render(request, 'crawling/keywords.html')


# category 선택 시, 해당 category 의 keywords 를 보여줌!
class CategoryDetailView(DetailView):
	template_name = 'crawling/keywords.html' 
	# context_object_name = 'keywords_list'  # view에서 template 에 전달할 context 변수명을 지정함

	def get(self, request, category_id):
		print("category_id",category_id)
		# queryset: dict {'k1': w1, 'k2': w2, 'k3': w3, ...}
		keywords_queryset = Category.objects.filter(id=category_id).values('keywords')[0]['keywords']
		querysetJson = json.dumps(keywords_queryset)
		# == articles = Article.objects.select_related('category').filter(category_id=category_id)
		articles_queryset = Article.objects.prefetch_related('category').filter(category_id=category_id).order_by('register_date')
		obj = articles_queryset
		for o in obj.values():
			if o['top_keywords'] and 'A' in o['top_keywords']:
				print(True)
			print(o['top_keywords'])
		# obj = articles_queryset.filter(id=id)
		# obj.update(
		# 	top_keywords = ['A', 'B', 'C', 'D', 'E']
		# )
		# print(querysetJson)ㄴ
		# print(type(querysetJson))
		# print(queryset)
		# print(type(queryset))
		print(articles_queryset)
		
		return render(request, self.template_name, {'keywords_list': keywords_queryset, 'articles_list': articles_queryset, 'queryset_json': querysetJson})


# 키워드 선택 -> 기사 나열!!  
# prefetch_related: 역방향 참조 이용해서 해당 카테고리에 있는 article을 가져와야함.
# category = Category.objects.prefetch_related(Prefetch('article_set'))
# # 기사 가져올 때 해당 키워드가 있어야하는데 어떻게 구현??
class ArticleDetailView(DetailView):
	template_name = 'crawling/articles.html'
	# context_object_name = 'articles_list'

	def get(self, request, category_id, keyword):
		articles = Article.objects.prefetch_related('category').filter(category_id=category_id).order_by('register_date')
		quertset = []
		for a in articles.values():
			if keyword in a['top_keywords']:
				quertset.append(a)

		print(quertset)
		
		return render(request, self.template_name, {'articles_list': quertset})





# summary 화면
# class ArticleDetailView(DetailView):
#     # id = article id !! (pk)
#     queryset = Article.objects.filter(pk=id)
#     template_name = '.html'
#     context_object_name = 'article'

# """
# django get parameter filtering
# keyword
# filtering content like query
# """


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
