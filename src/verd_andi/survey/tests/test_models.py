# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
# from django.conf import settings

from survey.models import (
    Survey,
    )


class SurveyModelTest(TestCase):

    def test_survey_str_function(self):
        survey = Survey(code='abcd',
                        year=int(1997),
                        current=True,
                        dataflowID='pppMishmash')

        self.assertEqual(str(survey), "abcd-1997")
