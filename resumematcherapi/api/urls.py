from django.urls import path
from . import views

urlpatterns = [
    path('user', views.getAllUsers),
    path('user/id/<int:id>', views.getUser),
    path('user/email/<str:email>', views.getUserByEmail),
    path('user/add', views.addUser)
]