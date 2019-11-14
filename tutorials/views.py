import markdown
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from tutorials.models import Topic


def index(request):
    return render(request, 'tutorials/index.html', {'model': Topic.objects.filter(parent=None)})


def topic(request, pk):
    model = get_object_or_404(Topic, id=pk)
    if model.content:
        model.content = markdown.markdown(model.content, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc'
        ])
    root = model.get_root()
    menu = root.get_children()
    context = {'model': model, 'root': model.get_root()}
    return render(request, 'tutorials/topic.html', context)

