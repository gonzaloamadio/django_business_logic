# -*- coding: utf-8 -*-
"""Proxy models to implement heavy logic in them. Manager and queryset so methods are chainable."""
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from tektank.libs.models import PersistentModelManager, PersistentModelQuerySet

from .models import Job


class ActiveJobQuerySet(PersistentModelQuerySet):
    """Extends PersistentModelQuerySet for the ActiveJob proxy model.

    Methods that we will be able to call from an ActiveJob manager.
    As we are declairing here in the overriden QuerySet (and we have to call
    them from the actual manager, we can chain them.
    For example if we have method1 and method2, we will be able to call

    ActiveJob.objects.method1().method2()

    For achieving that, we have to call this methods from the manager.
    """

    def great_payed(self):
        return self.filter(amount_to_pay__gt=50)

    def no_great_payed(self):
        return self.filter(amount_to_pay__lt=50)


class ActiveJobManager(PersistentModelManager):
    """Extends PersistentModelManager for the ActiveJob proxy model.

    Manager asignable to an ActiveJob model.
    We will define the same methods as in the QuerySet, and the only thing
    this methods will do will be calling the queryset methods.

    See code for examples/explanation.
    """

    def get_queryset(self):
        return ActiveJobQuerySet(self.model, using=self._db).filter(
            date_end__gt=timezone.now(),
        )

    def great_payed(self):
        return self.get_queryset().great_payed()

    def no_great_payed(self):
        return self.get_queryset().no_great_payed()


class ActiveJob(Job):
    """Job proxy model.

    Job proxy model, to filter active (not expired) jobs.
    Active jobs will be the ones that the end date it's after the actual date
    , i.e. now

    This model will NOT create a new table in the database.
    """

    # Assign manager to the model.
    objects = ActiveJobManager()

    class Meta:
        proxy = True
        verbose_name = _("active job")
        verbose_name_plural = _("active jobs")
        app_label = 'posts'

    def get_absolute_url(self):
        """Return absolute url for a job element."""
        return reverse("v1:posts-activejob-detail", kwargs={"slug": self.slug})
