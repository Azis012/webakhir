from django.urls import path
from .views import MyFileUploadList

urlpatterns = [
    path('files/', MyFileUploadList.as_view(), name='api-file-upload'),
]
