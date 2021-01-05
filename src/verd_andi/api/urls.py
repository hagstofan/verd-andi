from django.conf.urls import url

from . import views
# from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'api'

urlpatterns = [
    url(r'^$', views.ItemList.as_view(), name='item-list'),
    url(r'^observer-items/(?P<pk>[0-9]+)/update$',
        views.ItemObserverUpdateAPIView.as_view()),
    url(r'^observer-items/(?P<pk>[0-9]+)/destroy$',
        views.ItemObserverDestroyAPIView.as_view(), name='obs-item-destroy'),
    url(r'^observer-items/create/',
        views.ItemObserverCreateAPIView.as_view(), name='obs-item-create'),
    url(r'^observations',
        views.ObservationList.as_view(), name='api-observation-list'),
]
