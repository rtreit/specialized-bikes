from django.urls import path
from .views import scrape_specialized

urlpatterns = [
    path('specialized', scrape_specialized, name='scrape_specialized'),
]
