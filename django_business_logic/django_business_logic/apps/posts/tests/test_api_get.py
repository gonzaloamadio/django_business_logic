# -*- coding: utf-8 -*-
import json
from datetime import timedelta

import factory
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

# To create fake data
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from posts.api_v1.serializers import JobSerializer
from posts.models import ActiveJob, Job
from tektank.libs_project.helpers import slug_generator

# initialize the APIClient app
client = APIClient()


faker = Factory.create()


class JobFactory(factory.DjangoModelFactory):
    class Meta:
        model = Job

    title = faker.word()
    email = faker.email()
    date_start = timezone.now()
    date_end = timezone.now() + timedelta(hours=3)
    amount_to_pay = faker.random_number(1, 100)


class ActiveJobFactory(factory.DjangoModelFactory):
    class Meta:
        model = ActiveJob

    title = faker.word()
    email = faker.email()
    date_start = timezone.now()
    date_end = timezone.now() + timedelta(hours=3)
    amount_to_pay = faker.random_number(1, 100)


class GetJobTest(TestCase):
    """ Test module for GET all Jobs API """

    @classmethod
    def setUpTestData(cls):  # noqa: N802
        cls.a = JobFactory(title="mock")
        cls.b = JobFactory()
        cls.c = JobFactory()
        cls.url_list = "v1:posts-job-list"
        cls.url_detail = "v1:posts-job-detail"

    def test_get_all_jobs(self):
        # get API response
        response = client.get(reverse(self.url_list))
        # get data from db
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        self.assertEqual(response.data.get("data"), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(json.loads(response.content).get('data')) == Job.objects.count())

    def test_get_valid_job(self):
        # Creamos un job (Y le creamos el slug, xq no estamos usando el
        # services.py)
        from django.utils import timezone
        from datetime import timedelta

        aware_start = timezone.now()
        aware_end = timezone.now() + timedelta(hours=3)
        job = Job.objects.create(
            title="my faked title",
            date_start=aware_start,
            date_end=aware_end,
            amount_to_pay=10,
            email='fake@gmail.com',
        )
        slug = slug_generator(job.id, job.title)
        job.slug = slug
        job.save()
        # Lo traemos con la api
        response = client.get(reverse(self.url_detail, kwargs={"slug": slug}))
        # Lo traemos desde la base
        a = Job.objects.get(pk=job.pk)
        serializer = JobSerializer(a)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_job(self):
        # A slug with random string, just in case
        slug = "inexistent-slug-43y4832y482hfsh"
        response = client.get(reverse(self.url_detail, kwargs={"slug": slug}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetActiveJobTest(TestCase):
    """ Test module for GET all ActiveJobs API """

    @classmethod
    def setUpTestData(cls):  # noqa: N802
        #cls.a = ActiveJobFactory(title="mock")
        #cls.b = ActiveJobFactory()
        cls.url_list = "v1:posts-activejob-list"
        cls.url_detail = "v1:posts-activejob-detail"

    def test_get_all_jobs(self):
        # get API response
        response = client.get(reverse(self.url_list))
        # get data from db
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        self.assertEqual(response.data.get("data"), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_job(self):
        # Creamos un job (Y le creamos el slug, xq no estamos usando el
        # services.py)
        from django.utils import timezone
        from datetime import timedelta

        aware_start = timezone.now()
        aware_end = timezone.now() + timedelta(hours=3)
        job = Job.objects.create(
            title="my faked title",
            date_start=aware_start,
            date_end=aware_end,
            amount_to_pay=10,
            email='fake@gmail.com',
        )
        slug = slug_generator(job.id, job.title)
        job.slug = slug
        job.save()
        # Lo traemos con la api
        response = client.get(reverse(self.url_detail, kwargs={"slug": slug}))
        # Lo traemos desde la base
        a = Job.objects.get(pk=job.pk)
        serializer = JobSerializer(a)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_job_because_of_slug(self):
        # A slug with random string, just in case
        slug = "inexistent-slug-43y4832y482hfsh"
        response = client.get(reverse(self.url_detail, kwargs={"slug": slug}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_invalid_job_because_it_is_old(self):
        # Creamos un job (Y le creamos el slug, xq no estamos usando el
        # services.py)
        from django.utils import timezone
        from datetime import timedelta

        aware_start = timezone.now() - timedelta(hours=4)
        aware_end = timezone.now() - timedelta(hours=3)
        job = Job.objects.create(
            title="my faked title",
            date_start=aware_start,
            date_end=aware_end,
            amount_to_pay=10,
            email='fake@gmail.com',
        )
        slug = slug_generator(job.id, job.title)
        job.slug = slug
        job.save()
        # Lo traemos con la api
        response = client.get(reverse(self.url_detail, kwargs={"slug": slug}))
        # Lo traemos desde la base
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
