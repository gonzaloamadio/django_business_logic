# -*- coding: utf-8 -*-
import json
from datetime import timedelta

import factory
from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

# To create fake data
from faker import Factory
from rest_framework import status
from rest_framework.test import (
    APITestCase,
)  # Inherit from this and self.client will be APIClient()

from posts.api_v1.serializers import ActiveJobSerializer, JobSerializer
from posts.models import ActiveJob, Job
from tektank.libs_project.helpers import slug_generator

faker = Factory.create()


class JobFactory(factory.DjangoModelFactory):
    """Creation of a valid Job, all required fields and good format"""

    class Meta:
        model = Job

    title = faker.word()
    email = faker.email()
    date_start = timezone.now()
    date_end = timezone.now() + timedelta(hours=3)
    amount_to_pay = faker.random_number(1, 100)


#    slug = 'asd'


class JobFactoryInvalid(factory.DjangoModelFactory):
    """Invalid Job: date_end < date_start"""

    class Meta:
        model = Job

    title = faker.word()
    email = faker.email()
    date_start = timezone.now()
    date_end = timezone.now() - timedelta(hours=3)
    amount_to_pay = faker.random_number(1, 100)


class JobFactoryInvalid2(factory.DjangoModelFactory):
    """Invalid Job: no date_start"""

    class Meta:
        model = Job

    title = faker.word()
    email = faker.email()
    date_end = timezone.now() + timedelta(hours=3)
    amount_to_pay = faker.random_number(1, 100)


class PostJobTest(APITestCase):
    """ Test module for POST to Jobs API

        We inherit from APITestCase, so in self.client we cave APIClient()
        Test creation of jobs
    """

    # def setUpTestData(self):
    def setUp(self):
        self.url = reverse("v1:posts-job-list")
        # Convert a factory's output to a dict.
        self.data_valid = factory.build(dict, FACTORY_CLASS=JobFactory)
        self.data_invalid = factory.build(dict, FACTORY_CLASS=JobFactoryInvalid)

    #        self.a = JobFactory(title="mock")
    #        self.b = JobFactory()
    #        self.c = JobFactory()
    #        self.d = JobFactory()

    def test_post_valid_job(self):
        response = self.client.post(self.url, self.data_valid)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_invalid_job(self):
        response = self.client.post(self.url, self.data_invalid)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # This two next code lines are not true, it does't raises validation err.
        # It returns 400 BAD REQUEST and inside response.data we have something
        # like  this:
        # (Pdb) response.data
        # {'title': [ErrorDetail(string='Title cannot be only numbers', code='invalid')]}
        #        with self.assertRaises(ValidationError):
        #            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data_invalid2 = factory.build(dict, FACTORY_CLASS=JobFactoryInvalid2)
        response = self.client.post(self.url, data_invalid2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
