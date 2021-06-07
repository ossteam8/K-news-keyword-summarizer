from django.contrib import admin
from django.urls import path

from .views import KeywordsListView, KeywordsDetailView


urlpatterns = [
    path('<int:category_id>', KeywordsListView.as_view(), name='keywords_list'),
    path('<int:category_id>/<int:topics_num>', KeywordsDetailView.as_view(), name='keywords_detail'),  # (?P<keyword>[\w-]+)/$
]