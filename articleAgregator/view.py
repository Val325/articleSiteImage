from django.http import HttpResponse
from django.template.response import TemplateResponse
from .forms import send_article_form 
from .models import Article

def index(request):
    post_article = Article.objects.all()
    print("Article: ", post_article)
    for post_art in post_article:
        print("post_art: ", post_art.id)


    return TemplateResponse(request,"main.html", {"article_posts": post_article})

def add_article(request):

    if request.method == "POST":
        article_form = send_article_form(request.POST, request.FILES)
        text = request.POST.get("text")
        author = request.POST.get("author")
        if article_form.is_valid():   
            print("author: ", author)
            print("text: ", text)
            artice_post = Article(text=text, author=author)
            artice_post = article_form
            artice_post.save()
    else:
        article_form = send_article_form()
    return TemplateResponse(request,"addarticle.html", {"form": article_form})

