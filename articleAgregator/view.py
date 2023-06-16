from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from .forms import send_article_form, LoginForm, RegisterForm 
from .models import Article
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework.decorators import api_view
from rest_framework import  status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .serializers import ArticleSerializer

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
        print("user: ", post_art.user)
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
            artice_post = article_form.save(commit=False)
            artice_post.user = request.user
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

@api_view(['GET', 'POST'])
def ArticleList(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Article.objects.all()
        serializer = ArticleSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def ArticleDetail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Article.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticleSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ArticleSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#class ArticleDetail(generics.RetrieveAPIView):
#    queryset = Article.objects.all()
#    serializer_class = ArticleSerializer

class ArticleListGeneric(LoginRequiredMixin,ListView):
    login_url = '/login/'
    #raise_exception = True
    redirect_field_name = '/login/'
    template_name = "ArticleListGeneric.html" 
    # specify the model for list view
    model = Article

class ArticleDetailView(DetailView):
    template_name = "ArticleDetailGeneric.html" 
    # specify the model to use
    model = Article

class ArticleUpdateView(UpdateView):
    template_name = "ArticleUpdate.html" 
    # specify the model you want to use
    model = Article
 
    # specify the fields
    fields = [
        "user",
        "text",
        "author"
    ]
 
    # can specify success url
    # url to redirect after successfully
    # updating details
    success_url ="/"

class ArticleDeleteView(DeleteView):
    template_name = "ArticleDelete.html" 
    # specify the model you want to use
    model = Article
     
    # can specify success url
    # url to redirect after successfully
    # deleting object
    success_url ="/"
