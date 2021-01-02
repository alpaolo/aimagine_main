from dataclasses import dataclass
from PIL import Image, ImageDraw, ExifTags, ImageColor
import os

@dataclass
class Img ():
    rel_source : str = ''
    abs_source : str = ''
    width : int = 0
    height : int = 0
    byte_array : list = []



    def read(self, filepath) :
        with open(filepath, 'rb') as image:
            self. byte_array = image.read()


