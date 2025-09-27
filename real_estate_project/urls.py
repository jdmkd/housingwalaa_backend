from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from real_estate_project import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path("api/accounts/", include("accounts.urls")),
    path("api/locations/", include("locations.urls")),
    path("api/properties/", include("properties.urls")),
    path("api/inquiries/", include("inquiries.urls")),
    path("api/promotions/", include("promotions.urls")),


]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)