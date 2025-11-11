import os
import zipfile
from django.shortcuts import render
from django.http import JsonResponse, FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.urls import reverse


@csrf_exempt
def handle_upload(request):
    if request.method != 'POST':
        return JsonResponse({'status': 405, 'message': 'Method not allowed'})

    files = request.FILES.getlist('files')

    if not files:
        return JsonResponse({'status': 400, 'message': 'No files uploaded'})

    # Correct upload folder
    folder_name = 'uploads'
    upload_path = os.path.join(settings.MEDIA_ROOT, folder_name)
    os.makedirs(upload_path, exist_ok=True)

    # Save uploaded files
    for file in files:
        with open(os.path.join(upload_path, file.name), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

    # Create ZIP file
    zip_folder = os.path.join(settings.MEDIA_ROOT, 'downloads')
    os.makedirs(zip_folder, exist_ok=True)

    zip_path = os.path.join(zip_folder, f"{folder_name}.zip")

    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in files:
            file_path = os.path.join(upload_path, file.name)
            zipf.write(file_path, arcname=file.name)

    # Generate proper download URL using reverse()
    download_url = request.build_absolute_uri(
        reverse('download_zip', args=[f"{folder_name}.zip"])
    )

    return JsonResponse({
        'status': 200,
        'message': 'Files uploaded and zipped successfully',
        'data': {
            'folder': folder_name,
            'download_url': download_url
        }
    })


def download_zip(request, filename):
    zip_path = os.path.join(settings.MEDIA_ROOT, 'downloads', filename)

    if not os.path.exists(zip_path):
        raise Http404("ZIP file not found")

    return FileResponse(open(zip_path, 'rb'), as_attachment=True)
    

def home(request):
    return render(request, 'home.html')
