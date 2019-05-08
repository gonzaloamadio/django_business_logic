# -*- coding: utf-8 -*-
"""Concentrate the heavy business logic of the operations of an application.

It knows all Models that should be part of the flow and knows
the API/services of those models. It also orchestrate all the side-effects
and therefore can make the use of other use cases/services.
"""
from django.utils.translation import gettext as _

from payments_comissions.models import PaymentComission
from posts.models import Job
from posts_areas.models import PostArea
from tektank.internal_services.use_case_interface import UseCaseInterface
from tektank.libs_project.helpers import slug_generator

from .errors import InvalidCategories, InvalidDateOrder
from .interfaces import JobRepositoryInterface


class CreateJob(UseCaseInterface):
    """Create Job service.

    Service layer for the creation of a Job. Here we are going to do all
    validations and side effects. We are going to always use this service
    instead of calling the Models create method directly.

    We combine validations here, and validators in the model itself.

    Input:
        Parameters of Job model, i.e. its fields.
        repository : A class that will operate against the DB,
                    or any other source to get/put information.

    Raises:
        InvalidCategories
        InvalidDateOrder

    Returns:
        Instance of Job created.
    """

    def __init__(
        self,
        repository: JobRepositoryInterface,
        title,
        email,
        date_start,
        date_end,
        amount_to_pay,
        avatar=None,
        company=None,
        city=None,
        state=None,
        country=None,
        postal_code=None,
        post_category=None,
        post_subcategory=None,
        address=None,
        phone=None,
        cellphone=None,
        description=None,
        terms=None,
        deleted=False,
        slug=None,
    ):
        """

        We can instantiate like
        CreateJob('title','email@gmail.com',date1,date2,
            ** { "address" : " 123 street ","description ":"This is a descr"}
        So we are providing mandatory fields, and rest that we want to set.

        Fields: slug and payment_comission does not appear, because they are
            set by us. It is not an user input.
        """
        # -- Set the internal state of the model for the operation
        # The fields listed here, should match with the ones defined in the
        # model definition. And also with only one _ before the field name.
        self._title = title
        self._email = email
        self._date_start = date_start
        self._date_end = date_end
        self._amount_to_pay = amount_to_pay
        self._avatar = avatar
        self._company = company
        self._city = city
        self._state = state
        self._country = country
        self._postal_code = postal_code
        self._post_category = post_category
        self._post_subcategory = post_subcategory
        self._address = address
        self._phone = phone
        self._cellphone = cellphone
        self._description = description
        self._terms = terms
        # Forces None, as we set them
        self._slug = None
        self._payment_comission = None
        self._deleted = deleted
        # ----- Other objects ----- #
        self.__obj = None
        self.__repository = repository
        # A list of keys defined in the model. If model is modified, we should
        # also modify this.
        self.__model_keys = [
            'title',
            'email',
            'date_start',
            'date_end',
            'amount_to_pay',
            'avatar',
            'company',
            'city',
            'state',
            'country',
            'postal_code',
            'post_category',
            'post_subcategory',
            'address',
            'phone',
            'cellphone',
            'description',
            'terms',
            'slug',
            'deleted',
            'payment_comission',
        ]

    @property
    def repository(self) -> JobRepositoryInterface:
        """Return the respository (adapter) used."""
        return self.__repository

    def execute(self) -> Job:
        """Main operation, the one that be executed by external code. This
        operation will condense the rest. Will execute side effects, and
        all required operations in order.
        """
        self._strip_data()
        # Create an instance of Job, and save it into self.__obj
        self._factory()
        self.is_valid()
        self.__obj.slug = self._generate_slug(  # noqa: T484
            self.__obj.id, self.__obj.title,  # noqa: T484
        )
        self.__obj.payment_comission = self._generate_payment_comission(  # noqa: T484
            self.__obj.amount_to_pay,  # noqa: T484
        )
        self.__repository.save(self.__obj)
        return self.__obj

    def _strip_data(self):
        """Clean fields. For example, delete trailing spaces."""
        fields = [
            "title",
            "address_1",
            "address_2",
            "email",
            "website",
            "phone",
            "cellphone",
        ]
        for field in fields:
            value = getattr(self, field, None)
            if value:
                setattr(self, field, value.strip())

    def is_valid(self):
        """Public method to allow clients of this object to validate the data even before to execute the use case.

        To use it, create an instance of the class with the values desired.
        And execute it.

        Returns:
            True or False

        Raises:
            ValidationError, InvalidDateOrder, InvalidCategories
        """

        # ## Check date order

        if self._date_end and self._date_start and self._date_end <= self._date_start:
            raise InvalidDateOrder(_("Start date should be before end date"))

        # ## Check categories match.

        # TODO: This should not be necessary, but in admin
        # dropdown menu for selecting categories are not well filtered when selecting parent
        # categorie, so we need to do it.
        # TODO: Send ID instead of name for better lookup
        # TODO: This logic would go inside posts_category services
        if self._post_category:
            assert isinstance(
                self._post_category, str
            ), "Category name should be a string"
        if self._post_subcategory:
            assert isinstance(
                self._post_subcategory, str
            ), "Subcategory name should be a string"
        # If user selected both categories, check that the parent is the correct
        # If only subcategory selected, fill the right parent.
        # If only category, do nothing.
        cat = (
            PostArea.objects.find_by_name(self._post_category)
            if self._post_category
            else None
        )
        subcat = (
            PostArea.objects.find_by_name(self._post_subcategory)
            if self._post_subcategory
            else None
        )
        if subcat:
            if cat and subcat.parent != cat:
                raise InvalidCategories(cat.name, subcat.name)
            else:
                self._post_category = subcat.parent.name

        # Here at the end, as before this, we were cleaning and validating all
        # fields, so it has sense that at this point, the model will be in the
        # final state.
        # If object is not stored locally, do it.
        if not self.__obj:
            self._factory()
        # ## Execute programatically model validations. Raises validation error.
        self.__obj.full_clean()

        return True

    def _generate_slug(self, uuid, title):
        """Generate slug for the instance."""
        return slug_generator(uuid, title)

    def _generate_payment_comission(self, amount_to_pay):
        """Assign an instance to PaymentComission related to this model.

        This assignment will later dictated how we are going to charge this
        job.
        The rules of how we are going to calculate this, are done by us.
        """
        return PaymentComission.assign_payment_comission(amount_to_pay)

    def _factory(self):
        """Create an instance of a Job, and save it into self.__obj."""
        # Check if it is a field in the model # TODO do it better?

        # Remove _ from keys, so we pass correct arguments to create,
        # and leave only values that are not None.
        def process(s):
            if s[0] == '_' and s[1] != '_' and s[1:] in self.__model_keys:
                return s[1:]

        params = {
            process(k): v
            for k, v in self.__dict__.items()
            if v is not None and process(k)
        }
        self.__obj = self.__repository.factory(**params)
