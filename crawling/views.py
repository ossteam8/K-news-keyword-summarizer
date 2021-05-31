from django.shortcuts import render

# from django.urls import reverse_lazy
# Generic View는 정해진 것을 사용하기 때문에 쉽지만 정해진 규약이 많다
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView  # show data
# from django.views.generic.edit import CreateView, UpdateView, DeleteView  # add data

from django.db.models.query import Prefetch


from .models import Article, Category


# Create your views here.
def index(request):
    return render(request, 'crawling/index.html')

def keywords(request):
    # 기사 키워드 render
    return render(request, 'crawling/keywords.html')


# category 선택 시, 해당 category 의 keywords 를 보여줌!
class CategoryKeywordsListView(ListView):
    template_name = 'crawling/keywords.html' 
    context_object_name = 'keywords_list'  # view에서 template 에 전달할 context 변수명을 지정함

    def get_queryset(self):
        category = self.request.GET.get('category')
        queryset = Category.objects.filter(category=category).values('keywords')[0] # {{'k1': w1, 'k2': w2, 'k3': w3, ...}}
        # keywords_dict[0]: {'k1': w1, 'k2': w2, 'k3': w3, ...}
        # 출력 
        print(category)
        print(queryset)

        return queryset

# get_context_data: 다른 객체들도 context에 넣어보내고 싶을 때 사용하는 method
# context = super(Category, self).get_context_data(**kwargs)


# 키워드 선택 -> 기사 나열!!  
# prefetch_related: 역방향 참조 이용해서 해당 카테고리에 있는 article을 가져와야함.
# category = Category.objects.prefetch_related(Prefetch('article_set', queryset=Post.objects.all()))
# # 기사 가져올 때 해당 키워드가 있어야하는데 
# class ArticleListView(ListView):
#     # model 속성으로 객체를 지정하는 것은 모든 generic view에서 가능.
#     category = Category.objects.prefetch_related(Prefetch('article_set', queryset=Category.objects.all()))

#     template_name = 'crawling/index.html'
#     context_object_name = 'article_list'


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
