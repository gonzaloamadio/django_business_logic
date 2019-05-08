"""File with combination of classes to inherit in our apps"""
from rest_framework import mixins, viewsets

class APIViewSet(
        viewsets.GenericViewSet,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin,
):
    pass


