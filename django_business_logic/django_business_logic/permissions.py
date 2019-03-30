# -*- coding: utf-8 -*-
from rest_framework import permissions
from django.contrib.auth.models import User


# class IsOwnerOrReadOnly(permissions.BasePermission):
class IsDjangoUser(permissions.BasePermission):
    """
    Custom permission to only allow django users to read actions.
    Dejamos solo a usuarios de django, ya que solamente van a ser usuarios de django
    la gente de la muni. El resto de los usuarios comunes, solo estan en las tablas.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        #if request.method in permissions.SAFE_METHODS:
        #    return True

        # Write permissions are only allowed to the owner of the snippet.
        #return obj.owner == request.user

        try:
            user = User.objects.get(username=request.user.username)
            return True
        except User.DoesNotExist:
            return False

