
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
# noinspection PyUnresolvedReferences
from manageportal.views import contact_view

urlpatterns = [
                  path('admincontroller/', admin.site.urls),
                  path('', include('pages.urls')),
                  path('managesmartmarket/', include('manageportal.urls')),
                  path('contact/', contact_view, name='contact'),
                  path('accounts/', include('django.contrib.auth.urls')),
              ]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
