from django.urls import path
from .views import crawl_url

urlpatterns = [
    path("crawl/", crawl_url, name="crawl_url"),
]
