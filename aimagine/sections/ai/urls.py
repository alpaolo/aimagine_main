from django.urls import path, re_path
from django.http import HttpResponse
from django.conf.urls import url
from django.conf import settings as settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import face_detection_views


urlpatterns = [
    path('', lambda request: HttpResponse('Is the ai index page')),
    path('tracking/', face_detection_views.person_track, name='iaawspersontracker'),
    re_path('tracking/(?P<action>\w+)/$', face_detection_views.person_track, name='iapersontracker'),
    path('facedetection/', face_detection_views.aws_face_detection, name='iaawsfacedetection'),
    re_path('facedetection/(?P<action>\w+)/$', face_detection_views.aws_face_detection, name='iaawsfacedetection'),
    
    #path('imagerecognition/(?P<action>\w+)/$', views.process, name='process'),

] 

# Serving the media files in development mode

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#else: urlpatterns += staticfiles_urlpatterns()
else: urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)