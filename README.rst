django_exports
========================

Welcome to the documentation for django-django_exports!

Features
-----------------------------------

- Easy installation
- High level of customizability
- Created with permissions in mind
- Sane defaults

Installation
----------------------------------

- Python 2.7, 3.3+
- `Django <http://www.djangoproject.com/>`_ >= 1.5

To install::

    pip install django-exports

Next add `django_exports` to your `INSTALLED_APPS` to include the related css/js::

    INSTALLED_APPS = (
        # Other apps here
        'django_csv_exports',
    )


Configuration
-----------------------------------
There are two django settings that you can use to configure who can use the export action::

    # Use if you want to check user level permissions only users with the can_csv_<model_label>
    # will be able to download csv files.
    DJANGO_EXPORTS_REQUIRE_PERM = True
    # Use if you want to disable the global django admin action. This setting is set to True by default.
    DJANGO_CSV_GLOBAL_EXPORTS_ENABLED = False


Fields to export
---------------------------------
By default, all of the fields available in a model ar ordered and exported. You can override this behavior
at the admin model level. Define the following attribute in your AdminModel::

    class ClientAdmin(CSVExportAdmin):
        csv_fields = ['first_name', 'last_name', 'email', 'phone_number',]


Permission granularity
--------------------------------
User permissions: If you want to limit who can export CSV files from the admin interface.
You can define a custom permission in your model::

    class Client(models.Model):
        class Meta:
            permissions = (("can_csv_client", "Can export list of clients as CSV file"),)

The second way to limit who has access to exporting as csv is by defining a `has_csv_permission`
method in your admin model as follows::

    class ClientAdmin(CSVExportAdmin):
        search_fields = ('name', 'id', 'email')
        csv_fields = ['name', 'id']

        def has_csv_permission(self, request):
            """Only super users can export as CSV"""
            if request.user.is_superuser:
                return True


Running the Tests
------------------------------------

You can run the tests with via::

    python setup.py test

or::

    python runtests.py
