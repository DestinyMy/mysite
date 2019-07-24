from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('<int:blog_pk>', views.blog_detail, name='blog_detail'),
    path('blog_type/<int:blog_type_pk>', views.blogs_with_type, name='blogs_with_type'),
<<<<<<< HEAD
    path('date/<int:year>/<int:month>', views.blogs_with_date, name="blogs_with_date"),
=======
>>>>>>> b4bbb4c76f39b52dbf64ed5e83ae9589a8273a98
]
