from django.urls import path
from . import views

urlpatterns = [
    path('myfeed/', views.myfeed, name='myfeed'),
    path('myfeed2/', views.myfeed2, name='myfeed2'),
    path('myfeed3/', views.myfeed3, name='myfeed3'),
]
