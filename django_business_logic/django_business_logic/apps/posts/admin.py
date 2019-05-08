# -*- coding: utf-8 -*-
from django.contrib import admin

from posts_areas.models import PostArea
from tektank.libs.admin import ExportCsvMixin

from . import models


class JobAdmin(admin.ModelAdmin, ExportCsvMixin):
    """Admin definition for posts model."""

    # actions = ["export_as_csv","mark_as_deleted"]
    actions = ["export_as_csv"]
    exclude = ('slug',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filter dropdown menus, to show only related entries."""
        if db_field.name == "post_category":
            kwargs["queryset"] = PostArea.objects.filter(parent__isnull=True)
        if db_field.name == "post_subcategory":
            kwargs["queryset"] = PostArea.objects.exclude(parent__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


#    def mark_as_deleted(self, request, queryset):
#        queryset.update(deleted=True)
#    mark_as_deleted.short_description = "Mark as deleted"

admin.site.register(models.Job, JobAdmin)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
