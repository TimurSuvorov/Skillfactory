from django.urls import path
from .views import NewsList, SpecialPost, SearchNewsList, CreateNews, CreateArticle, UpdateNews, UpdateArticle, \
    DeletePost, subscribe, unsubscribe, CategoryListView
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', NewsList.as_view(), name='list_posts'),
    path('<int:id>', SpecialPost.as_view(), name='special_post'),
    path('search/', SearchNewsList.as_view(), name='news_search'),
    path('news/create/', CreateNews.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', UpdateNews.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', DeletePost.as_view(), name='news_delete'),
    path('articles/create/', CreateArticle.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', UpdateArticle.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', DeletePost.as_view(), name='article_delete'),
    path('subscribe/<int:pk>', subscribe, name='subscribe'),
    path('unsubscribe/<int:pk>', unsubscribe, name='unsubscribe'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list')
]
