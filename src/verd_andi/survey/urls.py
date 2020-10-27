from django.conf.urls import url

from . import views

# survey urls
app_name = 'survey'

urlpatterns = [
    url(r'^done-observation-pictures/(?P<idx>[0-9]+)/$', views.DoneUpload, name="done-observation-picture"),
    url(r'^observation-picture/(?P<idx>[0-9]+)/$', views.UploadView.as_view(), name="observation-picture"),
    url(r'^observer-items/(?P<idx>[0-9]+)/$',
        views.ObserverItems, name='observer-items'),
    url(r'^collector-comment/(?P<idx>[\w{}.-]{1,40})/'
        '(?P<uname>[\w{}.-]{1,40})/$',
        views.CollectorCommentView, name='collector-comment'),
    url(r'^observation/(?P<idx>[0-9]+)/$',
        views.ObservationUpdate, name='observation-update'),
    url(r'^observation-view/(?P<idx>[0-9]+)/$',
        views.viewObservation, name='observation-view'),
    url(r'^observation/(?P<pk>[0-9]+)/delete/',
        views.ObservationDelete.as_view(), name='observation-delete'),
    url(r'^$', views.SurveyListView.as_view(), name='survey-list'),
    url(r'^item-obs/(?P<idx>[\w{}.-]{1,40})/$',
        views.item_observation, name='item-observation'),
    url(r'^udash/', views.user_dash, name='survey-userdash'),
    url(r'^search/(?P<pk>[0-9]+)/$',
        views.search, name='survey-search'),
    url(r'^survey-detail/(?P<pk>[0-9]+)/$', views.SurveyDetailView.as_view(),
        name='survey-detail'),
    url(r'^itemcommentary/(?P<idx>[\w{}.-]{1,40})/$',
        views.ItemCommentaryView, name='item-commentary-edit'),
    url(r'^observers-management/',
        views.ObserversManagement, name='observers-management'),
    url(r'(?P<pk>[0-9]+)/xml/', views.SurveyXML, name='survey-xml'),
    url(r'^item-observations/(?P<idx>[\w{}.-]{1,40})/$',
        views.prev_item_observations, name='item-observations'),
]
