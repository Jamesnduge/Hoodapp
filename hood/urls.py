from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as authviews

urlpatterns = [
    url('^$',views.home, name='home'),
    url(r'^profile/(?P<username>\w+)/$', views.profile, name='profile'),
    url(r'^profile/bio/(?P<username>\w+)/$', views.profile_bio, name='bio'),
    url(r'^profile/business/(?P<username>\w+)/$', views.profile_business, name='business'),
    url(r'^ajax/business/$', views.new_business, name='new_business'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)