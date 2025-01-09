from django.urls import path
from . import views

urlpatterns = [
    path('base/', views.Ask_model_view, name='ask_model.html'),
    path('send_info/', views.Send_data, name='send_data.html'),
]
