from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from .models import Blog, BlogType

EACH_PAGE_BLOG_NUM = 2 #每一页的博客数量(第一种设置博客数方式)

<<<<<<< HEAD
def common_code(request, blog_all_list):
=======
def blog_list(request):
    blog_all_list = Blog.objects.all()
>>>>>>> b4bbb4c76f39b52dbf64ed5e83ae9589a8273a98
    paginator = Paginator(blog_all_list, settings.EACH_PAGE_BLOG_NUM) #第二种设置博客数的方式
    page_num = request.GET.get('page', 1) #获取url的页面参数(GET请求)
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number #获取当前页的页码
    #获取当前页面前后2页的页面
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
                 list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
    #添加页码之间的省略标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, "...")
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append("...")
    #添加首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
<<<<<<< HEAD
        page_range.append(paginator.num_pages)
    context = {}
    context['page_of_blogs'] =  page_of_blogs
    context['page_range'] =  page_range
    context['blog_types'] = BlogType.objects.all()
    context['blog_dates'] = Blog.objects.dates('create_time', 'month', order='DESC')
    return context

def blog_list(request):
    blog_all_list = Blog.objects.all()
    context = common_code(request, blog_all_list)
    return render_to_response('blog/blog_list.html', context)

def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blog_all_list = Blog.objects.filter(blog_type=blog_type)
    context = common_code(request, blog_all_list)
    context['blog_type'] = blog_type
    return render_to_response('blog/blogs_with_type.html', context)

def blogs_with_date(request, year, month):
    blog_all_list = Blog.objects.filter(create_time__year=year, create_time__month=month) 
    context = common_code(request, blog_all_list)
    context['blogs_with_date'] = "%s年%s月" % (year, month)
    return render_to_response('blog/blogs_with_date.html', context)

def blog_detail(request, blog_pk):
    context = {}
    blog = get_object_or_404(Blog, pk=blog_pk)
    context['blog'] = blog
    context['previous_blog'] = Blog.objects.filter(create_time__lt=blog.create_time).first()
    context['next_blog'] = Blog.objects.filter(create_time__gt=blog.create_time).last()
    return render_to_response('blog/blog_detail.html', context)
=======
        page_range.append(paginator.num_pages) 
    context = {}
    context['page_of_blogs'] =  page_of_blogs
    context['page_range'] =  page_range
    context['count'] = Blog.objects.all().count() #第二种方式得到博文的篇数，在界面使用时为blog.count或直接用count
    context['blog_types'] = BlogType.objects.all()
    return render_to_response('blog/blog_list.html', context)

def blog_detail(request, blog_pk):
    context = {}
    context['blog'] = get_object_or_404(Blog, pk=blog_pk)
    return render_to_response('blog/blog_detail.html', context)

def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blog_all_list = Blog.objects.filter(blog_type=blog_type) 
    paginator = Paginator(blog_all_list, settings.EACH_PAGE_BLOG_NUM)
    page_num = request.GET.get('page', 1) #获取url的页面参数(GET请求)
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number #获取当前页的页码
    #获取当前页面前后2页的页面
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
                 list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
    #添加页码之间的省略标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, "...")
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append("...")
    #添加首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages) 
    context = {}
    context['blog_type'] = blog_type
    context['page_of_blogs'] =  page_of_blogs
    context['page_range'] =  page_range
    context['blog_types'] = BlogType.objects.all()
    return render_to_response('blog/blogs_with_type.html', context)
>>>>>>> b4bbb4c76f39b52dbf64ed5e83ae9589a8273a98
