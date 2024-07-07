from django.db import models
import pandas as pd
from django.utils import timezone

from django.db import models
import pandas as pd
from django.utils import timezone

class MyFileUpload(models.Model):
    file_name = models.CharField(max_length=50)
    my_file = models.FileField(upload_to='csv/')
    creator_name = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateField(default=timezone.now)
    project_id = models.CharField(max_length=50, null=True, blank=True)  # Tambahkan field ini
    project_name = models.CharField(max_length=255, null=True, blank=True)  # Tambahkan field ini

    def read_csv(self):
        file_path = self.my_file.path
        df = pd.read_csv(file_path)
        return df


from django.db import models

class Dataset(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=100, default='Belum selesai')

    def __str__(self):
        return self.name

class Column(models.Model):
    dataset = models.ForeignKey(Dataset, related_name='columns', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    data_type = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.data_type})"
