#coding:utf-8
from django.conf import settings
import os
import time
import shutil

def check_and_get_video_type(type_obj,type_value,message):
    try:
        type_obj(type_value)
    except:
        return {'code':-1,'msg':message}
    return {'code':0,'msg':'success'}

def handle_video(video_file,video_id,number):
    path = os.path.join(settings.BASE_DIR,'app/dashboard/temp')
    name = '{}_{}'.format(int(time.time()),video_file.name)
    path_name = '/'.join([path,name])
    with open(path_name,'wb') as f:
        for temp_path in video_file.chunks():
            f.write(temp_path)


