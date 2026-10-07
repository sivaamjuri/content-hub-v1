from django.urls import path
from .views import ArticleListView, CategoryListView, CategoryDetailView

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
]
