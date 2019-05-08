# -*- coding: utf-8 -*-
"""Interfaes of operations on the database.

Basically this file will contain only interfaes, implemented by the adapters.
All operations must be implemented.
"""
import abc

from posts.models import Job


class JobRepositoryInterface(metaclass=abc.ABCMeta):
    """Abstract class for adapters."""

    @abc.abstractmethod
    def find(self, uuid: 'UUID') -> Job:
        """Find a Job given the uuid.

        ``find(self, uuid: 'UUID') -> Job``

        Args:
            uuid (UUID): primary key of the object that we want to retrieve.

        Returns:
            Job: The job founded.

        """
        pass

    #    @abc.abstractmethod
    #    def find_by(self, username: str) -> Job:
    #        pass

    @abc.abstractmethod
    def create(self, **kwargs) -> Job:
        """Create a new Job. Calls Django ORM.

        ``create(self, **kwargs) -> Job``

        Args:
            kwargs (dict): Dictionary with field names as keys, and values that
            wants to be assigned.

        Returns:
            Job: Job created

        """
        pass

#    @abc.abstractmethod
#    def update_status(self, credential: str) -> CredentialInterface:
#        pass

    @abc.abstractmethod
    def get_or_create(self, **kwargs) -> Job:
        """Get or Create a new Job. Calls Django ORM.

        Args:
            kwargs (dict): Dictionary with field names as keys, and values that
            wants to be assigned.

        Returns:
            Job: Job created

        """
        pass

    @abc.abstractmethod
    def factory(self, **kwargs) -> Job:
        """Get a Job class with data provided in the parameters.

        This function will not create a Job in the databasse, will only instantiate
        a new Job()

        Args:
            kwargs (dict): Dictionary with field names as keys, and values that
            wants to be assigned to the instance.
        """
        pass

    @abc.abstractmethod
    def save(self, instance: Job) -> Job:
        """Save an instance of a Job.

        ```save(self, instance: Job) -> Job```

        Args:
            instance (Job): Instance thats going to be saved to DB.

        Returns:
            Job: The Job instance after being saved.

        """
        pass

    @abc.abstractmethod
    def update_fields(self, instance: Job, fields: dict) -> Job:
        """Update some fields on a Job instance.

        ``update_fields(self, instance: Job, fields: dict) -> Job``

        Args:
            instance (Job) : Instance to be updated
            fields (dict)  : {key:new_value} dict, with fields and new values.

        Returns:
            Job: Instance of the job after being updated.

        """
        pass
