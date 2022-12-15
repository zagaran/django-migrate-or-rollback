# django-migrate-or-rollback

While single migrations in Django are atomic (as long as they have the default `atomic=True`),
a group of migrations are not.  Thus, when running migrations, you can have a partial
failure where some but not all of your migrations succeed.  This library fixes that.

This library provides a new management command `migrate_or_rollback`.  It's a drop-in
replacement for the Django builtin management command `migrate`.  Here's how it works:

1. Checks your database and current migration files for the latest migrations run per Django app.
2. Runs migrations as normal.
3. If migrations fail, it rolls back to the migrations identified in step 1.

## Instalation

`pip install django-migrate-or-rollback`

Alternatively, add `django-migrate-or-rollback` to your requirements.txt file.

Then, add `django_migrate_or_rollback` to your `INSTALLED_APPS` in settings.py, like so:

```
INSTALLED_APPS = [
    # ...
    "django_migrate_or_rollback",
]
```

## Usage

Run `python managage.py migrate_or_rollback` instead of the standard `migrate` command.

In particular, you should use `migrate_or_rollback` in place of `migrate` in your deployment scripts or CI/CD system.

`migrate_or_rollback` has all of the same options as `migrate`, such as `--noinput`.
