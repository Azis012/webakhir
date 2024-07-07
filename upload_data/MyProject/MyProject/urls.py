from django.contrib import admin
from django.urls import path, include
from UploadFiles import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.base, name="base"),
    path('add', views.home, name="home"),
    path('view', views.view, name="view"),
    path('uploadfile', views.uploadfile, name="uploadfile"),
    path('deleteFile/<int:id>', views.deleteFile, name="deleteFile"),  # Ensure correct naming here
    path('csv/<int:id>/', views.csv_details, name='csv_details'),
    path('update/<int:id>/', views.update_file, name='update_file'),
    path('api/', include('UploadFiles.urls')),
    path('request/', views.dataset_details, name='request'),
    path('update-dataset-status/<int:dataset_id>/', views.update_dataset_status, name='update_dataset_status'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
