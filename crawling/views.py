from django.shortcuts import render

from django.urls import reverse_lazy
# Generic View는 정해진 것을 사용하기 때문에 쉽지만 정해진 규약이 많다
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView  # show data
from django.views.generic.edit import CreateView, UpdateView, DeleteView  # add data

from .models import Article


# Create your views here.
def index(request):
    return render(request, 'crawling/index.html')

def keywordCharts(request):
    return render(request, 'crawling/keywordCharts.html')


# class ProductList(ListView):
#     model = Product
#     template_name = 'product/product.html'
#     # variable name to use in template(html)
#     context_object_name = 'product_list'


# class KeywordListView(generic.ListView):
#     template_name = 'dsfdsfdsf.html'
#     models = Keyword


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

