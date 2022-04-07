from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

# Assigning a Reference to a function to a URL
urlpatterns = [
    path('', views.homepage),
    path('clear', views.reset_session, name="clear"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
