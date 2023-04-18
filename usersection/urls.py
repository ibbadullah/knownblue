from django.urls import path
from .views import *


urlpatterns = [
    path('q/search/content/',articleSearchView,name="SearchArticle"),
]
