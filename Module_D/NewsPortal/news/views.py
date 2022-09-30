from django.shortcuts import render
from django.views.generic import ListView , DetailView
from pprint import pprint

from .models import Post


class NewsList(ListView):
    model = Post
    ordering = 'cr_time'
    template_name = 'newslist.html'
    context_object_name = 'newslist'


class SpecialPost(DetailView):
    model = Post
    ordering = 'cr_time'
    template_name = 'specialpost.html'
    context_object_name = 'specialpost'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #r = Post.objects.filter(Post=self.model).values_list('postAuthor__author__username', flat=True)
        #print(r)
        return context