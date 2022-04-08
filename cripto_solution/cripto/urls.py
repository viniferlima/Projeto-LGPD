from django.urls import path

from . import views

urlpatterns = [
    path('newUser', views.add_new_user, name='index'),
    path('DeleteUser', views.delete_user, name='index'),
]