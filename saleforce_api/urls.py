"""saleforce_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from home_resource.views import home
from tmc_access_resource import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home, name='home'),
    url(r'^activate_tmc_form', views.activate_form, name='activate_tmc_form'),
    url(r'^activate_tmc', views.activate, name='activate_tmc'),
    url(r'^query_activation_form', views.query_activation_form, name='query_activation_form'),
    url(r'^query_activation', views.query_activation, name='query_activation'),
]
