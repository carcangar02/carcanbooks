from django.urls import path
from . import views

app_name = 'carcanbooks'  # para usar namespace en templates o reverses

urlpatterns = [
    path('', views.librerias_menu, name='librerias_menu'),
    # path('libro/<str:libro.titulo>/', views.libro_details, name='libro_details'),

]
