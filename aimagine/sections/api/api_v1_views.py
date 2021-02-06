import os
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings as conf_settings
from django.views.decorators.csrf import csrf_exempt
from pathlib import Path
from PIL import Image, ImageDraw, ExifTags, ImageColor, ImageEnhance
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
def yolo_faceblur(request):
    byte_array_image = request.POST.get('image')
    print("len",len(byte_array_image))
    detector = YoloDetector(img_to_detect=byte_array_image)
    result = detector.run_singleframe_detector()
    print("result", result)
    data = detector.getResult()
    data = {'message' : 'ciao','name' : 'pippo', 'age' : 50}
    return JsonResponse(result)
