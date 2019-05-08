# -*- coding: utf-8 -*-
"""Serializers for posts app."""
from rest_framework import serializers

# from django.core.exceptions import ValidationError
from rest_framework.serializers import ValidationError

from posts.models import ActiveJob, Job
from tektank.libs.serializers import AuditedModelSerializer

from ..internal_services.services import CreateJobService


class JobSerializer(serializers.ModelSerializer):
    """Serializer of Job model.

    .. _JobSerializer

    Serializer of job model. We define the lookup field as the slug field.
    Also overwrite CRUD methods that are used in the view to create instances,
    so instead of the default operations, we use our own business logic
    declared inside internal_services.

    Args:
        Request data for instance (json dic).

    Returns:
        Object _Job created or data serialized if it used to request data.

    Raises:
        ValidationError
    """
    post_category = serializers.StringRelatedField()
    post_subcategory = serializers.StringRelatedField()

    class Meta:
        model = Job
        fields = '__all__'
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}

    def create(self, validated_data):
        """Overwrite serializer create method to use our business logic.

        Args:
            Request data for instance.

        Returns:
            Object _Job created or data serialized if it used to request data.

        Raises:
            ValidationError
        """
        # User services to operate, not manager straight
        service = CreateJobService()
        error, ret = service.create_job(**validated_data)
        if error:
            raise ValidationError(error, code='invalid_model_data')
        else:
            return ret.get('data')


class ActiveJobSerializer(serializers.ModelSerializer):
    """Serializer of Active Job model.

    Same as `JobSerializer`_, but for the proxy model ActiveJob.
    So the set returned will be filtered by Active jobs, i.e. jobs that are
    elegible to applied for.

    Should be only used for retrieving info, not to create or update.
    """
    post_category = serializers.StringRelatedField()
    post_subcategory = serializers.StringRelatedField()

    class Meta:
        model = ActiveJob
        fields = '__all__'
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}


class JobSerializerAdmin(AuditedModelSerializer):
    """Serializer to use as an admin, with all fields."""
    class Meta:
        model = Job
        fields = '__all__'
