from django.conf.urls import url

from . import views

# survey urls

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^$', views.SurveyListView.as_view(), name='survey-list'),
    url(r'(?P<pk>[0-9]+)/$', views.SurveyDetailView.as_view(), name='survey-detail'),
]
