from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from .forms import send_article_form, LoginForm, RegisterForm 
from .models import Article
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm
from django.contrib.auth.decorators import login_required

def index(request):
    post_article = Article.objects.all()
    users = User.objects.all()
    print("Article: ", post_article)
    auth = None
    try:
        print("isAuth?: ", request.session['auth'])
        auth = request.session['auth']
        print("Username: ", request.session['user'])
    except:
        print("User not authenticate")

    for post_art in post_article:
        print("post_art: ", post_art.id)
        print("image: ", post_art.images)
    for us in users:
        print("username: ", us.username)
        print("password: ", us.password)

    return TemplateResponse(request,"main.html", {"article_posts": post_article, "auth": auth})

@login_required(login_url='/') #redirect when user is not logged in
def add_article(request):
 
    auth = None
    try:
        auth = request.session['auth']
    except:
        return redirect('/login')

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
    return TemplateResponse(request,"addarticle.html", {"form": article_form, "auth": auth})

def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'register.html', { 'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'register.html', {'form': form})

def sign_out(request):
    logout(request)
    return redirect('/')

def sign_in(request):

    if request.method == 'GET':
        form = LoginForm()
        return render(request,'login.html', {'form': form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request, user)
                print("username: ", username)
                print("password: ", password)
                request.session['auth'] = True
                request.session['user'] = username
                return redirect('/')
            print("Not auth") 
        
        return render(request,'login.html',{'form': form})

