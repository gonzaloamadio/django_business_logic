# -*- coding: utf-8 -*-
"""Test of usecase CreateJob"""
import uuid
from datetime import timedelta
from unittest.mock import patch

import factory
import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from django_mock_queries.query import MockSet

# To create fake data
from faker import Factory

import tektank.libs_project.shortuuid as _su
from posts.models import Job
from posts.internal_services.adapters import JobRepository
from posts.internal_services.errors import InvalidCategories, InvalidDateOrder
from posts.internal_services.usecases import CreateJob
from posts_areas.models import PostArea

faker = Factory.create()

# ------------------------------------------------------------------------------
# |                  Test Creation, actual creation                            |
# ------------------------------------------------------------------------------

class JobFactory(factory.DjangoModelFactory):
    class Meta:
        model = Job

    title = faker.word()
    email = faker.email()
    date_start = timezone.now()
    date_end = timezone.now() + timedelta(hours=3)
    amount_to_pay = faker.random_number(1, 100)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        if 'id' in kwargs.keys():
            kwargs.pop('id')
        return CreateJob(JobRepository(), **kwargs).execute()


class JobCreationTest(TestCase):
    """
        Test creation of Job model, but using directly the models method. So only
        validations declared in the definition of the model are taken into account.
        The service module is the one that we are going to use to create Jobs, so
        that is the one that should be tested completely.
    """

    def setUp(self, **kwargs):
        self.start = timezone.now()
        self.end = timezone.now() + timedelta(hours=3)

    def test_simple_creation(self):
        import datetime
        import pytz

        aware_start = datetime.datetime(2011, 8, 15, 8, 15, 12, 0, pytz.UTC)
        aware_end = datetime.datetime(2012, 8, 15, 8, 15, 12, 0, pytz.UTC)
        Job.objects.create(
            title="my faked title",
            date_start=aware_start,
            date_end=aware_end,
            amount_to_pay=10,
            email='fake@gmail.com',
        )
        JobFactory()

    def test_job_field_not_modified_on_creation(self):
        import datetime
        import pytz

        aware_start = datetime.datetime(2011, 8, 15, 8, 15, 12, 0, pytz.UTC)
        aware_end = datetime.datetime(2012, 8, 15, 8, 15, 12, 0, pytz.UTC)
        j = JobFactory(
            title="my faked title",
            date_start=aware_start,
            date_end=aware_end,
            amount_to_pay=10,
            email='fake@gmail.com',
            slug='asd',
        )

        self.assertTrue(isinstance(j, Job))
        self.assertEqual(j.title, "my faked title")
        self.assertEqual(j.date_start, aware_start)
        self.assertEqual(j.date_end, aware_end)
        self.assertEqual(j.amount_to_pay, 10)
        self.assertEqual(j.email, 'fake@gmail.com')

    def test_creation(self):
        long_str = "this is ignored and this is one veeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeery long slug, it should be ignored, i guess this has more than 157 chars 123456789123456789123456789123456789"
        # Invalid slugs, long slugs, no slugs. Slug is autogenerated, so no
        # matter what we pass there, it should be ok
        self.assertTrue(JobFactory(slug="a/s"))
        self.assertTrue(JobFactory(slug="this is ignored"))
        self.assertTrue(JobFactory(slug=long_str))

        ### All failing cases ###

        # Title very long
        with self.assertRaises(ValidationError):
            self.assertTrue(JobFactory(title=long_str))
        # No email
        with self.assertRaises(ValidationError):
            # self.assertTrue(Job.objects.create(title=faker.word(),date_start = self.start,date_end= self.end,amount_to_pay = 10))
            self.assertTrue(JobFactory(email=None))
        # No date_start
        with self.assertRaises(ValidationError):
            self.assertTrue(JobFactory(date_start=None))
        # No date_end
        with self.assertRaises(ValidationError):
            self.assertTrue(JobFactory(date_end=None))
        # No amount_to_pay
        with self.assertRaises(ValidationError):
            self.assertTrue(JobFactory(amount_to_pay=None))


# ------------------------------------------------------------------------------
# |                 Test Execute , with mocked creation                        |
# ------------------------------------------------------------------------------

# def create_job(title, email, date_start, date_end, amount, **extra_fields):
def create_jobb(**kwargs):
    # mock for "create_job" method on the Job model
    # to avoind touching the database. Unit tests should not
    # touch databases :)
    return Job(**kwargs)


@patch.object(Job.objects, 'create', side_effect=create_jobb)
@patch.object(
    CreateJob, 'is_valid', return_value=True
)  # Tested with another test, assumes OK
class TestExecute(TestCase):
    # Test the execute method on Createjob service

    def setUp(self):
        # setup method will be executed on each test
        self.start = timezone.now()
        self.end = timezone.now() + timedelta(hours=3)
        self._use_case = CreateJob(
            JobRepository(),
            title='How to test a job creation',
            email='john.smith@example.com',
            date_start=self.start,
            date_end=self.end,
            amount_to_pay=20,
        )
        self._use_case2 = CreateJob(
            JobRepository(),
            title='How to test a job creation',
            email='john.smith@example.com',
            date_start=self.start,
            date_end=self.end,
            amount_to_pay=60,
        )

    def test_return_job_type(self, mock_is_valid, mock_create):
        # def test_return_job_type(self,mock_is_valid):
        result = self._use_case.execute()
        assert isinstance(result, Job)
        result = self._use_case2.execute()
        assert isinstance(result, Job)

    def test_create_job_title(self, mock_is_valid, mock_create):
        expected_result = 'How to test a job creation'
        res = self._use_case.execute()
        assert res.title == expected_result

    def test_create_job_email(self, mock_is_valid, mock_create):
        expected_result = 'john.smith@example.com'
        res = self._use_case.execute()
        assert res.email == expected_result

    def test_create_job_date_start(self, mock_is_valid, mock_create):
        expected_result = self.start
        res = self._use_case.execute()
        assert res.date_start == expected_result

    def test_create_job_date_end(self, mock_is_valid, mock_create):
        expected_result = self.end
        res = self._use_case.execute()
        assert res.date_end == expected_result

    def test_create_job_amount_to_pay(self, mock_is_valid, mock_create):
        res = self._use_case.execute()
        assert res.amount_to_pay == 20
        res = self._use_case2.execute()
        assert res.amount_to_pay == 60

    def test_create_job_payment_comission1(self, mock_is_valid, mock_create):
        res = self._use_case.execute()
        assert res.payment_comission.percentage == 10

    def test_create_job_payment_comission2(self, mock_is_valid, mock_create):
        res = self._use_case2.execute()
        assert res.payment_comission.percentage == 20


# ------------------------------------------------------------------------------
# |                       Test is_valid method                                 |
# ------------------------------------------------------------------------------

# Replace this searches so we do not hit database:
# cat = PostArea.objects.find_by_name(self._post_category) if self._post_category else None
def findbn(category):
    pa1 = PostArea(name='one')
    pa11 = PostArea(name='one-child', parent=pa1)
    pa2 = PostArea(name='two')

    if category == 'one':
        return pa1
    if category == 'two':
        return pa2
    if category == 'one-child':
        return pa11

#mocker.patch.object(PostArea.objects, 'find_by_name', side_effect=findbn)
@pytest.mark.django_db
@patch.object(PostArea.objects, 'find_by_name', side_effect=findbn)
class TestValidData:
    """ Test the is_valid method on RegisterUserAccount use case """

    def test_when_end_date_is_before_start_date(self, mock_find):

        with pytest.raises(InvalidDateOrder):
            use_case = CreateJob(
                JobRepository(),
                title='How to test a job creation',
                email='john.smith@example.com',
                date_start=timezone.now(),
                date_end=timezone.now() - timedelta(hours=1),
                amount_to_pay=20,
            )

            # We give an empty to is_valid, because it takes a dict with the params,
            # but it does not need it in this case
            use_case.is_valid()

    def test_when_categories_do_not_match(self, mock_find):
        """Test that if we select categories that not match, it fails"""

        # Assrert that we raise the correct error
        with pytest.raises(InvalidCategories):
            use_case = CreateJob(
                JobRepository(),
                title='How to test a job creation',
                email='john.smith@example.com',
                date_start=timezone.now(),
                date_end=timezone.now() + timedelta(hours=1),
                amount_to_pay=20,
                post_category='one',
                post_subcategory='two',
            )
            # We give {} to is_valid, because it takes a dict with the params,
            # but it does not need it in this case
            use_case.is_valid()

    @pytest.mark.django_db
    def test_when_title_is_too_long(self, mock_find):

        with pytest.raises(ValidationError):
            title = 'How to test a job creationsssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo'
            email = 'john.smith@example.com'
            date_start = timezone.now()
            date_end = timezone.now() + timedelta(hours=1)
            amount_to_pay = 20
            dic = {
                'title': title,
                'email': email,
                'date_end': date_end,
                'date_start': date_start,
                'amount_to_pay': amount_to_pay,
            }
            use_case = CreateJob(
                JobRepository(),
                title=title,
                email=email,
                date_start=date_start,
                date_end=date_end,
                amount_to_pay=amount_to_pay,
            )

            use_case.is_valid()