from django.conf.urls import url

from . import views

# survey urls
app_name = 'survey'

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^$', views.SurveyListView.as_view(), name='survey-list'),
    url(r'^obs/(?P<id>[\w{}.-]{1,40})/$', views.survey_dash, name='survey-observation'),
    url(r'^item-obs/(?P<idx>[\w{}.-]{1,40})/$', views.item_observation, name='item-observation'),
    url(r'^udash/', views.user_dash, name='survey-userdash'),
    url(r'^search/(?P<pk>[0-9]+)/$', views.search, name='survey-search'),
    url(r'(?P<pk>[0-9]+)/$', views.SurveyDetailView.as_view(), name='survey-detail'),
]
