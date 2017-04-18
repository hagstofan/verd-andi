"""verd_andi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin
from perap.views import home


urlpatterns = [
	url(r'^$', home, name='index'),
    url(r'^perap/', include('perap.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^nested_admin/', include('nested_admin.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^survey/', include('survey.urls')),
]
