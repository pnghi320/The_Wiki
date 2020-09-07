from django.contrib import admin
from django.urls import path, include
from . import views
app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:entryName>', views.getEntry, name="getEntry"),
    path('search', views.search, name="search"),
    path('createPage', views.createPage, name="createPage"),
    path('editPage', views.editPage, name = "editPage"),
    path('saveEditedPage', views.saveEditedPage, name = "saveEditedPage"),
    path('randomPage', views.randomPage, name ="randomPage")
]
