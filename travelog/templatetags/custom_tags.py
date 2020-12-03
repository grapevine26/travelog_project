from django import template
import re

register = template.Library()


# regex = re.compile('src="[a-zA-Z0-9/._-]+"')
@register.filter
def first_sentence(value):
    regex = re.compile('([가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9/._!? -]+)')
    value = regex.findall(value)
    return value[1]


@register.filter
def first_picture(value):
    regex = re.compile('"[a-zA-Z0-9/._-]+"')
    value = regex.findall(value)
    print(value)
    if value:
        value = value[0].replace('"', '')
    else:
        value = ''
    return value


"""
<p>asddsaasd
<img src="/media/django-summernote/2020-12-02/3ceccbd9-7e5b-4783-a7f7-cce91c460435.jpg" style="width: 410px;">
</p><p>ㅇㄴㄻㄴㅇㄹ
<img src="/media/django-summernote/2020-12-02/fdae12f1-1dbf-4d22-9c8e-e7f91e1b2c1c.jpg" style="width: 880px;">
</p><p>ㄴㄻㅇㅇ
<img src="/media/django-summernote/2020-12-02/477ce3b2-8be3-4a28-90e1-6d1c45ed9664.png" style="width: 702px;">
</p>
"""
