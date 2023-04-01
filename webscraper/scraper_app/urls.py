from django.urls import path
from . import views

urlpatterns = [
    path('scrape/', views.scrape, name='scrape'),
    path('', views.scrape, name='scrape'),
]