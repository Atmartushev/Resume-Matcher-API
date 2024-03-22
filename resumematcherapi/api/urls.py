from django.urls import path
from . import views

urlpatterns = [
    path('user', views.getAllUsers),
    path('user/<int:id>', views.getUser),
    path('user/add', views.addUser)
]