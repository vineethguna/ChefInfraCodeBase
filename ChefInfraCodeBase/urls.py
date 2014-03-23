from django.conf.urls import patterns, include, url
from django.contrib import admin
from app import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ChefInfraCodeBase.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/$', include(admin.site.urls)),
    url(r'^$', views.index, name='index page'),
    url(r'^onprem/$', views.on_prem_index, name='On Prem Homepage'),
    url(r'^cloud/$', views.cloud_index, name='Cloud Homepage'),
    url(r'^onprem/create/$', views.create_on_prem_deployment, name='On Prem Deployment Creation'),
    url(r'^cloud/create/$', views.create_cloud_deployment, name='Cloud Deployment Creation'),
    url(r'^onprem/handle_deploy/$', views.handle_on_prem_deployment, name='Handle On Prem Deployment'),
    url(r'^cloud/handle_deploy/$', views.handle_cloud_deployment, name='Handle Cloud Deployment')
)
