from django.http import HttpResponse
from django.template.response import TemplateResponse
from .forms import send_article_form 
from .models import Article

def index(request):
    post_article = Article.objects.all()
    print("Article: ", post_article)

    return TemplateResponse(request,"main.html", {"article_posts": post_article})

def add_article(request):
    article_form = send_article_form()

    if request.method == "POST":
        text = request.POST.get("text")
        author = request.POST.get("author")
        print("author: ", author)
        print("text: ", text)
        artice_post = Article(text=text, author=author)
        artice_post.save() 
    return TemplateResponse(request,"addarticle.html", {"form": article_form})

