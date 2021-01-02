import os
from django.shortcuts import render
from django.http import HttpResponse

from django.core.files.storage import FileSystemStorage
from django.conf import settings as conf_settings
from pathlib import Path
from PIL import Image, ImageDraw, ExifTags, ImageColor, ImageEnhance
import boto3
from . recog import detect_labels_local_file, getphoto
from . aiprocess import face_detector 




# This views satisfy any kind of url with appropriate view and template but is confused
args = {}
args ={'section':'ai', 'title': 'Image recognition'}

def index(request):
    return HttpResponse("Hello, world. Is upload section")


def face_detection(request, action=''): # va tutto spostato in models
    args = {}
    args ={'section':'Intelligenza artificiale:', 'subsection': 'Riconoscimento facciale', 'imgsrc':'', 'rekog_imgsrc' : ''}
    args['imgsrc'] = ''
    if action =='analyze' and request.method == 'POST':
        args['filename'] = request.FILES.get('file_to_analyze', False)
        if args['filename'] == False:
            args['message'] = "Nessun file da analizzare"
            return render(request, 'ai.html', args)
        args['message'] = ""
        # Salva l'immagine nel server e tiene conto del percorso per la visualizzazione
        fs = FileSystemStorage()
        fs.save(args['filename'].name, args['filename'])
        args['imgsrc'] = 'media/'+args['filename'].name
        # Rileva il percorso assoluto per leggere l'immagine da processare
        abs_image_path =  os.path.join(conf_settings.MEDIA_ROOT , args['filename'].name)
        result = face_detector(abs_image_path, args['filename'].name) # Processa l'immagine
        args['items'] = result['items'] # Lista di elementi riconosciuti
        args['n_items'] = result['n_items'] # Numero di elementi riconosciuti
        args['rekog_imgsrc'] =  'media/'+result['rekog_filename']
        fs = None
        #-----------------------------------------------------------------------------------------------
        return render(request, 'ai.html', args)
    else:
        args['message'] = "Nessun file da analizzare"
        return render(request, 'ai.html', args)
            

