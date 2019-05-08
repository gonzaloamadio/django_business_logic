# -*- coding: utf-8 -*-
"""Concrete implementations of the interfaces.

This implementations will do operations on the database, it will call
the ORM. So it can be easily changed if we need to operate on a different
type of database.
"""
from django.core.exceptions import ObjectDoesNotExist

from posts.models import Job

from .interfaces import JobRepositoryInterface


class JobRepository(JobRepositoryInterface):
    """Implementation of the interface that define operations over the database."""

    def find(self, uuid: 'UUID') -> Job:  # noqa: T484, F821
        """Find a Job given the uuid.

        ``find(self, uuid: 'UUID') -> Job``

        Args:
            uuid (UUID): primary key of the object that we want to retrieve.

        Returns:
            Job: The job founded.

        """
        return self._find({'uuid': uuid})

    #    def find_by(self, username: str) -> Job:
    #        elem = self._find({'username': username})
    #        return self._factory(elem)

    def create(self, **kwargs) -> Job:
        """Create a new Job. Calls Django ORM.

        ``create(self, **kwargs) -> Job``

        Args:
            kwargs (dict): Dictionary with field names as keys, and values that
            wants to be assigned.

        Returns:
            Job: Job created

        """
        return Job.objects.create(**kwargs)

    def get_or_create(self, **kwargs) -> Job:
        """Get or Create a new Job. Calls Django ORM.

        Args:
            kwargs (dict): Dictionary with field names as keys, and values that
            wants to be assigned.

        Returns:
            Job: Job created

        """
        return Job.objects.get_or_create(**kwargs)

    def factory(self, **kwargs) -> Job:
        """Get a Job class with data provided in the parameters.

        This function will not create a Job in the databasse, will only instantiate
        a new Job()

        Args:
            kwargs (dict): Dictionary with field names as keys, and values that
            wants to be assigned to the instance.
        """
        return self._factory(**kwargs)

    def save(self, instance: Job) -> Job:
        """Save an instance of a Job.

        ```save(self, instance: Job) -> Job```

        Args:
            instance (Job): Instance thats going to be saved to DB.

        Returns:
            Job: The Job instance after being saved.

        """
        return instance.save()

    def update_fields(self, instance: Job, fields: dict) -> Job:
        """Update some fields on a Job instance.

        ``update_fields(self, instance: Job, fields: list) -> Job``

        Only the fields named in that list will be updated. This may be desirable
        if you want to update just one or a few fields on an object.
        There will be a slight performance benefit from preventing all of the
        model fields from being updated in the database.

        Usage Example:
            product.name = 'Name changed again'
            product.save(update_fields=['name'])

        Args:
            instance (Job) : Instance to be updated
            fields (list)  : List of fields to be updated

        Returns:
            Job: Instance of the job after being updated.

        """
        for attr, val in fields.items():
            setattr(instance, attr, val)
        return instance.save(update_fields=fields.keys())

    def _factory(self, **kwargs) -> Job:
        """Return an instance of a Job class with parameters provided."""
        return Job(**kwargs)

    def _find(self, params: dict) -> Job:
        """Find a Job given some field values.

        ``_find(self, params: dict) -> Job``

        Args:
            params (dict): primary key of the object that we want to retrieve.

        Returns:
            Job or None: The job founded or None if not Job matches.

        """
        try:
            ret = Job.objects.get(**params)
        except ObjectDoesNotExist:
            return None
        else:
            return ret


#    def update_status(self, job: Job) -> Job:
#        elem = self._find({'uuid': job.uuid})
#        elem.is_active = elem.active
#        elem.save()
