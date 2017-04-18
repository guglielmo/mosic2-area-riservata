# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url

# load admin modules
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

import views
from views import SedutaCIPEViewSet, SedutaPreCIPEViewSet, FileUploadView

admin.autodiscover()

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'cipe', SedutaCIPEViewSet, base_name='cipe')
router.register(r'precipe', SedutaPreCIPEViewSet, base_name='precipe')


urls = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^upload_file/(?P<filename>.+)$', FileUploadView.as_view(), name='upload-file'),
    url(r'^seduta/(?P<tipo>[^/]+)/(?P<id_seduta>.+)$', views.SedutaView.as_view(), name='url-seduta'),
    url(r'^api-token-auth/', obtain_jwt_token, name='obtain-jwt'),
    url(r'^api-token-refresh/', refresh_jwt_token, name='refresh-jwt'),
    url(r'^seduta-precipe/(?P<hash>[^/]+)$', views.PublicView.as_view(), name='seduta-precipe' ),
    url(r'^seduta-cipe/(?P<hash>[^/]+)$', views.PublicView.as_view(), name='seduta-cipe' ),
    url(r'^403$', views.TemplateView.as_view(template_name="403.html"), name='tampering-403'),
]
urlpatterns = urls

# static and media urls with DEBUG = True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns.append(
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )

