from django.template import Library
from django.db.models import Count
from django.db.models.functions import TruncMonth
from blog import models

register = Library()

@register.inclusion_tag('blog/classify.html')
def classify(username):
    user = models.User.objects.filter(username=username).first()
    category_count = models.Category.objects.filter(blog=user.blog).annotate(
        count=Count('article__nid')).values_list('title', 'count','pk')
    tag_count = models.Tag.objects.filter(blog=user.blog).annotate(count=Count('article__nid')).values_list(
        'title', 'count','pk')
    article_month = models.Article.objects.filter(blog=user.blog).annotate(
        month=TruncMonth('create_time')).values('month').annotate(count=Count('month')).values_list('month','count')
    return {'category_count': category_count, 'tag_count': tag_count, 'article_month': article_month, 'username': username}
