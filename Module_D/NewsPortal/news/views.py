from django.http import HttpRequest , HttpResponse
from django.shortcuts import render
from django.urls import reverse , reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PostForm
from .models import Post
from .filters import NewsFilter

from pprint import pprint


class NewsList(ListView):
    model = Post
    ordering = 'cr_time'
    template_name = 'postslist.html'
    context_object_name = 'newslist'
    paginate_by = 10


class SearchNewsList(ListView):
    model = Post
    ordering = 'cr_time'
    template_name = 'searchpostslist.html'
    context_object_name = 'newslist'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()  # Изначальный queryset = Post.objects.all()
        self.newsfilterset = NewsFilter(self.request.GET, queryset)  # Применяем к нему параметры QueryDict из фильтра NewsFilter
        return self.newsfilterset.qs  # Получаем queryset с целевым набором. Теперь это надо добавить в context

    def get_context_data(self, **kwargs):  # Переопределяем контекст
        context = super().get_context_data()
        context['newsfilterset'] = self.newsfilterset  # Добавляем новый QuerySet
        return context


class SpecialPost(DetailView):
    model = Post
    ordering = 'cr_time'
    template_name = 'specialpost.html'
    context_object_name = 'specialpost'
    pk_url_kwarg = 'id'


class CreateNews(CreateView):
    model = Post  # К какой модели применяем
    form_class = PostForm  # Указываем нашу разработанную форму
    template_name = 'createnews.html'  # В каком шаблоне применяем
    success_url = reverse_lazy('list_posts')

    def form_valid(self, form):  # Метод вызывается, когда проверка запроса POST прошла успешно. Можно добавить действие.
        posts = form.save(commit=False)  # Берем поля заполненной пользователем формы POST без сохранения в БД
        posts.type = 'NW'  # Переназначаем поле c 'post' - по умолчанию на type'
        return super().form_valid(form)  # Вызываем метод в родительском классе с измененной формой

    def get_success_url(self):
        return reverse('list_posts')


class UpdateNews(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'editnews.html'

    def get_success_url(self):
        return reverse('special_post', kwargs={'id': self.kwargs['pk']})  # kwargs - параметры из URL адреса, переданные в View


class CreateArticle(CreateView):
    model = Post  # К какой модели применяем
    form_class = PostForm  # Указываем нашу разработанную форму
    template_name = 'createarticles.html'  # В каком шаблоне применяем

    def get_form_class(self):
        form_class = super(CreateArticle, self).get_form_class()
        return form_class

    def form_valid(self, form):
        posts = form.save(commit=False)
        posts.type = 'AR'
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('list_posts')


class UpdateArticle(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'editarticle.html'


class DeletePost(DeleteView):
    model = Post
    template_name = 'deletepost.html'
    success_url = reverse_lazy('list_posts')  #  Переход после создания. Возвращается с помощью метода get_success_url


def iamuser(request: HttpRequest):
    user = request.user
    return HttpResponse(user)
