# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PostsConfig(AppConfig):
    """Config for this app."""
    name = 'posts'
    verbose_name = _('posts')


#    def ready(self):
#        import posts.signals  # noqa: F401
