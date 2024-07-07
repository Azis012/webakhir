from rest_framework import serializers
from .models import *

class MyFileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyFileUpload
        fields = '__all__'
