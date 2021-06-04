"""oss_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from crawling.views import CategoryListView, CategoryDetailView, ArticleListView, ArticleDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', CategoryListView.as_view(), name = 'index'),

    path('keywords/<int:category_id>', CategoryDetailView.as_view(), name='category_keywords'),
    path('articles/<int:category_id>/<keyword>', ArticleListView.as_view(), name='article_list'),  # (?P<keyword>[\w-]+)/$
    path('summary/<int:article_id>', ArticleDetailView.as_view(), name='summary'),
]

