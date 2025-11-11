from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from home.views import home, handle_upload, download_zip

urlpatterns = [
    path('', home, name='home'),
    path('upload/', handle_upload, name='handle_upload'),
    path('handle/', handle_upload, name='handle_upload'),
    path('download/<str:filename>/', download_zip, name='download_zip'),
    path('admin/', admin.site.urls),
]

# Serve static files (Render needs this)
urlpatterns += staticfiles_urlpatterns()

# ✅ DO NOT SERVE MEDIA IN PRODUCTION — FileResponse handles download
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
