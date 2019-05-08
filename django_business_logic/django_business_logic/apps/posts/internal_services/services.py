# -*- coding: utf-8 -*-
"""Exported services to use in the rest of the code, and maybe from other apis.

This file will be the one that will contain the "public" operations
on the model.
The rest of the code should use this, or a usecase if required for some reason
of how exceptions are handled.

With "public" we mean that this file contains all the functinos that can be
called from the rest of the code or from outside.

EVERY OPERATION on the model should go through this services. As here is
where all the validations are made.
"""
from typing import Any, Dict, Tuple

from django.core.exceptions import ValidationError

from .adapters import JobRepository
from .errors import Error as JobError
from .usecases import CreateJob

# Instead of Any, should be Job. But if we return more things, I left Any
RetDict = Dict[str, Any]
RetValue = Tuple[str, RetDict]


class CreateJobService:
    """Service that creates a new job.

    It executes a concrete use case.

    Basically there will be a one 2 one correspondence between a service
    and a use case (where all the heavy lifting will be)
    """

    def create_job(self, *args, **kwargs) -> RetValue:
        """Concrete execution of the service, create a Job.

        Args:
            kwargs should contain all (at least required) parameters in Job model

        Returns:
            A tuple containing a string with any errors and a dic with the job created.

        Raises:
            Errors are captured and listed into the return tuple, on the first component.
            So this does not raises exceptions (or should not).

        """
        errors = []
        ret_data = {}
        repository = JobRepository()
        try:
            usecase = CreateJob(repository, **kwargs)
            new_job = usecase.execute()
        except (JobError, ValidationError) as err:
            errors.append(str(err))
        else:
            ret_data.update({'data': new_job})
        return ','.join(errors), ret_data
