# -*- coding: utf-8 -*-
"""Api views for this app.

Viewsets are going to be implemented in this files. All views that are going to
be exposed and called. We are going to mantain it quite simple, as all the heavy
lifting is going to be done by the internal services.
"""
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.response import Response

from posts.api_v1.serializers import ActiveJobSerializer, JobSerializer
from posts.models import ActiveJob, Job
from tektank.libs.views import APIViewSet


class ActiveJobFilter(filters.FilterSet):
    """Filters for the ActiveJobViewSet.

    This class defines the filters that can be applied when querying the Viewset.

    For a list of the urls generated, or filters that can be applied, check for
    the tests, or doc.
    """

    min_payment = filters.NumberFilter(field_name="amount_to_pay", lookup_expr="gte")
    max_payment = filters.NumberFilter(field_name="amount_to_pay", lookup_expr="lte")
    title = filters.CharFilter(lookup_expr='icontains')
    post_category = filters.CharFilter(
        lookup_expr='icontains', field_name='post_category__name',
    )
    post_subcategory = filters.CharFilter(
        lookup_expr='icontains', field_name='post_subcategory__name',
    )

    class Meta:  # noqa: D106
        model = ActiveJob
        fields = [
            "title",
            "company",
            "city",
            "postal_code",
            "post_category",
            "post_subcategory",
            "min_payment",
            "max_payment",
        ]


class JobViewSet(APIViewSet):
    """Viewset for Job model.

    This viewset will be called when creating or updating new jobs.

    Create function is overwritten so we can perform the operation through the
    serializer, and call our own business logic declared in the internal services.

    The lookup field for a particular job is the slug generated, and not
    the id straightforward.

    Implements:
        create, update, retrieve, delete, list
    """

    queryset = Job.objects.all()
    serializer_class = JobSerializer
    lookup_field = "slug"

    def create(self, request, *args, **kwargs):
        """Create a new Job. Called when posting a new Job.

        Overwrite of the default create function, so we can call our custom logic
        defined in our internal services. With this we are trying to mantain the
        models and the views thing, and concentrate all the heavy lifting in the
        services.

        Returns:
            A Response object with the data of the object created (if succesfull),
            the status of the operation.

        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers,
        )

    def perform_create(self, serializer):
        """Call the serializer save method and maybe do something else."""
        serializer.save()


class ActiveJobViewSet(APIViewSet):
    """Viewset for ActiveJob model. So Jobs that are elegibles to apply (active).

    This viewset will be called when listing or retrieving jobs.

    The lookup field for a particular job is the slug generated, and not
    the id straightforward.

    Implements:
        Retrieve, List
    """

    queryset = ActiveJob.objects.all()
    serializer_class = ActiveJobSerializer
    lookup_field = "slug"
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ActiveJobFilter
