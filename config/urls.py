from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.views.generic import TemplateView
import os

def health_check(request):
    return JsonResponse({'status': 'ok', 'message': 'API is running'})

def frontend_view(request):
    """Serve the frontend HTML file"""
    frontend_path = os.path.join(settings.BASE_DIR, 'frontend.html')
    if os.path.exists(frontend_path):
        with open(frontend_path, 'r', encoding='utf-8') as f:
            from django.http import HttpResponse
            return HttpResponse(f.read(), content_type='text/html')
    return JsonResponse({'error': 'Frontend not found'}, status=404)

urlpatterns = [
    path('', frontend_view, name='frontend'),
    path('admin/', admin.site.urls),
    path('api/health/', health_check),
    path('api/', include('apps.ml_inference.urls')),
    path('api/auth/', include('apps.accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
