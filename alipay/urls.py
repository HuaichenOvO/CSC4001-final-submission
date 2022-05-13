from django.urls import path
from . import views
urlpatterns=[
  path('',views.index,name='index'),
  path('bill1/',views.bill1,name='bill1'),
  path('bill2/',views.bill2,name='bill2'),
  path('bill3/',views.bill3,name='bill3'),
  path('show/',views.show,name='show'),
  path('check/',views.check,name='check'),
]