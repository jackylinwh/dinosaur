from django.shortcuts import render, get_object_or_404

# Create your views here.
from blog.models import Article


def index(request):
    return render(request, "blog/index.html", {"model":Article.objects.filter(parent=None)})


def article(request, pk):
    model = get_object_or_404(Article, id=pk)
    root = model.get_root()
    context = {'model': model, 'root': root}
    return render(request, 'blog/article.html', context)