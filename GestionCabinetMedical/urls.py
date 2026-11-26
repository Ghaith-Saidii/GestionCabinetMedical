from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import permission_required
from django.urls import path
from django.views.generic import RedirectView
from django.views.static import serve


urlpatterns = [
    path("", RedirectView.as_view(pattern_name="admin:index")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    @permission_required("AppointmentApp.view_appointment", raise_exception=True)
    def serve_prescription(request, filename):
        return serve(request, filename, document_root=settings.MEDIA_ROOT / "prescriptions")

    urlpatterns.append(
        path(f"{settings.MEDIA_URL.lstrip('/')}prescriptions/<str:filename>", serve_prescription)
    )
