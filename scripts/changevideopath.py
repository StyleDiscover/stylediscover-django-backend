import requests
import tempfile
from django.core import files
from django.core.files.images import ImageFile
from mainposts.models import MainPost
from mainposts.serializers import MainPostSerializer
from django.http import QueryDict
import os

def run(*args):
    mp_list_vd = MainPost.objects.filter(media_type='VD').values()
    if 'videopath':
        for list in mp_list_vd:
            list_item = MainPost.objects.get(id=list['id'])
            image_name = os.path.split(list_item.media_url.name)[1]
            new_path = f"main_post_media/{list_item.user.username}/videos/{image_name}"
            list_item.media_url = new_path
            list_item.save()