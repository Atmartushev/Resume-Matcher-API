from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.getUser),
    path('user/id/', views.addUser),
]