# -*- coding: utf-8 -*-
"""Signals for posts model."""
from django.db.models.signals import pre_save
from django.dispatch import receiver

from posts.models import Job
from tektank.libs_project.helpers import slug_generator


# We leave the code just in case, but we are doing this in the save method.
# @receiver(pre_save, sender=Job)
def generate_slug(sender, instance, **kwargs):
    """Generate slug field. Slugifying the title and appending ",hashedid"."""
    # Always generate it
    instance.slug = slug_generator(instance)
