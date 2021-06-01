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
from crawling.views import CategoryDetailView, index#, ArticleListView, SearchFormView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name = 'index'),
    # path('search/', SearchFormView.as_view(), name='search'),

    path('<int:category_id>/keywords', CategoryDetailView.as_view(), name='keywords'),
    # path('<int:category_id>/keywords/<str:keyword>', ArticleDetailView.as_view(), name='article_detail')
]

