from django.shortcuts import render_to_response, get_object_or_404
from read_statistics.utils import get_sevendays_read_data
from blog.models import Blog
from django.contrib.contenttypes.models import ContentType

def home(request):
    context = {}
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_sevendays_read_data(blog_content_type)
    context['read_nums'] = read_nums
    context['dates'] = dates
    return render_to_response('home.html', context)