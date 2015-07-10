Django CSV Exports
========================

An admin action that allows you to export your models as CSV files without
having to write a single line of code --besides installation, of course.

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


Permission
--------------------------------
There are two ways to limit who can export data as CSV files.

Model level permissions: create a new model permission and assign it only to
user who should have access to the export action in the admin.

    class Client(models.Model):
        class Meta:
            permissions = (("can_csv_client", "Can export list of clients as CSV file"),)

AdminModel Level permissions: define a `has_csv_permission` and return True if a user should have access::

    class ClientAdmin(admin.AdminModel):
        search_fields = ('name', 'id', 'email')
        csv_fields = ['name', 'id']

        def has_csv_permission(self, request):
            """Only super users can export as CSV"""
            if request.user.is_superuser:
                return True


Selective Installation
-------------------------
Sometimes, you don't want to allow all of your admin models to be exported. For this, you will need to
set `DJANGO_CSV_GLOBAL_EXPORTS_ENABLED` to False, and have your AdminModels extend our `CSVExportAdmin`
admin class::

    from django_csv_exports.admin import CSVExportAdmin

    class ClientAdmin(CSVExportAdmin):
        pass


Running the Tests
------------------------------------

You can run the tests with via::

    python setup.py test

or::

    python runtests.py
