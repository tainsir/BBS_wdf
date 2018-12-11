from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse
from django.views import View
from blog.myform.myform import MyForm
from django.http import JsonResponse
from blog import models
from PIL import Image,ImageDraw,ImageFont
from blog.ValidCode import Random
from io import BytesIO
from django.core.paginator import Paginator
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class Register(View):
    def get(self,request):
        my_form = MyForm()
        return render(request,'user/register.html',locals())

    def post(self,request):
        my_form = MyForm(request.POST)
        if my_form.is_valid():
            username = my_form.cleaned_data.get('username')
            password = my_form.cleaned_data.get('password')
            email = my_form.cleaned_data.get('email')
            print(username,password,email)
            blog = models.Blog.objects.create(site_name=username)
            models.User.objects.create_user(username=username, password=password, email=email, blog=blog)
            dic={'status':'200','url':'/index/'}
        else:
            dic={'status':'201','msg':my_form.errors}
        return JsonResponse(dic)


class CheckUsername(View):
    def post(self,request):
        dic = {'status': '200', 'msg': None}
        username = request.POST.get('username')
        user = models.User.objects.filter(username=username).first()
        if user:
            dic={'status':'101','msg':'用户名被占用'}
        return JsonResponse(dic)


class ValidCode(View):
    def get(self,request):
        width = 240
        height = 35
        img = Image.new('RGB', (width,height), Random.random_color())
        img_draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('statics/font/ss.TTF',size=25)
        word = Random.random_word(5)
        img_draw.text((70,0), word, Random.random_color(), font=font)
        Random.random_point(img_draw,width,height)
        Random.random_line(img_draw,width,height)
        Random.random_arc(img_draw,width,height)
        f=BytesIO()
        img.save(f,'png')
        data = f.getvalue()
        request.session['valid'] = word
        return HttpResponse(data)


class Login(View):
    def get(self,request):
        return render(request,'user/login.html')

    def post(self,request):
        next = request.GET.get('next')
        username = request.POST.get('username')
        password = request.POST.get('password')
        valid = request.POST.get('valid')
        dic = {'status': '200', 'msg': None}
        if valid.upper() == request.session['valid'].upper():
            user = auth.authenticate(request,username=username, password=password)
            if user:
                auth.login(request, user)
                dic['url'] = '/index/'
                if next:
                    dic['url'] = next
                dic['msg'] = '登录成功'
            else:
                dic['status'] = '202'
                dic['msg'] = '用户名密码错误'
        else:
            dic['status'] = '201'
            dic['msg'] = '验证码错误'
        return JsonResponse(dic)


class Index(View):
    def get(self, request):
        user = request.user
        article_list = models.Article.objects.all()
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
        return render(request, 'user/index.html', locals())


class Out(View):
    def get(self, request):
        auth.logout(request)
        return redirect(reverse('index'))


@method_decorator(login_required,name='dispatch')
class AlterPassword(View):
    def get(self,request):
        return render(request,'user/alter_password.html')

    def post(self,request):
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        valid = request.POST.get('valid')
        dic = {'status': '200', 'msg': None}
        if valid.upper() == request.session.get('valid').upper():
            ret = request.user.check_password(old_password)
            if ret:
                request.user.set_password(new_password)
                request.user.save()
                dic['url'] = '/index/'
            else:
                dic['status'] = '202'
                dic['msg'] = '密码错误'
        else:
            dic['status'] = '201'
            dic['msg'] = '验证码错误'
        return JsonResponse(dic)
