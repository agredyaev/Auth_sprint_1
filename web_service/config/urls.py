from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from movies.views import health_check

urlpatterns = [
    path("admin/", admin.site.urls),
    path("healthcheck/", health_check, name="health-check"),
    path("api/", include("movies.api.urls")),
    path("v1/", include("movies.api.v1.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
