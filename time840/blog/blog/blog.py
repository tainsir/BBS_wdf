from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse
from django.views import View
from django.http import JsonResponse
from blog import models
from django.core.paginator import Paginator

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class PersonBlog(View):
    def get(self,request,username):
        user = models.User.objects.filter(username=username).first()
        if not user:
            return render(request,'error.html')
        article_list = models.Article.objects.filter(blog=user.blog).all()
        paginator = Paginator(article_list, 4)
        try:
            current_page_num = int(request.GET.get('page'))
            current_page = paginator.page(current_page_num)
        except Exception:
            current_page_num = 1
            current_page = paginator.page(current_page_num)

        if paginator.num_pages > 5:
            if current_page_num - 2 < 1:
                page_range = range(1, 6)
            elif current_page_num + 2 > paginator.num_pages:
                page_range = range(paginator.num_pages - 4, paginator.num_pages + 1)
            else:
                page_range = range(current_page_num - 2, current_page_num + 3)
        else:
            page_range = paginator.page_range
        return render(request, 'blog/blog.html', locals())


class Set(View):
    def get(self,request):
        return render(request,'blog/set.html')


class Backend(View):
    def get(self,request):
        article_list = models.Article.objects.filter(blog=request.user.blog).all()
        paginator = Paginator(article_list, 4)
        try:
            current_page_num = int(request.GET.get('page'))
            current_page = paginator.page(current_page_num)
        except Exception:
            current_page_num = 1
            current_page = paginator.page(current_page_num)
        if paginator.num_pages > 5:
            if current_page_num - 2 < 1:
                page_range = range(1, 6)
            elif current_page_num + 2 > paginator.num_pages:
                page_range = range(paginator.num_pages - 4, paginator.num_pages + 1)
            else:
                page_range = range(current_page_num - 2, current_page_num + 3)
        else:
            page_range = paginator.page_range
        return render(request, 'blog/backend.html',locals())


class Comment(View):
    def get(self,request):
        return render(request,'blog/comment.html')


class Config(View):
    def get(self,request):
        return render(request,'blog/config.html')

    def post(self,request):
        bg = request.POST.get('blog_bg')
        title = request.POST.get('blog_title')
        print(bg,title)
        request.user.blog.theme = bg
        request.user.blog.title = title
        request.user.blog.save()
        dic = {'status': '200',}
        return JsonResponse(dic)


class Method(View):
    def post(self,request):
        phone = request.POST.get('phone')
        request.user.phone=phone
        request.user.save()
        dic={'status':'200'}
        return JsonResponse(dic)


class UploadAvatar(View):
    def post(self,request):
        my_avatar = request.FILES.get('my_avatar')
        print(my_avatar)
        request.user.avatar = my_avatar
        request.user.save()
        return JsonResponse({'status':'200'})


class CategoryAdd(View):
    def get(self,request):
        user = request.user
        return render(request,'blog/category_add.html',locals())

    def post(self,request):
        title = request.POST.get('title')
        models.Category.objects.create(title=title,blog=request.user.blog)
        dic = {'status': '200', 'url': '/backend/'}
        return JsonResponse(dic)


class BlogArticle(View):
    def get(self, request, name, id):
        print(request.user.nid,id)
        is_up = models.UpAndDown.objects.filter(user=request.user,article_id=id).values('is_up').first()
        if is_up:
            print(is_up['is_up'])
        user = models.User.objects.filter(username=name).first()
        cur_article = models.Article.objects.filter(nid=id).first()
        if not cur_article:
            return render(request,'error.html')
        commit_list = models.Commit.objects.filter(article=cur_article).all()
        return render(request, 'blog/blog_article.html', locals())


class Kind(View):
    def get(self,request,username,*args, **kwargs):
        user = models.User.objects.filter(username=username).first()
        if not user:
            return render(request, 'error.html')
        article_list = user.blog.article_set.all()
        condition = kwargs.get('condition')
        param = kwargs.get('param')
        if 'tag' == condition:
            article_list = article_list.filter(tag__pk=param)
        elif 'category' == condition:
            article_list = article_list.filter(category__pk=param)
        elif 'archive' == condition:
            archive_list = param.split('-')
            article_list = article_list.filter(create_time__year=archive_list[0], create_time__month=archive_list[1])
        return render(request, 'blog/user_blog.html', locals())