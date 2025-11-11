from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from home.views import home, handle_upload
from home import views
urlpatterns = [
    path('', home, name='home'),
    path('handle/', handle_upload, name='handle_upload'),
    path('admin/', admin.site.urls),
    path('upload/', views.handle_upload, name='handle_upload'),
    path('download/<str:filename>/', views.download_zip, name='download_zip'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    # This serves files uploaded by users (media files)
    
    
    # This serves your static files (CSS, JavaScript, images)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
