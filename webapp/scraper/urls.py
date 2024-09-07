from django.urls import path
from .views import home, specialized_bikes

urlpatterns = [
    path('', home, name='home'),
    path('specialized', specialized_bikes, name='specialized_bikes'),
]
