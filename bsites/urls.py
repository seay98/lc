from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView, name='index'),
    path('cis', views.CisView, name='lac-cis'),
    path('cild', views.CildView, name='lac-cild'),
    path('lacs', views.LacsView, name='lac-lacs'),
    path('ci', views.CiView.as_view(), name='lac-ci'),
    path('ciloc', views.CilocView.as_view(), name='lac-ciloc'),
    path('cil/<int:pk>', views.CilView.as_view(), name='lac-cil'),
    path('lacr/<int:pk>', views.LacrView.as_view(), name='lac-lacr'),
]