import os
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings as conf_settings
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

def test(request):
    data = {'currency' : 'euro', 'count' : 5}
    return JsonResponse(data)


def yolo_faceblur(request):
    detector = YoloDetector()
    result = detector.run_singleframe_detector()
    print("result", result)
    data = detector.getResult()
    return JsonResponse(result)
