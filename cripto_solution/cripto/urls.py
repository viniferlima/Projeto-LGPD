from django.urls import path

from . import views

urlpatterns = [
    path('insert_user', views.add_new_user, name='index'),
    path('delete_user/<str:cpf>', views.delete_user, name='index'),
    path('old_sales', views.all_data_insert_sale, name='index'),
    path('find_user/<str:cpf>',views.find_user, name='index'),
]