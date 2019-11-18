import markdown
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse

from tutorials.models import Topic, Article


def index(request):
    return render(request, 'tutorials/index.html', {'model': Topic.objects.filter(parent=None)})


def article(request, pk):
    model = get_object_or_404(Article, id=pk)
    root = model.topic.get_root()
    context = {'model': model, 'root': root}
    return render(request, 'tutorials/article.html', context)

