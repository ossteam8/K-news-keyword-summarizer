from django.shortcuts import render

from django.urls import reverse_lazy
# Generic View는 정해진 것을 사용하기 때문에 쉽지만 정해진 규약이 많다
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView  # show data
from django.views.generic.edit import CreateView, UpdateView, DeleteView  # add data

from .models import Article, Category


# Create your views here.
def index(request):
    return render(request, 'crawling/index.html')

def keywordCharts(request):
    return render(request, 'crawling/keywordCharts.html')


class CategoryKeywordsListView(ListView):
    template_name = 'crawlint/keywordCharts.html'
    
    context_object_name = 'keywords'  # view에서 template 에 전달할 context 변수명을 지정함

    def get_queryset(self, **kwargs):
        queryset = Category.objects.filter(
            category=self.request.session.get('category') 
        )
        return queryset.keywords  # 해당 카테고리의 키워드 반환


class ArticleListView(ListView):
    model = Article
    template_name = 'crawling/index.html'
    context_object_name = 'article_list'


class ArticleDetailView(DetailView):
    queryset = Article.objects.all()
    template_name = '.html'
    context_object_name = 'article'

# """
# django get parameter filtering
# keyword
# filtering content like query
# """




# def date_view(self, request):
#         week_date = datetime.datetime.now() - datetime.timedelta(days=7)
#         week_data = Order.objects.filter(register_date__gte=week_date)
#         data = Order.objects.filter(register_date__lt=week_date)
#         context = dict(
#             self.admin_site.each_context(request),
#             week_data=week_data,
#             data=data,
#         )
