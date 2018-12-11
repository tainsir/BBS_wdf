from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
import re


class MyForm(forms.Form):
    username = forms.CharField(max_length=8,min_length=3,label='用户名',
                               error_messages={'max_length':'用户名长度必须为3~8','min_length':'用户名长度必须为3~8','required':'用户名必填'},
                               widget=widgets.TextInput(attrs={'class':'username'}))
    password = forms.CharField(max_length=8, min_length=4, label='密码',
                               error_messages={'max_length': '密码长度必须为4~8', 'min_length': '密码长度必须为4~8',
                                               'required': '密码必填'},
                               widget=widgets.PasswordInput(attrs={'class': 'password'}))
    re_password = forms.CharField(max_length=8, min_length=4, label='确认密码',
                                  error_messages={'max_length': '密码长度必须为4~8', 'min_length': '密码长度必须为4~8',
                                                  'required': '密码必填'},
                                  widget=widgets.PasswordInput(attrs={'class': 're_password'}))
    email = forms.EmailField(label='邮箱', widget=widgets.EmailInput(attrs={'class': 'email'}),
                             error_messages={'required': '邮箱必填', 'invalid': '不符合邮箱格式'})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match('^[a-z]{3,6}$', username):
            raise ValidationError('用户名只能是字母')
        else:
            return username

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        if not re.match('^\w{3,6}$', pwd):
            raise ValidationError('密码只能是数字、字母、下划线组成')
        else:
            return pwd

    def clean(self):
        pwd = self.cleaned_data.get('password')
        re_pwd = self.cleaned_data.get('re_password')
        if pwd and re_pwd:
            if pwd == re_pwd:
                return self.cleaned_data
            else:
                raise ValidationError('两次密码不一致')



