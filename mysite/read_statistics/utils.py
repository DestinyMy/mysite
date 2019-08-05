import datetime
from read_statistics.models import ReadNum, ReadDetail
from django.utils import timezone
from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType

# 对阅读进行计数
def read_once(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)
    if not request.COOKIES.get(key): #判断是否存在这条cookie，不存在就使阅读数量加1
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        # 总阅读数加一
        readnum.read_num += 1
        readnum.save()

        # 对每日阅读数量进行编辑统计
        date = timezone.now().date()
        readdetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        # 每天阅读数加一
        readdetail.read_num += 1
        readdetail.save()
    return key

# 得到前七天的阅读数
def get_sevendays_read_data(content_type):
    today = timezone.now().date()
    dates = []
    read_nums = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return dates, read_nums

# 得到今天的热门阅读
def get_todayhot_read_date(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    return read_details[:7]

# 得到昨天的热门阅读
def get_yesterdayhot_read_date(content_type):
    yesterday = timezone.now().date() - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')
    return read_details[:7]
