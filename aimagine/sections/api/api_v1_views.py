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
import boto3



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



'''
Gestire il request ed inviare alla funzione aws il bytearray ricevuto
'''
@csrf_exempt
@xframe_options_exempt
def yolo_faceblur(request):
    '''
    result = {'message' : 'message','name' : 'pippo', 'age' : 50}
    image_temp_file = NamedTemporaryFile()
    base64img_file = request.POST.get('file')
    imgdata = base64.b64decode(base64img_file)
    #str_image = str_image.encode('utf-8')
    print(len(imgdata))
    f = open('img.jpg','w+b')
    f.write(imgdata)
    f.close
    '''
    image_temp_file.write(imgdata)
    img = Image.open(image_temp_file)
    print(img.size)
    img.show()
    
    detector = YoloDetector(img_to_detect=img)
    result = detector.run_singleframe_detector()

    result = face_detector(abs_image_path, args['filename'].name) # Processa l'immagine
    args['items'] = result['items'] # Lista di elementi riconosciuti
    args['n_items'] = result['n_items'] # Numero di elementi riconosciuti
    args['rekog_imgsrc'] =  'media/'+result['rekog_filename']

    result['message'] = "Ho trovato i visi"
    print (result)
    return JsonResponse(result)

'''
Gestire il request ed inviare alla funzione aws il bytearray ricevuto
'''
@csrf_exempt
@xframe_options_exempt
def aws_faceblur(request):
    print(request.FILES['file'])
    #\  img.show()
    #\  detector = YoloDetector(img_to_detect=img)
    #\  result = detector.run_singleframe_detector()
    result = aws_detector(request.FILES['file'].read()) # Processa l'immagine
    
    args['items'] = result['items'] # Lista di elementi riconosciuti
    args['n_items'] = result['n_items'] # Numero di elementi riconosciuti
    #\  args['rekog_imgsrc'] =  'media/'+result['rekog_filename']

    result['message'] = "Ho trovato i visi"
    #\  print (result)
    return JsonResponse(result)


    
'''
Modificare il codice di aws_detector in modo che prelevi il bytearray dal Request e lo invii ad aws 
'''
# Call AWS Rekognition
def aws_detector_with_string_data(string_imgdata): # va tutto spostato in models
        # Rileva il percorso assoluto per leggere l'immagine da processare
        encoded_string = string_imgdata.encode()
        img_byte_array = bytearray(encoded_string)
        items = []
        client=boto3.client('rekognition')
        items = client.detect_faces(Image={'Bytes': img_byte_array})['FaceDetails']
        #-----------------------------------------------------------------------------------------------
        return {'items':items, 'n_items':len(items)}

def aws_detector(imgdata): # va tutto spostato in models
        # Rileva il percorso assoluto per leggere l'immagine da processare
        items = []
        client=boto3.client('rekognition')
        items = client.detect_faces(Image={'Bytes': imgdata})['FaceDetails']
        #-----------------------------------------------------------------------------------------------
        return {'items':items, 'n_items':len(items)}