"""
URL configuration for articleAgregator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from articleAgregator import view
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', view.index, name='mainpage'), 
    path('addarticle', view.add_article, name='addarticle'),
    path('logout/', view.sign_out, name='logout'),
    path('login/', view.sign_in, name='login'),
    path('register/', view.sign_up, name='register'),
    path('api/article', view.ArticleList, name='api'),
    path('api/article/<int:pk>/', view.ArticleDetail, name='apiName'),
    path('listDetail/', view.ArticleListGeneric.as_view()),
    path('detail/<pk>/', view.ArticleDetailView.as_view()),
    path('update/<pk>/', view.ArticleUpdateView.as_view()),
    path('delete/<pk>/', view.ArticleDeleteView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



