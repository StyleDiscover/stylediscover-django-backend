import requests
import tempfile
from django.core import files
from django.core.files.images import ImageFile
from mainposts.models import MainPost
from mainposts.serializers import MainPostSerializer
from django.http import QueryDict
import os

def run(*args):
    mp_list = MainPost.objects.filter(media_type='IM').values()
    if 'imagepath':
        for list in mp_list:
            list_item = MainPost.objects.get(id=list['id'])
            image_name = os.path.split(list_item.media_url.name)[1]
            image_name = image_name.split('.')[:-1]
            image_name = '.'.join(image_name)
            image_name = image_name + '.jpg'
            new_path = f"main_post_media/{list_item.user.username}/images/{image_name}"
            list_item.media_url = new_path
            list_item.save()