from django.urls import path
from .views import home

# add url patterns for views here
urlpatterns = [
    path("", home, name="home"),
    path("tracker", home, name="home")
]
