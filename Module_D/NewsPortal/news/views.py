from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin

from .custom_mixin import OwnerPermissionRequiredMixin
from .forms import PostForm
from .models import Post, Author, Category, UserCategory
from .filters import NewsFilter

from pprint import pprint

from .tasks import send_mail, send_mail_function


class NewsList(ListView):
    model = Post
    ordering = 'cr_time'
    template_name = 'postslist.html'
    context_object_name = 'newslist'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(NewsList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['currentuserid'] = self.request.user.id
        context['isauthor'] = all([Author.objects.filter(author__username=self.request.user).exists(),
                                  self.request.user.groups.filter(name='authors').exists()])
        if self.request.user.is_authenticated:
            context['curr_subscribes'] = self.request.user.category_set.values_list('catname', flat=True)
        return context


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


class CreateNews(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    permission_denied_message = 'Вы не являетесь автором на нашем сайте.'
    model = Post  # К какой модели применяем
    form_class = PostForm  # Указываем нашу разработанную форму
    template_name = 'createnews.html'  # В каком шаблоне применяем
    success_url = reverse_lazy('list_posts')

    def form_valid(self, form):  # Метод вызывается, когда проверка clean() POST прошла успешно. Можно добавить действие.
        self.postform = form.save(commit=False)  # Берем поля заполненной пользователем формы POST без сохранения в БД
        self.postform.type = 'NW'  # Переназначаем поле c 'post' - по умолчанию на type'
        self.postform.postAuthor = Author.objects.get(author__username=self.request.user)

        return super().form_valid(form)  # Вызываем метод в родительском классе с измененной формой

    # Проверка на 3 поста сутки
    def has_permission(self):
        day_ago_time = datetime.now() - timedelta(days=1)
        posts_numbers_last_day = Post.objects.filter(cr_time__gt=day_ago_time,
                                                     postAuthor__author__username=self.request.user).count()
        if posts_numbers_last_day >= 3:
            raise PermissionDenied('Вы слишком много пишите, отдохните!')

        perms = self.get_permission_required()
        return self.request.user.has_perms(perms)

    def get_success_url(self):
        return reverse('list_posts')


class UpdateNews(OwnerPermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_post'
    model = Post
    form_class = PostForm
    template_name = 'editnews.html'

    def get_success_url(self):
        return reverse('special_post', kwargs={'id': self.kwargs['pk']})  # kwargs - параметры из URL адреса, переданные в View


class CreateArticle(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    permission_denied_message = 'Вы не являетесь автором на нашем сайте.'
    model = Post  # К какой модели применяем
    form_class = PostForm  # Указываем нашу разработанную форму
    template_name = 'createarticles.html'  # В каком шаблоне применяем

    def form_valid(self, form):
        posts = form.save(commit=False)
        posts.type = 'AR'
        posts.postAuthor = Author.objects.get(author__username=self.request.user)
        return super().form_valid(form)

    # Проверка на 3 поста сутки
    def has_permission(self):
        day_ago_time = datetime.now() - timedelta(days=1)
        posts_numbers_last_day = Post.objects.filter(cr_time__gt=day_ago_time,
                                                     postAuthor__author__username=self.request.user).count()
        if posts_numbers_last_day >= 3:
            raise PermissionDenied('Вы слишком много пишите, отдохните!')

        perms = self.get_permission_required()
        return self.request.user.has_perms(perms)

    def get_success_url(self):
        return reverse('list_posts')


class UpdateArticle(OwnerPermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_post'
    model = Post
    form_class = PostForm
    template_name = 'editarticle.html'


class DeletePost(OwnerPermissionRequiredMixin, DeleteView):
    permission_required = 'news.delete_post'
    model = Post
    template_name = 'deletepost.html'
    success_url = reverse_lazy('list_posts')  # Переход после создания. Возвращается с помощью метода get_success_url


@login_required
def addtoauthors(request: HttpRequest):
    user = request.user
    authorgroup = Group.objects.get(name='authors')
    # Добавление юзера в группу authors
    if not user.groups.filter(name='authors').exists():  # Если юзера нет в группе authors
        authorgroup.user_set.add(user)

    # Добавление юзера в модель Authors
    if not Author.objects.filter(author__username=user).exists():  # Если юзера нет в модели Author
        Author.objects.create(author=user)
        message = 'Теперь вы автор и можете публиковать пост!'
    else:
        message = 'Вы уже автор'

    return render(request, 'addtoauthors.html', context={'message': message})


@login_required
def subscribe(request: HttpRequest, new_subscribe=None):
    user = request.user
    curr_subscribes = user.category_set.values_list('catname', flat=True)  # Все подписки-категории для юзера списком
    req_subscribe = request.GET['catname']  # Запрашиваемая категория на подписку
    if not (req_subscribe in curr_subscribes):  # Проверка активна ли подписка
        Category.objects.get(catname=req_subscribe).subscribers.add(user)
        new_subscribe = req_subscribe
        curr_subscribes = user.category_set.values_list('catname', flat=True)
    return render(request, 'subscribe.html', context={'curr_subscribes': curr_subscribes,
                                                           'new_subscribe': new_subscribe,
                                                           'req_subscribe': req_subscribe, }
                  )


@login_required
def unsubscribe(request: HttpRequest, old_subscribe=None):
    user = request.user
    curr_subscribes = user.category_set.values_list('catname', flat=True)  # Все подписки-категории для юзера списком
    req_unsubscribe = request.GET['catname']
    if req_unsubscribe in curr_subscribes:
        Category.objects.get(catname=req_unsubscribe).subscribers.remove(user)
        old_subscribe = req_unsubscribe
        curr_subscribes = user.category_set.values_list('catname', flat=True)
    return render(request, 'unsubscribe.html', context={'curr_subscribes': curr_subscribes,
                                                      'old_subscribe': old_subscribe,
                                                      'req_unsubscribe': req_unsubscribe, }
                  )