# -*- coding: utf-8 -*-
"""Urls definition for this app."""
from rest_framework.routers import DefaultRouter

from posts.api_v1 import views

# Create a router and register our viewsets with it.
# app_name = 'posts'
router = DefaultRouter()
router.register(r'jobs', views.JobViewSet, base_name="posts-job")
router.register(r'activejobs', views.ActiveJobViewSet, base_name="posts-activejob")
urlpatterns = router.urls
