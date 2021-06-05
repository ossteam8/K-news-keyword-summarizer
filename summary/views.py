from django.shortcuts import render
from django.views.generic.detail import DetailView

from crawling.models import Article


# summary 화면
class SummaryView(DetailView):
	# id = article id !! (pk)
	template_name = 'crawling/summary.html'

	def get(self, request, article_id):
		queryset = Article.objects.filter(pk=article_id).first()
		
		return render(request, self.template_name, {'article':queryset})
