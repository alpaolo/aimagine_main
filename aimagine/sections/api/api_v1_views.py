import os
import json
import base64
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings as conf_settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from tempfile import NamedTemporaryFile
from pathlib import Path
from PIL import Image, ImageDraw, ExifTags, ImageColor, ImageEnhance
from io import BytesIO, StringIO
from ... recog import detect_labels_local_file, getphoto
from ... aiprocess import face_detector 
from ... yolo import YoloDetector



# This views satisfy any kind of url with appropriate view and template but is confused
args = {}
args ={'section':'ai', 'title': 'Image recognition'}

def index(request):
    return HttpResponse("Hello, world. Is upload section")

@csrf_exempt
def test(request):
    message = request.POST.get('image')
    print (request.POST)
    #message = "ciao "
    data = {'message' : message,'name' : 'pippo', 'age' : 50}
    return JsonResponse(data)

def send_img():
    pass


@csrf_exempt
@xframe_options_exempt
def yolo_faceblur(request):
    result = {'message' : 'message','name' : 'pippo', 'age' : 50}
    image_temp_file = NamedTemporaryFile()
    base64img_file = request.POST.get('file')
    imgdata = base64.b64decode(base64img_file)
    #str_image = str_image.encode('utf-8')
    print(len(imgdata))
    '''
    f = open('img.jpg','w+b')
    f.write(imgdata)
    f.close
    '''
    image_temp_file.write(imgdata)
    img = Image.open(image_temp_file)
    print(img.size)
    #img.show()
    
    detector = YoloDetector(img_to_detect=img)
    result = detector.run_singleframe_detector()
    result['message'] = "Ho trovato i visi"
    print (result)
    return JsonResponse(result)
    
    
