from django.shortcuts import render

from django.views import generic


# Create your views here.
def index(request):
    return render(request, 'crawling/index.html')

def charts(request):
    return render(request, 'crawling/charts.html')

def tables(request):
    return render(request, 'crawling/tables.html')




# class KeywordListView(generic.ListView):
#     template_name = 'dsfdsfdsf.html'
#     models = Keyword


# class ArticleListView(generic.ListView):
#     template_name = 'sdfsdf.html'
#     models = Article

# """
# django get parameter filtering
# keyword
# filtering content like query
# """


# class ArticleDetailView(generic.DetailView):
#     models = Article
#     template_name = 'sdfdsf.html'