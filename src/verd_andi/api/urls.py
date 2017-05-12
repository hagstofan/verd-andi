from django.conf.urls import url

from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    url(r'^$', views.ItemList.as_view()),
    url(r'^observer-items/(?P<pk>[0-9]+)/update$',views.ItemObserverUpdateAPIView.as_view()),
    url(r'^observer-items/(?P<pk>[0-9]+)/destroy$',views.ItemObserverDestroyAPIView.as_view()),
]
