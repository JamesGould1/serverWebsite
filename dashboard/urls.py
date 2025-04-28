from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.custom_login, name='login'),   
    path("", views.index, name="index"),
    path('start/<str:server_name>/', views.start_server, name='start_server'),
    path('stop/<str:server_name>/', views.stop_server, name='stop_server'),  # if you have stop
]
