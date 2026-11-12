from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalogo/', views.ProductoListView.as_view(), name='catalogo'),
]
