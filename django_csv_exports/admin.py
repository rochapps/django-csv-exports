import csv

import pandas

import django
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse, HttpResponseForbidden
from builtins import str as text


def export_as_csv(admin_model, request, queryset):
    """
    Generic csv export admin action.
    based on http://djangosnippets.org/snippets/1697/
    """
    # everyone has perms to export as csv unless explicitly defined
    if getattr(settings, 'DJANGO_EXPORTS_REQUIRE_PERM', None):
        admin_opts = admin_model.opts
        codename = '%s_%s' % ('csv', admin_opts.object_name.lower())
        has_csv_permission = request.user.has_perm("%s.%s" % (admin_opts.app_label, codename))
    else:
        has_csv_permission = admin_model.has_csv_permission(request) \
            if (hasattr(admin_model, 'has_csv_permission') and callable(getattr(admin_model, 'has_csv_permission'))) \
            else True
    if has_csv_permission:
        opts = admin_model.model._meta
        if getattr(admin_model, 'csv_fields', None):
            field_names = admin_model.csv_fields
        else:
            field_names = [field.name for field in opts.fields]
            field_names.sort()

        if django.VERSION[0] == 1 and django.VERSION[1] <= 5:
            response = HttpResponse(mimetype='text/csv')
        else:
            response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % text(opts).replace('.', '_')

        queryset = queryset.values_list(*field_names)
        pandas.DataFrame(list(queryset), columns=field_names).to_csv(response, index=False, encoding='utf-8')
        return response
    return HttpResponseForbidden()
export_as_csv.short_description = "Export selected objects as csv file"


class CSVExportAdmin(admin.ModelAdmin):
    def get_actions(self, request):
        actions = super(CSVExportAdmin, self).get_actions(request)
        if self.has_csv_permission(request):
            actions['export_as_csv'] = (export_as_csv, 'export_as_csv', "Export selected objects as csv file")
        return actions

    def has_csv_permission(self, request, obj=None):
        """
        Returns True if the given request has permission to add an object.
        Can be overridden by the user in subclasses. By default, we assume
        all staff users can use this action unless `DJANGO_EXPORTS_REQUIRE_PERM`
        is set to True in your django settings.
        """
        if getattr(settings, 'DJANGO_EXPORTS_REQUIRE_PERM', None):
            opts = self.opts
            codename = '%s_%s' % ('csv', opts.object_name.lower())
            return request.user.has_perm("%s.%s" % (opts.app_label, codename))
        return True


if getattr(settings, 'DJANGO_CSV_GLOBAL_EXPORTS_ENABLED', True):
    admin.site.add_action(export_as_csv)
