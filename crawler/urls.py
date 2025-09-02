from django.urls import path
from .views import URLRecordCreateView, URLRecordListView

urlpatterns = [
    path("urls/", URLRecordCreateView.as_view(), name="url-create"),   # POST
    path("urls/list/", URLRecordListView.as_view(), name="url-list"), # GET
]
