import markdown

from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.utils.text import slugify
from django.views.generic import ListView
from markdown.extensions.toc import TocExtension

from blog.models import Article


class IndexView(ListView):
    template_name = "blog/index.html"


def index(request):
    return render(request, "blog/index.html", {"model": Article.objects.filter(parent=None)})


def article(request, pk):
    model = get_object_or_404(Article, id=pk)
    model.viewed()
    root = model.get_root()

    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=slugify),
    ])
    content = md.convert(model.content)
    toc = md.toc
    context = {'model': model, 'root': root, 'content': content, 'toc': toc}
    return render(request, 'blog/article.html', context)


def page_not_found(request, exception):
    return redirect("/", False, {"msg": "404 Page NOT found!"})
