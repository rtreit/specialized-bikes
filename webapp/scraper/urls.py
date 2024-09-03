from django.urls import path
from .views import home, scrape_specialized

urlpatterns = [
    path('', home, name='home'),
    path('specialized', scrape_specialized, name='scrape_specialized'),
]
