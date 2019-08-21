import datetime
from django.utils import timezone
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.core.cache import cache
from django.contrib import auth
from django.urls import reverse
from read_statistics.utils import get_sevendays_read_data, get_todayhot_read_date, get_yesterdayhot_read_date
from blog.models import Blog
from django.contrib.contenttypes.models import ContentType

# 得到前七天的热门阅读
def get_7hot_read_data():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gte=date) \
                        .values('id', 'title') \
                        .annotate(read_num_sum=Sum('read_details__read_num')) \
                        .order_by('-read_num_sum')
    return blogs[:7]

def home(request):
    context = {}
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_sevendays_read_data(blog_content_type)
    # 进行一个小时的缓存
    sevenday_hot_read = cache.get('sevenday_hot_read')
    if sevenday_hot_read is None:
        sevenday_hot_read = get_7hot_read_data()
        cache.set('sevenday_hot_read', sevenday_hot_read, 3600)

    context['dates'] = dates
    context['read_nums'] = read_nums
    context['today_hot_read'] = get_todayhot_read_date(blog_content_type)
    context['yesterday_hot_read'] = get_yesterdayhot_read_date(blog_content_type)
    context['sevenday_hot_read'] = sevenday_hot_read
    return render(request, 'home.html', context)

def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(request, username=username, password=password)
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    if user is not None:
        auth.login(request, user)
        return redirect(referer)
    else:
        return render(request, 'error.html', {'message':'用户名不存在或者用户名与密码不匹配'})