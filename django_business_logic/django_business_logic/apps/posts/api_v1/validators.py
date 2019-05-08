# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from rest_framework.serializers import ValidationError

from tektank.libs.validators import OtherFieldValidatorInSerializer


class EndDateValidator(OtherFieldValidatorInSerializer):
    """Check that start date is before end date.

    ``class EndDateValidator(OtherFieldValidatorInSerializer)``

    The class inherit from the validator that check some condition between to
    fields. So we have to implement the make_validation function.
    """

    def make_validation(self, field, other_field):
        """Implement the validation. Check that one date field is before another."""
        date_end = field
        date_start = other_field
        if date_start and date_end and date_end < date_start:
            raise ValidationError(
                _('End date cannot be before start date.'), code='invalid_model_data',
            )
