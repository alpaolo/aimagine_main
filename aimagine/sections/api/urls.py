from django.urls import path
from django.http import HttpResponse
from django.conf.urls import url
from django.conf import settings as settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import api_v1_views


urlpatterns = [
    path('', lambda request: HttpResponse('Is the api index page')),
    path('v1', api_v1_views.test, name='apiv1test'),
    path('v1(?P<action>\w+)/$', api_v1_views.test, name='apiv1test'),
    path('v1/blur', api_v1_views.yolo_faceblur, name='apiv1yolofaceblur'),
 
    
    #path('imagerecognition/(?P<action>\w+)/$', views.process, name='process'),

] 

# Serving the media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#else: urlpatterns += staticfiles_urlpatterns()
else: urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)