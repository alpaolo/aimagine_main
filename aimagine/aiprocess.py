
from . recog import detect_labels_local_file, getphoto
from django.conf import settings as conf_settings
from pathlib import Path
from PIL import Image, ImageDraw, ExifTags, ImageColor, ImageEnhance
import os
import boto3

def face_detector(abs_imagepath, filename): # va tutto spostato in models
        # Rileva il percorso assoluto per leggere l'immagine da processare
        items = []
        client=boto3.client('rekognition')
        with open(abs_imagepath, 'rb') as image:
            items = client.detect_faces(Image={'Bytes': image.read()})['FaceDetails']
        # Carica l'immagine in pillow e disegna ( Per ottimizzare si potrebbe usare il byte array )
        im = Image.open(abs_imagepath)
       
        imgWidth, imgHeight = im.size 
        enhancer = ImageEnhance.Brightness(im)
        enhanced_im = enhancer.enhance(0.4)
        draw = ImageDraw.Draw(enhanced_im)  
        for faceDetail in items:
            box = faceDetail['BoundingBox']
            left = imgWidth * box['Left']
            top = imgHeight * box['Top']
            width = imgWidth * box['Width']
            height = imgHeight * box['Height']        
            draw.rectangle([left,top, left + width, top + height], outline='#ffff00')
            cropped_im =  im.crop((left, top, left+width, top+height))
            enhanced_im.paste(cropped_im,(int(left), int(top)))
        # Costruisce il nome ed il percorso per la visualizzazione sul server     
        rekog_filename =  'rekog_' + filename
        rekog_filepath = os.path.join(conf_settings.MEDIA_ROOT , rekog_filename)
        enhanced_im.save(rekog_filepath)
        im = None
        enhanced_im = None
        #-----------------------------------------------------------------------------------------------
        return {'items':items, 'n_items':len(items), 'rekog_filepath' : rekog_filepath, 'rekog_filename' : rekog_filename}



