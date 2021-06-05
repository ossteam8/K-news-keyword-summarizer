from django.contrib import admin
from django.urls import path

from .views import SummaryView

urlpatterns = [
    path('<int:article_id>', SummaryView.as_view(), name='summary'),
    
]