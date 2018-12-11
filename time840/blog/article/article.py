from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse
from django.views import View
from django.http import JsonResponse
from blog import models
import os
from time840 import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import transaction
from bs4 import BeautifulSoup


class ArticleAdd(View):

    def get(self,request):
        return render(request, 'article/article_add.html')

    def post(self,request):
        title = request.POST.get('title')
        content = request.POST.get('content')
        tag_info = request.POST.get('tag')
        category = request.POST.get('category')
        soup = BeautifulSoup(content, 'html.parser')
        tags = soup.find_all()
        for tag in tags:
            if tag.name == 'script':
                tag.decompose()
        desc = soup.text[0:150]
        art = models.Article.objects.create(title=title, content=content, desc=desc, category_id=category,blog_id=request.user.blog_id)
        if tag_info:
            tag_list = tag_info.split(',')
            for tag_info in tag_list:
                tag = models.Tag.objects.create(title=tag_info, blog_id=request.user.blog_id)
                models.Article2Tag.objects.create(article=art,tag=tag)
        dic = {'status': '200', 'url': '/backend/'}
        return JsonResponse(dic)


class UploadImg(View):
    def post(self,request):
        myfile = request.FILES.get('myfile')
        path = os.path.join(settings.BASE_DIR, 'media', 'img')
        if not os.path.isdir(path):
            os.mkdir(path)
        file_path = os.path.join(path, myfile.name)
        with open(file_path, 'wb') as f:
            for line in myfile:
                f.write(line)
        dic = {'error': 0, 'url': '/medi/img/%s' % myfile.name}
        return JsonResponse(dic)


class ArticleDel(View):
    def get(self,request,pk):
        models.Tag.objects.filter(article2tag__article__pk=pk).delete()
        models.Article.objects.filter(blog=request.user.blog,pk=pk).delete()
        url = reverse('backend')
        return redirect(url)


class CommitDel(View):
    def get(self,request,pk):
        models.Commit.objects.filter(pk=pk).delete()
        url = reverse('comment')
        return redirect(url)


class ArticleUpdate(View):
    def get(self,request,pk):
        article = models.Article.objects.filter(pk=pk).first()
        tags = article.tag.all()
        str=''
        for tag in tags:
            str += (tag.title+',')
        return render(request,'article/article_update.html',locals())

    def post(self,request,pk):
        title = request.POST.get('title')
        content = request.POST.get('content')
        tag_info = request.POST.get('tag')
        category = request.POST.get('category')
        soup = BeautifulSoup(content, 'html.parser')
        tags = soup.find_all()
        for tag in tags:
            if tag.name == 'script':
                tag.decompose()
        desc = soup.text[0:150]
        models.Article.objects.filter(pk=pk).update(title=title, content=content, desc=desc, category_id=category)
        ta = models.Article2Tag.objects.filter(article_id=pk).all()
        for t in ta:
            models.Tag.objects.filter(nid=t.tag_id).delete()
            t.delete()
        if tag_info:
            tag_list = tag_info.split(',')
            for tag_info in tag_list:
                tag = models.Tag.objects.create(title=tag_info, blog_id=request.user.blog_id)
                models.Article2Tag.objects.create(article_id=pk, tag=tag)
        dic = {'status': '200', 'url': '/backend/'}
        return JsonResponse(dic)


from django.core.mail import send_mail
from threading import Thread
from django.db.models import F


@method_decorator(login_required,name='dispatch')
class CommentAdd(View):

    def post(self,request):
        comment = request.POST.get('comment')
        id = request.POST.get('id')
        nid = request.POST.get('nid')
        if comment.startswith('@'):
            comment_list = comment.split('\n')[1:]
            comment = '\n'.join(comment_list)
            models.Article.objects.filter(nid=id).update(commit_num=F('commit_num') + 1)
            commit = models.Commit.objects.create(content=comment, user=request.user, article_id=id,parent_id=nid)
        else:
            models.Article.objects.filter(nid=id).update(commit_num=F('commit_num') + 1)
            commit = models.Commit.objects.create(content=comment,user=request.user,article_id=id)
        if not request.user.username == commit.article.blog.user.username:
            article_name = commit.article.title
            user_name = request.user.username
            t=Thread(target=send_mail, args=(
                    '您的%s文章被%s评论了' % (article_name, user_name), '这个人评论了:%s' % (comment,), settings.EMAIL_HOST_USER,
                    [commit.article.blog.user.email,]))
            t.start()
        dic = {'status': '200'}
        return JsonResponse(dic)


class UpOrDown(View):
    def post(self,request):
        dic = {'status': '200', 'msg': None}
        if request.user.is_authenticated():
            article_id = request.POST.get('article_id')
            is_up = request.POST.get('is_up')
            user = request.user
            ret = models.UpAndDown.objects.filter(user_id=user.pk, article_id=article_id).exists()
            if ret:
                dic['msg'] = '您已经点过了'
                dic['status'] = '201'
            else:
                with transaction.atomic():
                    models.UpAndDown.objects.create(user=user, article_id=article_id, is_up=is_up)
                    article = models.Article.objects.filter(pk=article_id)
                    if is_up:
                        article.update(up_num=F('up_num') + 1)
                        dic['msg'] = '点赞成功'
                    else:
                        article.update(down_num=F('down_num') + 1)
                        dic['msg'] = '反对成功'
        else:
            dic['msg'] = '请先登录'
            dic['status'] = '202'
        return JsonResponse(dic)