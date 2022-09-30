from django.urls import path
from .views import NewsList, SpecialPost

urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:id>' , SpecialPost.as_view( )),

]