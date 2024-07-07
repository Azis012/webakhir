import requests
from django.shortcuts import redirect, render, get_object_or_404
from .forms import MyFileForm
from .models import MyFileUpload
from django.contrib import messages
from rest_framework import generics
from .serializer import *
import os
from django.conf import settings
from django.views.decorators.http import require_POST

import matplotlib
matplotlib.use('Agg')  # Use the Anti-Grain Geometry backend
import matplotlib.pyplot as plt

class MyFileUploadList(generics.ListCreateAPIView):
    queryset = MyFileUpload.objects.all()
    serializer_class = MyFileUploadSerializer

def base(request):
    return render(request, 'base.html')

def home(request):
    mydata = MyFileUpload.objects.all()
    myform = MyFileForm()
    context = {'form': myform, 'mydata': mydata if mydata.exists() else None}
    return render(request, 'index.html', context)

def view(request):
    query = request.GET.get('q')
    if query:
        mydata = MyFileUpload.objects.filter(file_name__icontains=query)
    else:
        mydata = MyFileUpload.objects.all()
    myform = MyFileForm()

    # Fetching data from the external API
    api_url = 'http://172.16.1.130:8001/projects/'  # Ganti dengan endpoint API Anda
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        project_codes = response.json()  # Assuming the API returns a JSON response
    except requests.RequestException as e:
        project_codes = []
        messages.error(request, f"Error fetching project codes: {e}")

    # Create a mapping between project IDs and their names
    project_id_to_name = {project['project_id']: project['project_name'] for project in project_codes}

    context = {'form': myform, 'mydata': mydata if mydata.exists() else None, 'project_id_to_name': project_id_to_name, 'query': query}
    return render(request, 'view.html', context)

def fetch_project_name(project_id):
    api_url = f'http://172.16.1.130:8001/projects/{project_id}/'
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        project_data = response.json()
        return project_data.get('project_name', 'Unknown Project')
    except requests.RequestException as e:
        return f"Error fetching project name: {e}"


def uploadfile(request):
    if request.method == "POST":
        myform = MyFileForm(request.POST, request.FILES)
        if myform.is_valid():
            MyFileName = request.POST.get('file_name')
            MyFile = request.FILES.get('my_file')
            CreatorName = request.POST.get('creator_name')
            Status = request.POST.get('status')
            ProjectID = request.POST.get('project_id')

            ProjectName = fetch_project_name(ProjectID)

            exists = MyFileUpload.objects.filter(my_file=MyFile).exists()

            if exists:
                messages.error(request, 'The file %s already exists...!!!' % MyFile)
            else:
                file_instance = MyFileUpload.objects.create(file_name=MyFileName, my_file=MyFile, creator_name=CreatorName, status=Status, project_id=ProjectID, project_name=ProjectName)
                file_instance.save()
                messages.success(request, "File uploaded successfully.")
                return redirect("view")
        else:
            messages.error(request, "Form is not valid.")
            return redirect("home")

    return render(request, 'home.html', {'form': MyFileForm()})

def deleteFile(request, id):
    mydata = get_object_or_404(MyFileUpload, id=id)
    if mydata.my_file:
        try:
            os.remove(mydata.my_file.path)
        except FileNotFoundError:
            messages.warning(request, 'File not found.')
    mydata.delete()
    messages.success(request, 'File deleted successfully.')
    return redirect('view')

def csv_details(request, id):
    mydata = get_object_or_404(MyFileUpload, id=id)

    if not mydata.my_file:
        messages.error(request, "No file associated with this entry.")
        return redirect('view')  # Assuming 'view' is the name of your list view

    try:
        df = mydata.read_csv()
    except ValueError as e:
        messages.error(request, "Error reading the file: {}".format(e))
        return redirect('view')

    num_rows = df.shape[0]
    num_columns = df.shape[1]

    # Convert DataFrame to a list of lists, excluding the row index
    data_frame = [list(row) for row in df.itertuples(index=False)]
    columns = df.columns

    # Gather column statistics
    stats = {}
    for column in columns:
        stats[column] = {
            'unique': df[column].nunique(),
            'missing': df[column].isnull().sum(),
            'most_common': df[column].mode()[0] if not df[column].mode().empty else 'N/A',
            'mean': df[column].mean() if pd.api.types.is_numeric_dtype(df[column]) else 'N/A',
            'std': df[column].std() if pd.api.types.is_numeric_dtype(df[column]) else 'N/A',
            'min': df[column].min() if pd.api.types.is_numeric_dtype(df[column]) else 'N/A',
            'max': df[column].max() if pd.api.types.is_numeric_dtype(df[column]) else 'N/A',
        }

    # Generate histogram for the 'Harga' column
    image_path = None
    if 'Harga' in df.columns and pd.api.types.is_numeric_dtype(df['Harga']):
        plt.figure(figsize=(10, 6))
        df['Harga'].dropna().plot(kind='hist', bins=30, edgecolor='k', alpha=0.7)
        plt.title('Histogram of Harga')
        plt.xlabel('Harga')
        plt.ylabel('Frequency')
        plt.grid(True)
        image_filename = f'histogram_{id}.png'
        static_images_dir = os.path.join(settings.BASE_DIR, 'static', 'images')
        os.makedirs(static_images_dir, exist_ok=True)
        image_path = os.path.join(static_images_dir, image_filename)
        plt.savefig(image_path)
        plt.close()
        image_path = os.path.join('images', image_filename)

    context = {
        'file_name': mydata.file_name,
        'num_rows': num_rows,
        'num_columns': num_columns,
        'columns': columns,
        'data_frame': data_frame,
        'stats': stats,
        'image_path': image_path
    }
    return render(request, 'csv_details.html', context)

def update_file(request, id):
    file_instance = get_object_or_404(MyFileUpload, id=id)
    if request.method == 'POST':
        form = MyFileForm(request.POST, request.FILES, instance=file_instance)
        if form.is_valid():
            ProjectID = request.POST.get('project_id')
            ProjectName = fetch_project_name(ProjectID)
            file_instance.project_id = ProjectID
            file_instance.project_name = ProjectName
            form.save()
            messages.success(request, 'File details updated successfully.')
            return redirect('view')
    else:
        form = MyFileForm(instance=file_instance)

    return render(request, 'update_file.html', {'form': form, 'file_instance': file_instance})

@require_POST
def update_dataset_status(request, dataset_id):
    new_status = request.POST.get('status')
    try:
        response = requests.patch(f'http://172.16.1.130:8001/datasetss/{dataset_id}/', data={'status': new_status})
        response.raise_for_status()
        messages.success(request, "Status updated successfully.")
    except requests.RequestException as e:
        messages.error(request, f"Error updating status: {e}")

    return redirect('request')

def dataset_details(request):
    try:
        response = requests.get('http://172.16.1.130:8001/datasetss')
        response.raise_for_status()
        mydata = response.json()
    except requests.RequestException as e:
        mydata = []
        messages.error(request, f"Error fetching datasets: {e}")

    # Mendapatkan status dari MyFileUpload
    file_status_mapping = {file.file_name: file.status for file in MyFileUpload.objects.all()}

    for dataset in mydata:
        dataset_name = dataset.get('nama_dataset')
        dataset['status'] = file_status_mapping.get(dataset_name, 'Belum Selesai')

    context = {'mydata': mydata, 'file_status_mapping': file_status_mapping}
    return render(request, 'request.html', context)
