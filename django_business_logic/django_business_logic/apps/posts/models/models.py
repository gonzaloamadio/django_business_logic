# -*- coding: utf-8 -*-
"""Models representing posts, now only jobs."""
from django.contrib.postgres.indexes import BrinIndex
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from tektank.libs.models import AuditedModel, PersistentModel, UUIDPrimaryKey


class PostModel(UUIDPrimaryKey, AuditedModel):
    """Abstract model with basic info of a post.

    ``class PostModel(UUIDPrimaryKey, AuditedModel)``

    Composed by the following fields:

    .. _PostModel:

    +------------------+-----------------------+-------+-----------------------------------------------------------+
    | Field Name       |       Type            | Null  |                 Comments                                  |
    +==================+=======================+=======+===========================================================+
    | title            | Charfield(128)        |  No   |   Title of the post, ad or whatever will this represent   |
    +------------------+-----------------------+-------+-----------------------------------------------------------+
    | email            |  EmailField           |  No   |   Email of contact (maybe it is not the same as user email|
    +------------------+-----------------------+-------+-----------------------------------------------------------+
    | avatar           |  ImageField           |  Yes  |  Image for the post                                       |
    +------------------+-----------------------+-------+-----------------------------------------------------------+
    | company          | FK(entities.Company)  |  No   | Company that posted this                                  |
    +------------------+-----------------------+-------+-----------------------------------------------------------+
    | city             | FK(cities.City)       |  Yes  |  City where the job is held (if any)                      |
    +------------------+-----------------------+-------+-----------------------------------------------------------+
    | state            | FK(cities.Region)     |  Yes  |  Region where the job is held (if any)                    |
    +------------------+-----------------------+-------+-----------------------------------------------------------+
    | country          | FK(cities.Country)    |  Yes  |  Country where the job is held (if any)                   |
    +------------------+-----------------------+-------+-----------------------------------------------------------+
    | postal_code      | FK(cities.PostalCode) |  Yes  |  PC where the job is helled (if any)                      |
    +------------------+-----------------------+-------+-----------------------------------------------------------+
    | post_category    |FK(posts_areas.PostArea|  Yes  |  Category this post belongs to                            |
    +------------------+-----------------------+-------+-----------------------------------------------------------+
    | post_subcategory |FK(posts_areas.PostArea|  Yes  |  Sub Category this post belongs to                        |
    +------------------+-----------------------+-------+-----------------------------------------------------------+
    | payment_comission|FK(payments_comissions.|  Yes  |  Rate of comission payed to us. It will be autocalculated |
    |                  | PaymentComission)     |       |  depending on the amount. Despite it can be null, it will |
    |                  |                       |       |  never be, or must never be. So when a transaction is     |
    |                  |                       |       |  taken we can earn the comission. Anyway there will be    |
    |                  |                       |       |  check                                                    |
    +------------------+-----------------------+-------+-----------------------------------------------------------+
    | date_start       | DateTimeField         |  No   |  Date that this post/job starts                           |
    +------------------+-----------------------+-------+-----------------------------------------------------------+
    | date_end         | DateTimeField         |  No   |  Date that this post/job ends                             |
    +------------------+-----------------------+-------+-----------------------------------------------------------+
    | address          | CharField(128)        |  Yes  |  Address, if any, where the job is carried out            |
    +------------------+-----------------------+-------+-----------------------------------------------------------+
    | phone            | CharField(32)         |       |  Phone contact number, fixed line                         |
    +------------------+-----------------------+-------+-----------------------------------------------------------+
    | cellphone        | CharField(32)         |       |  Mobile Phone contact number                              |
    +------------------+-----------------------+-------+-----------------------------------------------------------+
    | description      | TextField(512)        |       |  Mobile Phone contact number                              |
    +------------------+-----------------------+-------+-----------------------------------------------------------+
    | terms            | TextField(512)        |       |  Mobile Phone contact number                              |
    +------------------+-----------------------+-------+-----------------------------------------------------------+
    | amount_to_pay    | PositiveSmallInt      |       |  Amount to pay fot the job                                |
    +------------------+-----------------------+-------+-----------------------------------------------------------+
    | slug             | SlugField             |       |  Slug field. Always overwriten when model is saved. It is |
    |                  |                       |       |  formed like "<title[:128]>-<hashed pk>"                  |
    +------------------+-----------------------+-------+-----------------------------------------------------------+

    """

    title = models.CharField(max_length=128, db_index=True, verbose_name=_("title"))
    email = models.EmailField(verbose_name=_("email"))
    avatar = models.ImageField(
        verbose_name=_("avatar"), blank=True, null=True, upload_to="avatars",
    )
    company = models.ForeignKey(
        "entities.Company",
        on_delete=models.SET_NULL,
        verbose_name=_("company"),
        null=True,
        blank=True,
        db_index=False,
    )
    city = models.ForeignKey(
        "cities.City",
        on_delete=models.SET_NULL,
        verbose_name=_("city"),
        null=True,
        blank=True,
        db_index=False,
    )
    state = models.ForeignKey(
        "cities.Region",
        on_delete=models.SET_NULL,
        verbose_name=_("region"),
        null=True,
        blank=True,
        db_index=False,
    )
    country = models.ForeignKey(
        "cities.Country",
        on_delete=models.SET_NULL,
        verbose_name=_("country"),
        null=True,
        blank=True,
        db_index=False,
    )
    postal_code = models.ForeignKey(
        "cities.PostalCode",
        on_delete=models.SET_NULL,
        verbose_name=_("postal code"),
        null=True,
        blank=True,
        db_index=False,
    )
    post_category = models.ForeignKey(
        "posts_areas.PostArea",
        on_delete=models.SET_NULL,
        verbose_name=_("post category"),
        null=True,
        blank=True,
        related_name="+",
        db_index=False,
    )  # related_name with + --> no backward relations
    post_subcategory = models.ForeignKey(
        "posts_areas.PostArea",
        on_delete=models.SET_NULL,
        verbose_name=_("post sub category"),
        null=True,
        blank=True,
        related_name="+",
        db_index=False,
    )
    payment_comission = models.ForeignKey(
        "payments_comissions.PaymentComission",
        on_delete=models.SET_NULL,
        verbose_name=_("comission"),
        null=True,
        blank=True,
        db_index=False,
    )

    date_start = models.DateTimeField(_("start date"))
    date_end = models.DateTimeField(_("end date"))

    address = models.CharField(
        max_length=128, db_index=True, verbose_name=_("adress"), null=True, blank=True,
    )
    phone = models.CharField(
        max_length=32, verbose_name=_("phone"), null=True, blank=True,
    )
    cellphone = models.CharField(
        max_length=32, verbose_name=_("mobile phone"), null=True, blank=True,
    )
    description = models.TextField(
        verbose_name=_("description"), max_length=512, blank=True,
    )
    terms = models.TextField(verbose_name=_("terms"), max_length=512, blank=True)

    amount_to_pay = models.PositiveSmallIntegerField(_("amount to pay to tester"))
    # Only for readability, post get will be still by ID (Url will be /id/slug)
    # This will come from the urls.py
    slug = models.SlugField(
        verbose_name=_("slug"), max_length=151, null=True, blank=True,
    )

    # Payment data
    # TODO: Complete

    class Meta:
        abstract = True
        get_latest_by = ["created_at", "updated_at"]
        indexes = (
            # NOT FK Fields
            BrinIndex(fields=["created_at"]),
            BrinIndex(fields=["updated_at"]),
            BrinIndex(fields=["date_start"]),
            BrinIndex(fields=["date_end"]),
            models.Index(fields=["amount_to_pay"]),
            # FK Fields
            models.Index(fields=["postal_code"]),
            models.Index(fields=["city"]),
            models.Index(fields=["state"]),
            models.Index(fields=["country"]),
            models.Index(fields=["company"]),
            models.Index(fields=["post_category"]),
            models.Index(fields=["post_subcategory"]),
            models.Index(fields=["payment_comission"]),
        )

    def __str__(self):
        return self.title

    def clean(self, *args, **kwargs):
        """Strip whitespaces."""
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

    # This will come from the urls.py
    def get_absolute_url(self):
        """Return absolute url for a post element."""
        return reverse("v1:posts-detail", kwargs={"slug": self.slug})


class Job(PostModel, PersistentModel):
    """Proposal of jobs.

    This model represents a company posting a job  that
    needs to be done, a product to be tested.

    Inherit from `PostModel`_
    """

    class Meta:
        verbose_name = _("job")
        verbose_name_plural = _("jobs")
        app_label = 'posts'

    def get_absolute_url(self):
        """Return absolute url for a job element."""
        return reverse("v1:posts-job-detail", kwargs={"slug": self.slug})
