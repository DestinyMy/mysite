from read_statistics.models import ReadNum
from django.contrib.contenttypes.models import ContentType

def read_once(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)
    if not request.COOKIES.get(key): #判断是否存在这条cookie，不存在就使阅读数量加1
        if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
            #存在记录
            readnum = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
        else:
            #不存在对应的记录
            readnum = ReadNum(content_type=ct, object_id=obj.pk)
        #阅读数加一
        readnum.read_num += 1
        readnum.save()
    return key