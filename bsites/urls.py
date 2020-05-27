from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('ic', views.IcView.as_view(), name='lac-ic'),
]