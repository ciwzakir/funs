from xml.dom.minidom import Document
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('altandexp.urls'))
] + static(settings.MEDIA_URL, Document_root= settings.MEDIA_ROOT)
