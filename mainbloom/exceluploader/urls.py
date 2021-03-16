from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^excel-upload$', views.Excel.as_view()),
    url(r'^home$', views.Home.as_view()),
]
