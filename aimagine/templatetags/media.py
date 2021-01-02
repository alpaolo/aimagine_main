from django import template 
from django.conf import settings as conf_settings

register = template.Library() 

@register.simple_tag(name='media')
def media(filename): 
    return "/media/"+filename