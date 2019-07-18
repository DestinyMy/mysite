from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator
from .models import Blog, BlogType

def blog_list(request):
    blog_all_list = Blog.objects.all()
    paginator = Paginator(blog_all_list, 10) #每10页进行分页
    page_num = request.GET.get('page', 1) #获取url的页面参数(GET请求)
    page_of_blogs = paginator.get_page(page_num)
    context = {}
    context['page_of_blogs'] =  page_of_blogs
    context['count'] = Blog.objects.all().count() #第二种方式得到博文的篇数，在界面使用时为blog.count或直接用count
    context['blog_types'] = BlogType.objects.all()
    return render_to_response('blog/blog_list.html', context)

def blog_detail(request, blog_pk):
    context = {}
    context['blog'] = get_object_or_404(Blog, pk=blog_pk)
    return render_to_response('blog/blog_detail.html', context)

def blogs_with_type(request, blog_type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    context['blogs'] = Blog.objects.filter(blog_type=blog_type) 
    context['blog_type'] = blog_type
    context['blog_types'] = BlogType.objects.all()
    return render_to_response('blog/blogs_with_type.html', context)