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