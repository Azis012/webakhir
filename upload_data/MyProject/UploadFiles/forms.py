from django import forms
from .models import MyFileUpload, Dataset

class MyFileForm(forms.ModelForm):
    class Meta:
        model = MyFileUpload
        fields = ['file_name', 'my_file', 'creator_name', 'status', 'created_at', 'project_id', 'project_name']
        widgets = {
            'file_name': forms.TextInput(attrs={'class': 'form-control'}),
            'my_file': forms.FileInput(attrs={'class': 'form-control'}),
            'creator_name': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
            'created_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'project_id': forms.TextInput(attrs={'class': 'form-control'}),
            'project_name': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),  # Tambahkan read-only widget untuk project_name
        }


class DatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['name', 'description', 'status']