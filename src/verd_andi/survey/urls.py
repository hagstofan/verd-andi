from django.conf.urls import url

from . import views

# survey urls

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^$', views.SurveyListView.as_view(), name='survey-list'),
    url(r'^obs/(?P<id>[\w{}.-]{1,40})/$', views.survey_dash, name='survey-observation'),
    url(r'(?P<pk>[0-9]+)/$', views.SurveyDetailView.as_view(), name='survey-detail'),
    url(r'^udash/', views.user_dash, name='survey-userdash'),

]
