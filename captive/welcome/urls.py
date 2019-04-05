# howdy/urls.py
from django.conf.urls import url
from welcome import views
from django.conf.urls import include
from django.contrib.auth.views import login


urlpatterns = [
    url(r'^welcome/wifiadmin/admin.html', views.AdminView.as_view(), name='admin_users'),
    url(r'^welcome/accounts/', include('django.contrib.auth.urls')),
    url(r'^welcome/wifiadmin/[enable|disable]', views.AdminManageView.as_view(), name='admin_manage_users'),
    url(r'^welcome/emergency', views.EmergencyAccessView.as_view(), name='admin_manage_users'),
    url(r'^welcome/wifiadmin/', views.AdminView.as_view(), name='admin_users'),
    url(r'^welcome', views.HomePageView.as_view(), name='welcome'),
    url(r'^about', views.AboutPageView.as_view()), # Add this /about/ route
    url(r'^ajax$', views.ajax, name='validate_username'),
    ]
