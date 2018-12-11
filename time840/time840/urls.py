"""time840 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from time840 import settings
from django.views.static import serve
from blog.user import user
from blog.blog import blog
from blog.article import article
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'medi/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
    url(r'^register/',user.Register.as_view(),name='register'),
    url(r'^check_username/',user.CheckUsername.as_view(),name='check_username'),
    url(r'^login/',user.Login.as_view(),name='login'),
    url(r'^valid/', user.ValidCode.as_view(), name='valid'),
    url(r'^index/', user.Index.as_view(), name='index'),
    url(r'^out/', user.Out.as_view(), name='out'),
    url(r'^alter_password/', user.AlterPassword.as_view(), name='alter_password'),

    url(r'^set/',blog.Set.as_view(),name='set'),
    url(r'^backend/',blog.Backend.as_view(),name='backend'),
    url(r'^category_add/', blog.CategoryAdd.as_view(), name='category_add'),
    url(r'^comment/',blog.Comment.as_view(),name='comment'),
    url(r'^config/',blog.Config.as_view(),name='config'),
    url(r'^upload_avatar/',blog.UploadAvatar.as_view(),name='upload_avatar'),
    url(r'^method/',blog.Method.as_view(),name='method'),

    url(r'^article_add',article.ArticleAdd.as_view(),name='article_add'),
    url(r'^article_update/(?P<pk>.+).html',article.ArticleUpdate.as_view(),name='article_update'),
    url(r'^article_del/(?P<pk>.+)', article.ArticleDel.as_view(), name='article_del'),
    url(r'^commit_del/(?P<pk>.+)', article.CommitDel.as_view(), name='commit_del'),
    url(r'^upload_img/', article.UploadImg.as_view()),
    url(r'^comment_add/', article.CommentAdd.as_view(), name='comment_add'),

    url(r'^up_down/$',article.UpOrDown.as_view(),name='up_down'),

    url(r'^(?P<username>[\w]+)/(?P<condition>category|tag|archive)/(?P<param>.*).html',blog.Kind.as_view(),name='kind'),
    url(r'^(.+)/([0-9]{1,2}).html', blog.BlogArticle.as_view(), name='blog_article'),


    url(r'(?P<username>.+)/',blog.PersonBlog.as_view(),name='blog'),

]
