from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('ci', views.CiView.as_view(), name='lac-ci'),
    path('ciloc', views.CilocView.as_view(), name='lac-ciloc'),
]