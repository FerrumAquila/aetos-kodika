__author__ = 'ironeagle'

import json
import requests

from base64 import b64decode
from django.shortcuts import *
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def index(request):
    return render(request, "web_render/index.html", {})


def get_html(request):
    url = request.GET['url']
    response = requests.get(url)
    html = response.text
    return HttpResponse(json.dumps({'success': True, 'html': html}))


def save_image(request):
    b64_text = request.POST['img_val']
    image_data = b64decode(b64_text[b64_text.index(',')+1:])
    tmp_file = ContentFile(image_data, 'downloaded123.png')
    path = default_storage.save('/Users/ironeagle/Code/my_projects/aetos_kodika/media/downloaded123.jpg', tmp_file)
    return HttpResponse(json.dumps({'success': True, 'path': str(path)}))