# -*- coding: utf-8 -*-
from django.test import TestCase, Client, RequestFactory
from django.conf import settings
# from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from datetime import datetime
from datetime import timedelta

from survey.models import (
    Survey,
    Item,
    ItemCommentary,
    Characteristic,
    Observation,
    ObservedCharacteristic,
    UserObservation,
    ItemObserver
    )

from survey.views import (
    SurveyListView,
    SurveyDetailView,
    )


class SurveyDetailViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.survey = Survey(
            id=int(1),
            code='abcd',
            year=int(1997),
            current=True,
            dataflowID='pppMishmash'
            )
        Survey.objects.create(id=int(1),
                              code='abcd',
                              year=int(1997),
                              current=True,
                              dataflowID='pppMishmash')

    def _call_survey_detail_view(self, user):
        user = User.objects.filter(is_superuser=True).first()
        kwargs = {'pk': self.survey.id}
        request = self.factory.get(reverse('survey:survey-detail'),
                                   kwargs=kwargs)
        request.user = user
        return SurveyDetailView.as_view()(request)

    def test_survey_detail_response(self):
        print(self.survey.id)
        self.assertEqual('fart', 'fart')
        # user = User.objects.filter(is_superuser=True).first()
        request = self.factory.get(reverse('survey:survey-detail',
                                           kwargs={'pk': self.survey.id}))
        response = SurveyDetailView.as_view()(request, pk=self.survey.id)
        self.assertEqual(response.status_code, 200)
